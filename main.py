update_id = "3a34d712-ee6f-46fa-991a-e7d9520c16fc"

packages = {
    # "microsoft-windows-client-languagepack-package_en-us-amd64-en-us.esd",
    "Microsoft-Windows-WordPad-FoD-Package-wow64.cab",
    "Microsoft-Windows-WordPad-FoD-Package-wow64-en-us.cab",
    "Microsoft-Windows-WordPad-FoD-Package-amd64.cab",
    "Microsoft-Windows-WordPad-FoD-Package-amd64-en-us.cab",
    "Microsoft-Windows-WMIC-FoD-Package-wow64.cab",
    "Microsoft-Windows-WMIC-FoD-Package-wow64-en-us.cab",
    "Microsoft-Windows-WMIC-FoD-Package-amd64.cab",
    "Microsoft-Windows-WMIC-FoD-Package-amd64-en-us.cab",
    "Microsoft-Windows-Notepad-FoD-Package-wow64.cab",
    "Microsoft-Windows-Notepad-FoD-Package-wow64-en-us.cab",
    "Microsoft-Windows-Notepad-FoD-Package-amd64.cab",
    "Microsoft-Windows-Notepad-FoD-Package-amd64-en-us.cab",
    "Microsoft-Windows-Notepad-System-FoD-Package-amd64.cab",
    "Microsoft-Windows-Notepad-System-FoD-Package-amd64-en-us.cab",
    "Microsoft-Windows-Notepad-System-FoD-Package-wow64.cab",
    "Microsoft-Windows-Notepad-System-FoD-Package-wow64-en-us.cab",
}

import requests
import xml.etree.ElementTree as ET

document = ET.parse("x.mum")
root = document.getroot()


packages = set(map(lambda s: s.lower(), packages))
# for update in root.findall(
#     ".//{urn:schemas-microsoft-com:asm.v3}update/{urn:schemas-microsoft-com:asm.v3}package/{urn:schemas-microsoft-com:asm.v3}assemblyIdentity"
# ):
#     packages.add(update.get("name").lower() + ".esd")

response = requests.get(f"https://api.uupdump.net/get.php?id={update_id}")
fetched = set()
if response.status_code == 200:
    try:
        data = response.json()["response"]["files"]
    except:
        print("! ", response.json()["response"]["error"])
        exit(1)
    with open("links.txt", "w+") as f:
        f.truncate(0)
        for filename, data in data.items():
            if filename.lower() in packages:
                f.write(data["url"] + "\n\tout=" + filename + "\n")
                print(f"# Got {filename}")
                fetched.add(filename.lower())

for package in packages.difference(fetched):
    print(f"! Didn't get {package}")
