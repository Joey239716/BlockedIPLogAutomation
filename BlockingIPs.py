import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = 'https://api.abuseipdb.com/api/v2/check'
apiKey = os.getenv("API_KEY")
print(apiKey)

headers = {
    'Accept': 'application/json',
    'Key': apiKey
}

directory = str(input("Input the directory you would like to access the ips in (copy the path of the folder and remove quotation marks): "))

clientIps = set()

# Checks all files in the folder and any of its subfolders in a recursive fashion
for path, folders, files in os.walk(directory):
    for filename in files:
        if filename.lower().endswith((".zip", ".gz", ".tar", ".7z")):
            continue
        file_path = os.path.join(path, filename)
        print(f"Reading file: {file_path}")
        
        try:
            with open(file_path, encoding='utf-8', errors='ignore') as f:
                data = []
                for line in f:
                    data.append(json.loads(line))

                for json_object in data:
                    if json_object["action"] == "BLOCK":
                        clientIps.add(json_object["httpRequest"]["clientIp"])
        except Exception as e:
            print(f"Could not read {file_path}: {e}")                



print("The number of IPs is " + str(len(clientIps)))
print(clientIps)

ipInformation = []

shortForm = {"United States of America": "USA", "United Kingdom of Great Britain and Northern Ireland": "UK", "Korea (the Republic of)": "South Korea"}

clientIps = list(clientIps)
#Code that uses the API KEY, Pulls data from AbusedIp API
for ip in clientIps:
        response = requests.request(method='GET', url=url, headers=headers, params={'ipAddress': ip, 'maxAgeInDays': '90', 'verbose': 'true'})

        decodedResponse = json.loads(response.text)

        if decodedResponse["data"]["countryName"] in shortForm:
            decodedResponse["data"]["countryName"] = shortForm[decodedResponse["data"]["countryName"]]

        # Notifies if confidence of abuse score is less than 5%
        if decodedResponse["data"]["abuseConfidenceScore"] < 5:
            confidenceScore = "(Confidence of Abuse is " + str(decodedResponse["data"]["abuseConfidenceScore"]) + "%)"   
            ipInformation.append([ip, decodedResponse["data"].get("domain", "N/A"), decodedResponse["data"]["countryName"], confidenceScore])
        else:
            ipInformation.append([ip, decodedResponse["data"].get("domain", "N/A"), decodedResponse["data"]["countryName"]])


print(ipInformation)

for i, row in enumerate(ipInformation, start=1):
    cleaned = [field if field is not None else "N/A" for field in row]
    print(" - ".join(cleaned))


"""
Testing code

# Code that uses the API KEY, Pulls data from AbusedIp API
for i in range(0, 3):
        response = requests.request(method='GET', url=url, headers=headers, params={'ipAddress': clientIps[i], 'maxAgeInDays': '90', 'verbose': 'true'})

        decodedResponse = json.loads(response.text)

        if decodedResponse["data"]["countryName"] in shortForm:
            decodedResponse["data"]["countryName"] = shortForm[decodedResponse["data"]["countryName"]]

        # Notifies if confidence of abuse score is less than 5%
        if decodedResponse["data"]["abuseConfidenceScore"] < 5:
            confidenceScore = "(Confidence of Abuse is " + str(decodedResponse["data"]["abuseConfidenceScore"]) + "%)"   
            ipInformation.append([clientIps[i], decodedResponse["data"].get("domain", "N/A"), decodedResponse["data"]["countryName"]], confidenceScore)
        else:
            ipInformation.append([clientIps[i], decodedResponse["data"].get("domain", "N/A"), decodedResponse["data"]["countryName"]])


print(ipInformation)
"""