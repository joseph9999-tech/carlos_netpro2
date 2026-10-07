import sys
from ncclient import manager
from ncclient.operations import RPCError

# 1. Connect to your Cisco IOS-XE Device
try:
    conn = manager.connect(
        host="192.168.100.10",       # Replace with your lab switch/router IP
        port=830,
        username="admin",            # Replace with your credentials
        password="admin_password",
        hostkey_verify=False
    )
    print("🚀 Connected successfully via NETCONF!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)

# Step 1: Check server capabilities
caps = conn.server_capabilities
has_candidate = any("candidate" in cap for cap in caps)
has_openconfig = any("openconfig" in cap for cap in caps)

if not has_candidate:
    print("❌ Critical: Device does not support candidate datastore. Exiting.")
    conn.close_session()
    sys.exit(1)

# Step 2 & 3: Your configuration payload (Example: Setting a description on GigabitEthernet1)
# Note: Using native IOS-XE YANG namespace here as a universal baseline
config_payload = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com">
        <interface>
            <GigabitEthernet>
                <name>1</name>
                <description>Automated Uplink via NETCONF Loop</description>
            </GigabitEthernet>
        </interface>
    </native>
</config>
"""

try:
    # Step 4: Lock the candidate datastore to block other users mid-change
    print("🔒 Locking candidate datastore...")
    conn.lock(target="candidate")

    # Step 5: Push the XML payload to the candidate target
    print("📝 Editing configuration in candidate...")
    conn.edit_config(target="candidate", config=config_payload)

    # Step 6: Validate the syntax of the candidate datastore
    print("🔍 Validating candidate configurations...")
    conn.validate(source="candidate")

    # Step 7: Confirmed Commit (Safety net: rolls back automatically if we lose connection)
    print("✈️ Performing confirmed commit (Timeout: 60s)...")
    conn.commit(confirmed=True, timeout=60)

    # Step 8: Verification phase (Querying running config back to check the change)
    print("🧐 Verifying from running configuration...")
    filter_xml = """
    <native xmlns="http://cisco.com">
        <interface>
            <GigabitEthernet>
                <name>1</name>
            </GigabitEthernet>
        </interface>
    </native>
    """
    running_state = conn.get_config(source="running", filter=('subtree', filter_xml))
    
    # Simple evaluation check
    if "Automated Uplink via NETCONF Loop" in str(running_state):
        print("✅ Verification passed: Description matches intent!")
        # Step 10: Confirming the commit makes it permanent
        conn.commit() 
        print("🎉 Configuration permanently applied.")
    else:
        # Step 9: Manually triggering a rollback if verification fails
        print("⚠️ Verification failed! Discarding changes...")
        conn.discard_changes()

except RPCError as rpc_err:
    print(f"❌ NETCONF Protocol Error encountered: {rpc_err}")
    print("🔄 Rolling back candidate changes safely...")
    try:
        conn.discard_changes()
    except Exception:
        pass

except Exception as general_err:
    print(f"❌ Script / System Error: {general_err}")

finally:
    # Step 11: Clean up environment constraints
    print("🔓 Unlocking and closing session.")
    try:
        conn.unlock(target="candidate")
    except Exception:
        pass
    conn.close_session()
