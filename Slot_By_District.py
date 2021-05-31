import requests
from datetime import datetime, timedelta
import time
import winsound

age = 48
districts = [{"district_id": 770, "district_name": "Ahmedabad Corporation"},
             # {"district_id": 179, "district_name": "Anand"},
             # {"district_id": 180, "district_name": "Bharuch"},
             # {"district_id": 176, "district_name": "Botad"},
             # {"district_id": 181, "district_name": "Chhotaudepur"},
             # {"district_id": 182, "district_name": "Dahod"},
             # {"district_id": 153, "district_name": "Gandhinagar"},
             # {"district_id": 772, "district_name": "Gandhinagar Corporation"},
             # {"district_id": 156, "district_name": "Kheda"},
             # {"district_id": 183, "district_name": "Mahisagar"},
             # {"district_id": 184, "district_name": "Narmada"},
             # {"district_id": 185, "district_name": "Panchmahal"},
             # {"district_id": 776, "district_name": "Surat Corporation"},
             # {"district_id": 166, "district_name": "Tapi"},
             # {"district_id": 155, "district_name": "Vadodara"},
             # {"district_id": 777, "district_name": "Vadodara Corporation"}
             ]
pincodes = ["411046", "411007", "411056"]
num_days = 1

print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

while True:
    counter = 0

    for district in districts:
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
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0):
                                    print(f'District: {district["district_name"]}')
                                    print("\t", f'Pincode: {center["pincode"]}')
                                    print("\t", "Slot Opened on: {}".format(given_date))
                                    print("\t", "Available on: {}".format(session['date']))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Age Limit: ", session["min_age_limit"])
                                    print("\t Availablity : ", session["available_capacity"])
                                    print("\t Dose 1 Availablity : ", session["available_capacity_dose1"])
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
        print("Search Completed!")

    dt = datetime.now() + timedelta(minutes=3)

    while datetime.now() < dt:
        time.sleep(1)
