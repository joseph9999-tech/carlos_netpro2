import requests
import urllib3
from requests.auth import HTTPBasicAuth


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://sandbox-router/restconf/data/openconfig-system:system/ntp"
url1 = "https://sandbox-router/restconf/data/openconfig-system:system/ntp"
url2= "https://sandbox-router/restconf/data/openconfig-system:system/ntp/servers/server=time.google.com"

query_params= {
    "depth": 8
}
payload = """
   
      
         <ntp xmlns="http://openconfig.net/yang/system">
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
       
     
    
"""

header = {
    "Content-Type": "application/yang-data+xml",
    "Accept": "application/yang-data+xml"
}

try:
    response = requests.patch(url=url, headers=header, auth=("admin", "admin"), data=payload, verify=False)

    if response.status_code in (200,204,201):
        print("commit success!!")
    
    else :
        print(f"error {response.status_code} occured!!")
        print(f"error-body: {response.text}")

    
    
except Exception as e:
    print(f"error occurred: {e}")


try:
    print("verifying config change.....")
    resp1 = requests.get(url=url1, verify=False, headers=header, auth=("admin", "admin"), params=query_params)
    if resp1.status_code == 200:

       print(resp1.text)

    

except Exception as e:
    print(f"error occurred: {e}")


try:
    resp2 = requests.delete(url=url2, verify=False, auth=("admin", "admin"), headers=header)
    if resp2.status_code in (200,204):
        print(f"delete success !!")
        print(f"status-code: {resp2.status_code}")
    else:
        print(f"error {resp2.status_code} occurred")
        print(f"error-body: {resp2.text} ")
except Exception as e:
    print(f"connection error {e} happened!!!")
