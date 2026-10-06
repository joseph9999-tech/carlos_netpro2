from ncclient import manager
from ncclient.operations import RPCError

device = {
    "host": "sandbox-router",
    "port": 830,
    "username": "admin",
    "password": "admin",
    "hostkey_verify": False,
    "device_params": {"name": "default"}
}

config_payload = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
     <interface>
       <name>Ethernet2</name>
       <config>
          <description>Uplink to core</description>
          <mtu>9000</mtu>

       </config>
     </interface>
  </interfaces>  
</config>
"""



get_payload = """
  <filter type="subtree">
    <interfaces xmlns="http://openconfig.net/yang/interfaces">
      <interface>
        <name>Ethernet2</name>
        <config>
          <description/>
          <mtu/>
        </config>
      </interface>
    </interfaces>
  </filter>

"""

hostname_payload = """
  <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <system xmlns="http://openconfig.net/yang/system">
      <hostname>router-phase2</hostname>
    </system>
  </config>

"""

gethostname_payload = """
  <filter type="subtree">
    <system xmlns="http://openconfig.net/yang/system">
      <hostname/>
    </system>
  </filter>

"""

dns_payload= """
  <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <system xmlns="http://openconfig.net/yang/system">
      <dns>
        <servers>
          <server>
            <address>8.8.8.8</address>
            <config>
               <address>8.8.8.8</address>
               <port>53</port>
            </config>
          </server>
        </servers>
      </dns>
    </system>
  </config>

"""

ntp_server_payload = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <system xmlns="http://openconfig.net/yang/system">
    <ntp>
      <servers>
        <server>
          <address>time.google.com</address>
          <config>
            <address>time.google.com</address>
            <version>4</version>
          </config>
        </server>
      </servers>
    </ntp>
  </system>
</config>
"""

# ─── NTP global config (enabled) ───────────────────────
ntp_global_payload = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <system xmlns="http://openconfig.net/yang/system">
    <ntp>
      <config>
        <enabled>true</enabled>
      </config>
    </ntp>
  </system>
</config>
"""

# ─── Filter: NTP servers ───────────────────────────────
ntp_server_filter = """
<filter type="subtree">
  <system xmlns="http://openconfig.net/yang/system">
    <ntp>
      <servers>
        <server>
          <address>time.google.com</address>
          <config>
            <address/>
            <version/>
          </config>
        </server>
      </servers>
    </ntp>
  </system>
</filter>
"""

# ─── Filter: NTP global config ─────────────────────────
ntp_global_filter = """
<filter type="subtree">
  <system xmlns="http://openconfig.net/yang/system">
    <ntp>
      <config>
        <enabled/>
      </config>
    </ntp>
  </system>
</filter>
"""

with manager.connect(**device) as m:
  try:
    response = m.edit_config(target="candidate", config=ntp_payload)
    print("edit ok!")
    
  except RPCError as e:
    print(f"error encountered!!: {e}")
    print(f"error-tag: {e.tag}")
    print(f"error-message: {e.message}")
    raise SystemExit(1)

  try:
    commit_response=m.commit()
    print("commit ok!")
    
  except RPCError as e:
        print(f"error encountered!!: {e}")
        print(f"error-tag: {e.tag}")
        print(f"error-message: {e.message}")
        raise SystemExit(1)

  try:
     resp2 = m.edit_config(target="candidate", config=ntp2_payload)
     print("edit ok!")
  except RPCError as e:
     print(f"error {e.tag} occurred!!")
     print(f"error-body: {e.message}")

  try:
     resp3 = m.commit()
     print("commit ok!")
  except RPCError as e:
       print(f"error {e.tag} occurred!!")
       print(f"error-body: {e.message}")

  print("verifying configurations.......")
  resp1 = m.get_config(source="running", filter=ntp_verify_payload)
  print(resp1)

  resp4 = m.get_config(source="running", filter=ntp2_verify_payload)
  print(resp4)

