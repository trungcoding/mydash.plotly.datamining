import requests
import json
import datetime
import pandas as pd

API_KEY = 'f082486ac50b9a79f4a25c1c4e8edbc3'
LAT = '21.028511'
LON = '105.804817'

URL = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={LAT}&lon={LON}&dt=1664622000&appid={API_KEY}"
response = requests.get(URL).json()


def tempK_to_tempC(tempK):
    tempC = tempK - 273.15
    return tempC


def dtUTC_to_datetime(response):
    datetimes = []
    response2 = response['daily']
    for item in response2:
        dt_value = item['dt']
        tempMax = tempK_to_tempC(item['temp']['max'])
        tempMin = tempK_to_tempC(item['temp']['min'])
        tempDay = tempK_to_tempC(item['temp']['day'])
        tempNight = tempK_to_tempC(item['temp']['night'])
        tempEve = tempK_to_tempC(item['temp']['eve'])
        tempMorn = tempK_to_tempC(item['temp']['morn'])
        tempAvg = (tempDay + tempEve + tempMorn + tempNight)/4
        dt_object = datetime.date.fromtimestamp(dt_value)
        datetimes.append([dt_object, tempAvg, tempMin, tempMax])
        # datetimes.append(dt_object)
        # datetimes.append(tempAvg)
        # datetimes.append(tempMin)
        # datetimes.append(tempMax)
    df = pd.DataFrame(datetimes)
    return df


# print(dtUTC_to_datetime(response))
# print(response)
with open('2022_10_1.json', 'w') as outfile:
    json.dump(response, outfile)
# print(tempK_max)
