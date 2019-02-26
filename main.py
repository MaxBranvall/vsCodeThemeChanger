from time import gmtime, strftime, sleep
from sys import exit
import requests
import json

VSCODE_SETTINGS_PATH = "/Users/max.branvall/Library/Application Support/Code/User/settings.json"
CONFIG = "config/config.json"
API = "https://api.sunrise-sunset.org/json" # format = json?lat=VALUE&lng=VALUE

def formatTimes(sunrise, sunset):

    if ':' in sunrise[0:2]:
        sunrise = sunrise[0:4] + sunrise[7:]
    else:
        sunrise = sunrise[0:5] + sunrise[8:]

    if ':' in sunset[0:2]:
        sunset = sunset[0:4] + sunset[7:]
    else:
        sunset = sunset[0:5] + sunset[8:]

    return sunrise, sunset

def setTheme(theme):
    with open(VSCODE_SETTINGS_PATH, 'r') as x:
        f = json.load(x)
        f['workbench.colorTheme'] = theme

    with open(VSCODE_SETTINGS_PATH, 'w') as x:
        json.dump(f, x)

class Main:

    def __init__(self):
        self.lightTheme = None
        self.darkTheme = None

        self.latitude = None
        self.longituide = None
        self.sunrise = None
        self.sunset = None

        self.currentTime = self._getCurrentTime()

        self._setConfig()
        self.getSunriseSunset(self.latitude, self.longituide)

    def _setConfig(self):
        """
        Initializes the themes and coordinates
        """
        with open(CONFIG, 'r') as x:
            f = json.load(x)
            self.lightTheme = f['vsCodeConfig']['lightTheme']
            self.darkTheme = f['vsCodeConfig']['darkTheme']

            self.latitude = f['apiConfig']['latitude']
            self.longituide = f['apiConfig']['longitude']

    def _getCurrentTime(self):
        """
        Return current time in H/HH:MM pp format.
        """
        t = strftime("%-I:%M %p", gmtime())
        return t

    def getSunriseSunset(self, lat, lng):
        """
        Grabs sunrise and sunset times, formats them correctly, and stores them in member variables.
        """
        response = requests.get(API + f'?lat={lat}&lng={lng}')
        responseJSON = json.loads(response.text)

        self.sunrise, self.sunset = formatTimes(responseJSON['results']['sunrise'], responseJSON['results']['sunset'])

if __name__ == '__main__':

    main = Main()
    print(f"Sunrise: {main.sunrise}\nSunset: {main.sunset}")

    try:
        while True:

            # If it is midnight.
            if main.currentTime == '6:00 AM':
                print(f"Sunrise: {main.sunrise}\nSunset: {main.sunset}")

            else:
                if main.currentTime == main.sunrise:
                    setTheme(main.lightTheme)

                elif main.currentTime == main.sunset:
                    setTheme(main.darkTheme)

            sleep(5)

    except KeyboardInterrupt:
        exit()
