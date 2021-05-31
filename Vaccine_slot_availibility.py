import requests
from datetime import datetime, timedelta
import time
import winsound

header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    'Accept-Language': "hi_IN",
    "accept": "application/json"
}
# Url to Get state list
state_url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
district_url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}"

result = requests.get(state_url, headers=header)

if result.ok:
    response_json = result.json()
    state_list = response_json['states']
    print("List of Available State")
    selected_state = {}
    for state in state_list:
        print(f"{state['state_name']}")
        # Get Details of Gujarat State First
        if state['state_name'].lower() == "gujarat":
            selected_state = state

    state_name = input("Enter State name from above list.Leave Blank for Gujarat): ")
    if state_name:
        selected_state = list(filter(lambda d: d['state_name'].lower() == state_name.strip().lower(), state_list))
        # selected_state = state_name
        if not selected_state:
            print(f'{state_name} is not available. Please check a spelling mistake.')
            exit(0)
        else:
            selected_state = selected_state[0]

    result = requests.get(district_url.format(selected_state["state_id"]), headers=header)
    if result.ok:
        districts = result.json()["districts"]

        print("List of Available Districts")
        for district in districts:
            print(f"{district['district_name']}")

        district_names = input(
            "Enter District Name(You can enter comma separated district names like(Ahmedabad Corporation,Valsad)")
        # selected_districts = ['Ahmedabad Corporation']
        if district_names:
            selected_districts = district_names.split(",")
        else:
            print("Please enter at least one district name.")
            exit(0)

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

                        result = requests.get(URL, headers=header)

                        if result.ok:
                            response_json = result.json()
                            if response_json["centers"]:
                                if (print_flag.lower() == 'y'):
                                    for center in response_json["centers"]:
                                        for session in center["sessions"]:
                                            if (session["available_capacity"] > 0):
                                                if int(session["min_age_limit"]) == age_limit and (
                                                        (dose_type == 1 and int(
                                                            session["available_capacity_dose1"]) > 0) or
                                                        (dose_type == 2 and int(
                                                            session["available_capacity_dose2"]) > 0)):
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
                                                        print("\t Dose 1 Availablity : ",
                                                              session["available_capacity_dose1"])
                                                    if int(session["available_capacity_dose2"]) > 0:
                                                        print("\t Dose 2 Availablity : ",
                                                              session["available_capacity_dose2"])

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
