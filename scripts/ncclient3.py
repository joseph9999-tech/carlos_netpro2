import re
from ncclient import manager
from ncclient.operations import RPCError

payload = """
  <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
     <network-instances xmlns="http://openconfig.net/yang/network-instance">
       <network-instance>
          <name>DEFAULT_INSTANCE</name>
          <protocols>
             <protocol>
                <identifier xmlns:oc-pol-types="http://openconfig.net">BGP</identifier>
                <name>bgp</name>
                <bgp xmlns="http://openconfig.net/yang/bgp">
                   <neighbors>
                      <neighbor>
                         <neighbor-address>192.168.10.1</neighbor-address>
                         <config>
                            <neighbor-address>192.168.10.1</neighbor-address>
                            <neighbor-port>179</neighbor-port>
                         </config>
                      </neighbor>
                   </neighbors>
                </bgp>
             </protocol>
          </protocols>
       </network-instance>        
     </network-instances>
  </config>

"""

payload2 = """
  <filter type="subtree">
    <network-instances xmlns="http://openconfig.net/yang/network-instance">
       <network-instance>
          <name>DEFAULT_INSTANCE</name>
          <protocols>
             <protocol>
                <identifier>oc-pol-types:BGP</identifier>
                <name>bgp</name>
                <bgp xmlns="http://openconfig.net/yang/bgp">
                   <neighbors>
                      <neighbor>
                         <neighbor-address/>
                      </neighbor>
                   </neighbors>
                </bgp>
             </protocol>
          </protocols>
       </network-instance>        
     </network-instances>  
  </filter>
  

"""

device = {
    "host":"192.168.100.10",       
    "port":830,
    "username":"admin",            
    "password":"admin_password",
    "hostkey_verify":False
    }

try:
    conn = manager.connect(**device) 
    
    print(f"successful connected to host at {device['host']} \n")

        #checking hosts capabilities
    capab = conn.server_capabilities

    has_openconfig = any('openconfig' in cap for cap in capab)
    has_candidate = any('candidate' in cap for cap in capab)

    if has_openconfig and has_candidate:
        
        with conn.lock(target="candidate"):
              print("candidate locked ready for configurations....\n")
              bgp = conn.edit_config(target="candidate", payload=payload)

              conn.validate(source="candidate")
              conn.commit(confirmed=True, timeout=60)

              bgp_verification = conn.get_config("source=running", filter=payload2)
              if "192.168.10.1"  in str(bgp_verification):
                    print("verification success!!, proceeding to permanent commit...\n")
                    conn.commit()
                    print("commited permanently ✔✔")
              else:
                    print("verification failed, rolling-backing gracefully")
                    conn.discard_changes()

    else:
            print("device can't be configured, missing either openconfig or candidate or both, exiting.....\n")
            conn.close_session()
            SystemExit(1)  

except RPCError as e:
        print(f"failed to connect to the host {device['host']}, graceful exit...\n")
        print(f"rpcerror: {e.tag}\n")
        print(f"error-body: {e.message}\n")
        conn.discard_changes()


except Exception as e:
    print(f"error occured b4 connecting to the device: {e.message}\n")
    SystemExit(1)

finally:
    try:
      conn.unlock(target="candidate")
      print("candidate unlocked successfully!... closing session ......\n")
      conn.close_session()
    except Exception:
      pass
      
      

