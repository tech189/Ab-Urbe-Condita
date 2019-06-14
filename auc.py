# this script requires python 3.7+

import datetime, math        # calculating dates
import json, urllib.request  # getting and parsing sunrise/set data
import sys                   # commandline arguments

help_text = "Converts dates into a Roman format\n\t--help\t\tshows this help text\n\t--now\t\tconvert current date and time\n\t--custom\t\tconvert a custom date (ISO 8601)\n\t--simple\t\tonly print the Roman format"

roman_months = ["Januarius", "Februarius", "Martius", "Aprilis", "Maius", "Junius", "Quintilius", "Sextilis", "September", "October", "November", "December"]
months_genitive = ["Januarii", "Februarii", "Martii", "Aprilis", "Maii", "Junii", "Quintilii", "Sextilis", "Septembris", "Octobris", "Novembris", "Decembris"]
weekdays = ["Lunae", "Martis", "Mercurii", "Iovis", "Veneris", "Saturni", "Solis"]

def int_to_roman(num):
    # https://stackoverflow.com/a/50012689
    _values = [
        1000000, 900000, 500000, 400000, 100000, 90000, 50000, 40000, 10000, 9000, 5000, 4000, 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]

    _strings = [
        'M', 'C', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', "M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

    result = ""
    decimal = num

    while decimal > 0:
        for i in range(len(_values)):
            if decimal >= _values[i]:
                if _values[i] > 1000:
                    result += u'\u0304'.join(list(_strings[i])) + u'\u0304'
                else:
                    result += _strings[i]
                decimal -= _values[i]
                break
    return result

today = datetime.datetime.now()

def get_year(input_date):
    # AUC = 21 April 752 BC

    if input_date.month == 4 and input_date.day < 21:
        auc = input_date.year + 752
    elif input_date.month == 4 and input_date.day >= 21:
        auc = input_date.year + 753
    elif input_date.month < 4:
        auc = input_date.year + 752
    elif input_date.month > 4:
        auc = input_date.year + 753
    
    return int_to_roman(auc)

def get_day(input_date):
    kalends = input_date.replace(day=1)

    if input_date.month in [3, 5, 7, 10]:
        nones = kalends + datetime.timedelta(days = 6)
    else:
        nones = kalends + datetime.timedelta(days = 4)

    ides = nones + datetime.timedelta(days = 8)

    if input_date.day > 13:
        kalends2 = input_date + datetime.timedelta(days = 20)
        kalends2 = kalends2.replace(day = 1)
        kalends2_delta = input_date - kalends2
        # print(kalends2, kalends2_delta)

    kalends_delta = input_date - kalends
    nones_delta = input_date - nones
    ides_delta = input_date - ides

    # for debugging:
    # print(kalends, nones, ides)
    # print(kalends_delta, nones_delta, ides_delta)

    # roman date goes to the closest marker in the future not the past, also need to check delta of the kalends of the next month!
    # plus one because Romans counted inclusively...


    if input_date.day == 1:
        day = "kalends " + months_genitive[input_date.month - 1]
    elif input_date.day < nones.day:
        day = "diem " + int_to_roman(abs(nones_delta.days) + 1) + " ante Nonas " + months_genitive[input_date.month - 1]
    elif input_date.day == nones.day:
        day = "Nones " + months_genitive[input_date.month - 1]
    elif input_date.day < ides.day:
        day = "diem " + int_to_roman(abs(ides_delta.days) + 1) + " ante Idus " + months_genitive[input_date.month - 1]
    elif input_date.day == ides.day:
        day = "Idus " + months_genitive[input_date.month - 1]
    else:
        day = "diem " + int_to_roman(abs(kalends2_delta.days) + 1) + " ante Kalendas " + months_genitive[input_date.month]

    result = "dies " + weekdays[input_date.weekday()] + ", " + day

    return result

def get_time(input_date):
    # get sunrise/sunset from internet, then work out length of hour

    # cache data for a whole day, then get new data when day changes
    try:
        with open("sunrisesunset-" + input_date.strftime("%Y%m%d") + ".json", "r", encoding="utf-8") as response:
            data = response.read()
            jsondata = json.loads(data)
    except:
        # requests the data for the current day of timezone - ISO 8601 format
        response = urllib.request.urlopen("https://api.sunrise-sunset.org/json?lat=51.509865&lng=-0.118092&formatted=0&date=" + input_date.strftime("%Y-%m-%d"))
        with open("sunrisesunset-" + input_date.strftime("%Y%m%d") + ".json", "w", encoding="utf-8") as outfile:
            data = response.read().decode("utf-8")
            jsondata = json.loads(data)
            json.dump(jsondata, outfile)

    sunrise = datetime.datetime.fromisoformat(jsondata["results"]["sunrise"])
    local_timezone = datetime.datetime.now().astimezone().tzinfo
    sunrise = sunrise.astimezone(local_timezone)

    sunset = datetime.datetime.fromisoformat(jsondata["results"]["sunset"])
    local_timezone = datetime.datetime.now().astimezone().tzinfo
    sunset = sunset.astimezone(local_timezone)

    input_date = input_date.replace(tzinfo=local_timezone)
    # print(input_date, sunrise, sunset)

    day_duration = sunset - sunrise
    hour_length = day_duration/12
    midday = sunrise + (day_duration/2)
    morning_portion = input_date - sunrise
    afternoon_portion = sunset - input_date
    # print(hour_length, midday, morning_portion, afternoon_portion)

    if input_date < sunrise:
        hour = int_to_roman(math.floor(abs(morning_portion/hour_length)) + 1)
        time = "hora " + hour + " ante solis ortum"
    elif input_date == sunrise:
        time = "solis ortus"
    elif input_date < midday:
        hour = int_to_roman(math.floor(morning_portion/hour_length) + 1)
        time = "hora " + hour + " post solis ortum"
    elif input_date == midday:
        time = "meridies"
    elif input_date < sunset:
        hour = int_to_roman(math.floor(afternoon_portion/hour_length) + 1)
        time = "hora " + hour + " ante solis occasum"
    elif input_date == sunset:
        time = "solis occasus"
    elif input_date > sunset:
        hour = int_to_roman(math.floor(abs(afternoon_portion/hour_length)) + 1)
        time = "hora " + hour + " post solis occasum"
    
    return time

output = {}

if len(sys.argv) < 2:
    print(help_text)
else:
    if "--help" in sys.argv:
        output["help"] = help_text
    elif "--now" in sys.argv:
        input_date = datetime.datetime.now()
        output["normal"] = today.strftime("%H:%M, %A, %d %B %Y AD")
        output["roman"] = get_time(input_date) + ", " + get_day(input_date) + " " + get_year(input_date) + " AUC"
    if "--custom" in sys.argv:
        try:
            test = output["normal"]
            print("Please use either now or custom date")
            sys.exit()
        except KeyError:
            # custom time not supported
            try:
                input_date = datetime.datetime.fromisoformat(sys.argv[sys.argv.index("--custom") + 1])
            except:
                print("Date not in ISO 8601 format")
                sys.exit()
            output["normal"] = input_date.strftime("%d %B %Y AD")
            output["roman"] = get_day(input_date) + " " + get_year(input_date) + " AUC"
    
    if "--simple" in sys.argv:
        try:
            output.pop("normal")
        except:
            print("Please select either a normal or custom date")
            sys.exit()
    if output == {}:
        output["help"] = help_text

    for x in output:
        print(output[x])