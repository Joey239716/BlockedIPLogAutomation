# AWSLogAutomation
Automates checking the logs for which IP's were blocked

Download and extract the file into VScode

To run this program:

    1. Run this command in the terminal: pip install -r requirements.txt to install all necessary packages

    2. Create a .env file
        - add this into into the .env file: API_KEY = "APIKEY"

    3. Replace "APIKey" with an API Key from https://www.abuseipdb.com/account/api
        - The contents of the .env file should look like this example: 
        - API_KEY = 125565abd7737da5d4924e08203d090bc7306779e9aadbcb7dc196fef050bce03a556ff84cbe5825
    
    4. Make sure all the files in the folder you want to scan are in a readable format. Files like .zip .gz will not be scanned

    5. Run the program, it will prompt you for a directory to scan. 
    
    6. Copy the path from the folder you want to scan paste it into the program and make sure there isn't any quotation marks in the directory's path

    7. Press enter and let the program run 

    8. The results will be formatted into a list with items formatted as ip - domain - country 
