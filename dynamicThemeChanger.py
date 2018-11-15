import json
import requests
from datetime import datetime
from time import strftime, gmtime
from time import sleep

iteration = 0
sunriseTime = 0
sunsetTime = 0
currentTime = 0

settingsJSON = '../../Library/Application Support/Code/User/settings.json'
configJSON = 'json/config.json'

sunsetSunriseURL = (f'https://api.sunrise-sunset.org/json')

with open(configJSON, 'r') as x:
    items = json.load(x)
    apiParamDict = {'lat': items['apiConfig']['latitude'], 'lng': items['apiConfig']['longitude']}

    lightTheme = items['vsCodeConfig']['lightTheme']
    darkTheme = items['vsCodeConfig']['darkTheme']

def getSunriseSunsetTimes():

    apiResponse = requests.get(sunsetSunriseURL, params=apiParamDict)
    apiJSON = json.loads(apiResponse.text)

    return apiJSON['results']['sunrise'], apiJSON['results']['sunset']

def formatTime(sunriseTime, sunsetTime):

    if ':' in sunriseTime[:2]:
        sunriseTime = ('0' + sunriseTime)

    if ':' in sunsetTime[:2]:
        sunsetTime = ('0' + sunsetTime)

    sunriseTime = (sunriseTime[0:5] + sunriseTime[-2:])
    sunsetTime = (sunsetTime[0:5] + sunsetTime[-2:])

    return sunriseTime, sunsetTime

def settingsHandler(theme):
    with open(settingsJSON, 'r') as x:
        f = json.load(x)
        f['workbench.colorTheme'] = theme

    with open(settingsJSON, 'w') as x:
        json.dump(f, x, indent=4)

def setLightTheme():
    settingsHandler(lightTheme)

def setDarkTheme():
    settingsHandler(darkTheme)

def compareTimes(currentTime, sunriseTime, sunsetTime):

    if (currentTime == sunriseTime):
        setLightTheme()

    elif (currentTime == sunsetTime):
        setDarkTheme()

def main():

    global iteration, sunriseTime, sunsetTime, currentTime

    currentTime = strftime('%I:%M%p', gmtime())

    if iteration == 0:

        now = datetime.now()
        todaysDate = (f'{now.month}/{now.day}/{now.year}')

        sunriseTime, sunsetTime = getSunriseSunsetTimes()
        sunriseTime, sunsetTime = formatTime(sunriseTime, sunsetTime)

        cstSunrise = int(sunriseTime[:2]) - 6
        cstSunrise = str(cstSunrise) + sunriseTime[2:-2]

        cstSunset = int(sunsetTime[:2]) - 6
        cstSunset = str(cstSunset) + sunsetTime[2:-2]

        print(f'Date: {todaysDate}\n')
        print(f'Sunrise: {cstSunrise} AM\nSunset: {cstSunset} PM\n')

        iteration += 1

    if (currentTime == '06:00 AM'):

        now = datetime.now()
        todaysDate = (f'{now.month}/{now.day}/{now.year}')

        sunriseTime, sunsetTime = getSunriseSunsetTimes()
        sunriseTime, sunsetTime = formatTime(sunriseTime, sunsetTime)

        cstSunrise = int(sunriseTime[:2]) - 6
        cstSunrise = str(cstSunrise) + sunriseTime[2:-2]

        cstSunset = int(sunsetTime[:2]) - 6
        cstSunset = str(cstSunset) + sunsetTime[2:-2]

        print(f'Date: {todaysDate}\n')
        print(f'Sunrise: {cstSunrise} AM\nSunset: {cstSunset} PM\n')

    elif (currentTime != '06:00 AM'):
        compareTimes(currentTime, sunriseTime, sunsetTime)

while True:

    try:
        sleep(1)
        main()

    except KeyboardInterrupt:
        break
