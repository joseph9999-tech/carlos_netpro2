from ncclient import manager
from ncclient.operations import RPCError
import re

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
    response = m.edit_config(target="candidate", config=ntp_global_payload)
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
     resp2 = m.edit_config(target="candidate", config=ntp_server_payload)
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
  resp1 = m.get_config(source="running", filter=ntp_global_filter)
  print(resp1)

  resp4 = m.get_config(source="running", filter=ntp_server_filter)
  print(resp4)


## checking modules supported by a network device
modules = []
caps = m.server_capabilities
for cap in caps:
   

   match = re.search('module=([^&]*)', cap) #or 'module=(.*)', cap
   #e.search('openconfig(.*)', cap) for openconfig details
   if match:
    modules.append(match.group(1))

for m in modules:
   print(m)

## checking for candidate and openconfig

caps = m.server_capabilities
if "candidate" in caps:
  
   
    print("you can write in candidate")
else:
      print("no candidate")

all_caps = "".join(caps)

if "candidate" in all_caps:
    print("You can write in candidate!")
else:
    print("No candidate datastore available.")
    

if "openconfig" in all_caps:
   print("openconfig supported!!")

if any("candidate" in cap for cap in caps):
    print("You can write in candidate!")
else:
    print("No candidate datastore available.")
    

if any("openconfig" in cap for cap in caps):
   print("openconfig supported!!")

