import requests
import json
import os
from dotenv import load_dotenv
import gzip
import shutil

load_dotenv()

url = 'https://api.abuseipdb.com/api/v2/check'
apiKey = os.getenv("API_KEY")

headers = {
    'Accept': 'application/json',
    'Key': apiKey
}
directory = str(input("Input the directory you would like to access the ips in (copy the path of the folder and remove quotation marks): "))
def checkQuotations(directory):
    if directory[0] == '"' and directory[-1] == '"':
        return directory[1:-1]
    else:
        return directory

directory = checkQuotations(directory)


clientIps = set()

#Loading Bar from Stack Overflow
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def unzipGz(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".gz"):
                gz_path = os.path.join(dirpath, filename)
                output_path = os.path.join(dirpath, filename[:-3])  # Remove '.gz' extension

                # Skip if file already exists
                if os.path.exists(output_path):
                    print(f"Skipped (already exists): {output_path}")
                    continue

                try:
                    with gzip.open(gz_path, 'rb') as f_in:
                        with open(output_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    print(f"Extracted: {gz_path} -> {output_path}")
                except Exception as e:
                    print(f"Error extracting {gz_path}: {e}")
unzipGz(directory)


files_read_count = 0  # Count of successfully accessed log files

# Checks all files in the folder and any of its subfolders in a recursive fashion and looks for all Blocked IPS
for path, folders, files in os.walk(directory):
    for filename in files:
        # Only process files ending with .log (case insensitive)
        if not filename.lower().endswith(".log"):
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
            files_read_count += 1  # Increment only if successfully accessed
        except Exception as e:
            print(f"Could not read {file_path}: {e}")

print(f"\nNumber of log files read: {files_read_count}")         



print("The number of IPs is " + str(len(clientIps)))

ipInformation = []

shortForm = {"United States of America": "USA", "United Kingdom of Great Britain and Northern Ireland": "UK", "Korea (the Republic of)": "South Korea", "Viet Nam": "Vietnam"}

clientIps = list(clientIps)
#Code that uses the API KEY, Pulls data from AbusedIp API
for idx, ip in enumerate(clientIps):
        printProgressBar(idx, len(clientIps) - 1, prefix='Progress:', suffix='Complete', length=50)
        response = requests.request(method='GET', url=url, headers=headers, params={'ipAddress': ip, 'maxAgeInDays': '90', 'verbose': 'true'})
        decodedResponse = json.loads(response.text)

        if "data" not in decodedResponse:
            print(f"No data for IP: {ip} — {decodedResponse}")
            continue  # Skip this IP if no data is returned

        if decodedResponse["data"]["countryName"] in shortForm:
            decodedResponse["data"]["countryName"] = shortForm[decodedResponse["data"]["countryName"]]

        # Notifies if confidence of abuse score is less than 5%
        if decodedResponse["data"]["abuseConfidenceScore"] < 5:
            confidenceScore = "(Confidence of Abuse is " + str(decodedResponse["data"]["abuseConfidenceScore"]) + "%)"   
            ipInformation.append([ip, decodedResponse["data"].get("domain", "N/A"), decodedResponse["data"]["countryName"], confidenceScore])
        else:
            ipInformation.append([ip, decodedResponse["data"].get("domain", "N/A"), decodedResponse["data"]["countryName"]])
print("")

print("Blocked IPs")

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