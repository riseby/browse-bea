from site_parse import SiteParse
from site_parse import Gastrogate
from site_parse import Filmhuset
from site_parse import Sidahuset
from site_parse import Styrman

import datetime
import configparser
import json, sys, getopt
import holidays
import locale
locale.setlocale(locale.LC_TIME, "sv_SE.utf8")

def getLunchDates(startDate):
    dates =[]
    d = startDate
    dates.append(d)

    while startDate.isocalendar()[1] == d.isocalendar()[1] and d.weekday() < 4:
        d = d  + datetime.timedelta(days=1)
        dates.append(d)
    return dates


path = ""
configPath = ""
additionalDataFilename = "addData.txt"
ldataFilename = "lunchData.txt"
configFilename = "lunchData.config"
configToClass = {'': SiteParse, 'Gastrogate': Gastrogate, 'Sidahuset': Sidahuset, 'Filmhuset': Filmhuset, 'Styrman': Styrman}
lunchDates = getLunchDates(datetime.date.today())

if sys.argv[1]:
    path = sys.argv[1]
    configPath = sys.argv[1]

if sys.argv[2:]:
    path = sys.argv[1]
    configPath = sys.argv[2]

statuses = []

statusAdditional = False
try:
    with open(path + additionalDataFilename) as json_data:
        try:
            additionalData = json.load(json_data)
        except json.decoder.JSONDecodeError:
            print("Reading non-json file")
        if datetime.datetime.strptime(additionalData['created'],'%c').date() == datetime.datetime.today().date():
            statusAdditional = True
        else:
            svHolidays =data['holiday']
except:
    print("Problem reading file, creating new: " + additionalDataFilename)

try:
    with open(path + ldataFilename) as json_data:
        try:
            data = json.load(json_data)
        except json.decoder.JSONDecodeError:
            print("Reading non-json file")
        if datetime.datetime.strptime(data['created'],'%c').date() == datetime.datetime.today().date():
            for h in data['houses']:
                statuses.append(h['status'])
except:
    print("Problem reading file, creating new: " + ldataFilename)

if not statusAdditional:
    additionalData = {}
    additionalData['created'] = datetime.datetime.now().strftime('%c')
    svHolidays = holidays.SE()
    additionalData['holiday'] = svHolidays.get(datetime.date.today())
    additionalData['today'] = str(datetime.date.today())
    additionalData['dates'] = []
    for d in lunchDates:
        additionalData['dates'].append({'date': str(d), 'holiday': svHolidays.get(d)})
    with open(path + additionalDataFilename, 'w') as outfile:
        json.dump(additionalData, outfile)

if statuses and all(s == 200 for s in statuses):
    print("Updated and valid data already gathered, exit")
    exit()
else:
    lunchData = {}
    lunchData['created'] = datetime.datetime.now().strftime('%c')
    lunchData['additionalData'] = additionalData
    lunchData['houses'] = []
    config = configparser.ConfigParser()
    config.read(configPath + configFilename)

    for i in config.sections():
        h = configToClass[config[i]['type']](config[i]['url'], i,lunchDates)
        data = h.getData()
        lunchData['houses'].append(data)

    with open(path + ldataFilename, 'w') as outfile:
        json.dump(lunchData, outfile)

# # TODO:
# Update when to fetch data depending on statuses
# paket holidays, inte uppdatera pa roda dagar
# (?) separat json for ovrig information
