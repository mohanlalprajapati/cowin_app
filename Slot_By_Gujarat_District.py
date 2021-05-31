import requests
from datetime import datetime, timedelta
import time
import winsound

age = 48
districts = [{"district_id": 154, "district_name": "Ahmedabad"},
             {"district_id": 770, "district_name": "Ahmedabad Corporation"},
             {"district_id": 174, "district_name": "Amreli"}, {"district_id": 179, "district_name": "Anand"},
             {"district_id": 158, "district_name": "Aravalli"}, {"district_id": 159, "district_name": "Banaskantha"},
             {"district_id": 180, "district_name": "Bharuch"}, {"district_id": 175, "district_name": "Bhavnagar"},
             {"district_id": 771, "district_name": "Bhavnagar Corporation"},
             {"district_id": 176, "district_name": "Botad"}, {"district_id": 181, "district_name": "Chhotaudepur"},
             {"district_id": 182, "district_name": "Dahod"}, {"district_id": 163, "district_name": "Dang"},
             {"district_id": 168, "district_name": "Devbhumi Dwaraka"},
             {"district_id": 153, "district_name": "Gandhinagar"},
             {"district_id": 772, "district_name": "Gandhinagar Corporation"},
             {"district_id": 177, "district_name": "Gir Somnath"}, {"district_id": 169, "district_name": "Jamnagar"},
             {"district_id": 773, "district_name": "Jamnagar Corporation"},
             {"district_id": 178, "district_name": "Junagadh"},
             {"district_id": 774, "district_name": "Junagadh Corporation"},
             {"district_id": 156, "district_name": "Kheda"}, {"district_id": 170, "district_name": "Kutch"},
             {"district_id": 183, "district_name": "Mahisagar"}, {"district_id": 160, "district_name": "Mehsana"},
             {"district_id": 171, "district_name": "Morbi"}, {"district_id": 184, "district_name": "Narmada"},
             {"district_id": 164, "district_name": "Navsari"}, {"district_id": 185, "district_name": "Panchmahal"},
             {"district_id": 161, "district_name": "Patan"}, {"district_id": 172, "district_name": "Porbandar"},
             {"district_id": 173, "district_name": "Rajkot"},
             {"district_id": 775, "district_name": "Rajkot Corporation"},
             {"district_id": 162, "district_name": "Sabarkantha"}, {"district_id": 165, "district_name": "Surat"},
             {"district_id": 776, "district_name": "Surat Corporation"},
             {"district_id": 157, "district_name": "Surendranagar"}, {"district_id": 166, "district_name": "Tapi"},
             {"district_id": 155, "district_name": "Vadodara"},
             {"district_id": 777, "district_name": "Vadodara Corporation"},
             {"district_id": 167, "district_name": "Valsad"}]

# pincodes = ["411046", "411007", "411056"]

print("List of Available Districts")
for district in districts:
    print(f"{district['district_name']}")

district_names = input(
    "Enter District Name(You can enter comma separated district names like(Ahmedabad Corporation,Valsad) Default: Ahmedabad Corporation): ")
selected_districts = ['Ahmedabad Corporation']
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
