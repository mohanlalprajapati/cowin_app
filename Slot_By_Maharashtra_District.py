import requests
from datetime import datetime, timedelta
import time
import winsound

age = 48
districts = [
    {"district_id": 391, "district_name": "Ahmednagar"},
    {"district_id": 364, "district_name": "Akola"},
    {"district_id": 366, "district_name": "Amravati"},
    {"district_id": 397, "district_name": "Aurangabad "},
    {"district_id": 384, "district_name": "Beed"},
    {"district_id": 370, "district_name": "Bhandara"},
    {"district_id": 367, "district_name": "Buldhana"},
    {"district_id": 380, "district_name": "Chandrapur"},
    {"district_id": 388, "district_name": "Dhule"},
    {"district_id": 379, "district_name": "Gadchiroli"},
    {"district_id": 378, "district_name": "Gondia"},
    {"district_id": 386, "district_name": "Hingoli"},
    {"district_id": 390, "district_name": "Jalgaon"},
    {"district_id": 396, "district_name": "Jalna"},
    {"district_id": 371, "district_name": "Kolhapur"},
    {"district_id": 383, "district_name": "Latur"},
    {"district_id": 395, "district_name": "Mumbai"},
    {"district_id": 365, "district_name": "Nagpur"},
    {"district_id": 382, "district_name": "Nanded"},
    {"district_id": 387, "district_name": "Nandurbar"},
    {"district_id": 389, "district_name": "Nashik"},
    {"district_id": 381, "district_name": "Osmanabad"},
    {"district_id": 394, "district_name": "Palghar"},
    {"district_id": 385, "district_name": "Parbhani"},
    {"district_id": 363, "district_name": "Pune"},
    {"district_id": 393, "district_name": "Raigad"},
    {"district_id": 372, "district_name": "Ratnagiri"},
    {"district_id": 373, "district_name": "Sangli"},
    {"district_id": 376, "district_name": "Satara"},
    {"district_id": 374, "district_name": "Sindhudurg"},
    {"district_id": 375, "district_name": "Solapur"},
    {"district_id": 392, "district_name": "Thane"},
    {"district_id": 377, "district_name": "Wardha"},
    {"district_id": 369, "district_name": "Washim"},
    {"district_id": 368, "district_name": "Yavatmal"}
]

# pincodes = ["411046", "411007", "411056"]

print("List of Available Districts")
for district in districts:
    print(f"{district['district_name']}")

district_names = input(
    "Enter District Name(You can enter comma separated district names like(Pune,Nagpur) Default: Pune): ")
selected_districts = ['Pune']
if district_names:
    selected_districts = district_names.split(",")
print_flag = 'Y'
num_days = int(input("Number days to see the slot: "))


age_limit = 18
dose_type = 1
age_limit_input = input("Please enter age limit(18/45) Default 18: ")
if age_limit_input:
    age_limit = int(age_limit_input)

dose_type_input = input("Please enter 1 for Dose 1 and 2 for Dose Two. Default 1: ")
if dose_type_input:
    dose_type = int(dose_type_input)

print("Starting search for Covid vaccine slots!")
actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

while True:
    counter = 0

    for district in districts:
        if district['district_name'] in selected_districts:
            for given_date in actual_dates:

                URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district['district_id']}&date={given_date}"
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

                result = requests.get(URL, headers=header)

                if result.ok:
                    response_json = result.json()
                    if response_json["centers"]:
                        if (print_flag.lower() == 'y'):
                            for center in response_json["centers"]:
                                for session in center["sessions"]:
                                    if (session["available_capacity"] > 0):
                                        if int(session["min_age_limit"]) == age_limit and (
                                                (dose_type == 1 and int(session["available_capacity_dose1"]) > 0) or
                                                (dose_type == 2 and int(session["available_capacity_dose2"]) > 0)):
                                            print(f'District: {district["district_name"]}')
                                            print("\t", f'Pincode: {center["pincode"]}')
                                            print("\t", "Slot Opened on: {}".format(given_date))
                                            print("\t", "Available on: {}".format(session['date']))
                                            print("\t", center["name"])
                                            print("\t", center["block_name"])
                                            print("\t Price: ", center["fee_type"])
                                            print("\t Age Limit: ", session["min_age_limit"])
                                            print("\t Availablity : ", session["available_capacity"])
                                            if int(session["available_capacity_dose1"]) > 0:
                                                print("\t Dose 1 Availablity : ", session["available_capacity_dose1"])
                                            if int(session["available_capacity_dose2"]) > 0:
                                                print("\t Dose 2 Availablity : ", session["available_capacity_dose2"])

                                            if (session["vaccine"] != ''):
                                                print("\t Vaccine type: ", session["vaccine"])
                                            print("\n")
                                            counter = counter + 1
                else:
                    print("No Response!")
    if counter:
        print("Vaccination slot available!")
        winsound.PlaySound("*", winsound.SND_ALIAS)
    else:
        print("No Slot is available for given criteria")

    dt = datetime.now() + timedelta(minutes=3)

    while datetime.now() < dt:
        time.sleep(1)
