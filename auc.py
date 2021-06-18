# this script requires python 3.7+

import datetime, calendar, math     # calculating dates
import json, urllib.request         # getting and parsing sunrise/set data        
import sys                          # for logging to stdout
import os                           # caching sunrise/set data
import logging                      # debugging
import argparse                     # commandline arguments
import unicodedata                  # remove macrons

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

start_dir = os.path.dirname(os.path.realpath(__file__))

# roman months in the accusative plural
months_acc = ["Iānuāriās", "Februāriās", "Martiās", "Aprīlēs", "Māiās", "Iūniās", "Quīntīlēs", "Sextīlēs", "Septembrēs", "Octōbrēs", "Nouembrēs", "Decembrēs"]
months_acc_greg = ["Jānuāriās", "Februāriās", "Martiās", "Aprīlēs", "Māiās", "Jūniās", "Jūliās", "Augustās", "Septembrēs", "Octōbrēs", "Novembrēs", "Decembrēs"]

# roman months in the ablative plural
months_abl = ["Iānuāriīs", "Februāriīs", "Martiīs", "Aprīlibus", "Māiīs", "Iūniīs", "Quīntīlibus", "Sextīlibus", "Septembribus", "Octōbribus", "Nouembribus", "Decembribus"]
months_abl_greg = ["Jānuāriīs", "Februāriīs", "Martiīs", "Aprīlibus", "Māiīs", "Jūniīs", "Jūliīs", "Augustīs", "Septembribus", "Octōbribus", "Nouembribus", "Decembribus"]

# idiomatic abbreviations:
months_abbr = ["Iān.", "Feb.", "Mar.", "Apr.", "Maī.", "Iūn.", "Quī.", "Sex.", "Sep.", "Oct.", "Nou.", "Dec."]
months_greg_abbr = ["Jān.", "Feb.", "Mar.", "Apr.", "Maī.", "Jūn.", "Jūl.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]

weekdays = ["Lūnae", "Mārtis", "Mercuriī", "Iovis", "Veneris", "Saturnī", "Sōlis"]

def remove_macrons(str):
    result = unicodedata.normalize("NFKD", str).encode("ascii", "ignore").decode()
    return result

def int_to_roman(num):
    # shamelessly stolen from https://stackoverflow.com/a/50012689
    _values = [
        1000000, 900000, 500000, 400000, 100000, 90000, 50000, 40000, 10000, 9000, 5000, 4000, 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]

    _strings = [
        'M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', "M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

    result = ""
    decimal = num

    while decimal > 0:
        for i in range(len(_values)):
            if decimal >= _values[i]:
                if _values[i] > 1000:
                    result += u'\u0305'.join(list(_strings[i])) + u'\u0305'
                else:
                    result += _strings[i]
                decimal -= _values[i]
                break
    logging.debug(f"{num} --> {result}")
    return result

def get_year(input_date: datetime.datetime):
    if isinstance(input_date, datetime.datetime):
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
    else:
        logger.error("Input was not a datetime.datetime object")

def get_day(input_date, macron_pref):
    if isinstance(input_date, datetime.datetime):
        result = "diēs " + weekdays[input_date.weekday()]
        if macron_pref:
            return remove_macrons(result)
        else:
            return result
    else:
        logger.error("Input was not a datetime.datetime object")

def get_date(input_date: datetime.datetime, macron_pref, idiomatic: bool):
    if isinstance(input_date, datetime.datetime) and isinstance(idiomatic, bool):
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
            logger.debug(f"\n Next month's Kalends:        {str(kalends2)}\n Next month's Kalends' delta: {kalends2_delta}")

        nones_delta = input_date - nones
        ides_delta = input_date - ides

        # for debugging:
        logger.debug(f"\n Kalends: {kalends}\n Nones:   {nones}\n Ides:    {ides}")
        logger.debug(f"\n Nones' delta: {str(nones_delta)}\n Ides' delta:  {str(ides_delta)}")

        # roman date goes to the closest marker in the future not the past, also need to check delta of the kalends of the next month!
        # plus one because Romans counted inclusively...
        
        if idiomatic:
            if input_date.day == 1:
                day = "Kal. " + months_abbr[input_date.month - 1]
            
            elif input_date.day < nones.day - 1:
                day = "a.d. " + int_to_roman(abs(nones_delta.days) + 1) + " Nōn. " + months_abbr[input_date.month - 1]
            elif input_date.day == nones.day - 1:
                day = "prīd. Nōn. " + months_abbr[input_date.month - 1]
            elif input_date.day == nones.day:
                day = "Nōn. " + months_abbr[input_date.month - 1]
            
            elif input_date.day < ides.day - 1:
                day = "a.d. " + int_to_roman(abs(ides_delta.days) + 1) + " Īd. " + months_abbr[input_date.month - 1]
            elif input_date.day == ides.day - 1:
                day = "prīd. Īd. " + months_abbr[input_date.month - 1]
            elif input_date.day == ides.day:
                day = "Īd. " + months_abbr[input_date.month - 1]

            # if last day of month (works for leap years!)
            elif input_date.day == calendar.monthrange(input_date.year, input_date.month)[1]:
                if input_date.month == 12:
                    day = "prīd. Kal. " + months_abbr[0]
                else:
                    day = "prīd. Kal. " + months_abbr[input_date.month] 
            
            # loop back to January if counting days until next month in December and leap year check
            else:
                if input_date.month == 12:
                    day = "a.d. " + int_to_roman(abs(kalends2_delta.days) + 1) + " Kal. " + months_abbr[0]
                elif input_date.month == 2 and input_date.day == 24:
                    try:
                        # try for leap year
                        input_date.replace(day=29)
                        day = "a.d. bis VI Kal. Mar."
                    except ValueError:
                        # not a leap year
                        day = "a.d. " + int_to_roman(abs(kalends2_delta.days) + 1) + " Kal. " + months_abbr[input_date.month]
                else:
                    day = "a.d. " + int_to_roman(abs(kalends2_delta.days) + 1) + " Kal. " + months_abbr[input_date.month]

        # if the user does not want an idiomatic date:
        # probably a shorter way to do this but ¯\_(ツ)_/¯
        else:
            if input_date.day == 1:
                day = "Kalendīs " + months_abl[input_date.month - 1]
            
            elif input_date.day < nones.day - 1:
                day = "ante diem " + int_to_roman(abs(nones_delta.days) + 1) + " Nōnās " + months_acc[input_date.month - 1]
            elif input_date.day == nones.day - 1:
                day = "prīdiē Nōnās " + months_acc[input_date.month - 1]
            elif input_date.day == nones.day:
                day = "Nōnīs " + months_abl[input_date.month - 1]
            
            elif input_date.day < ides.day - 1:
                day = "ante diem " + int_to_roman(abs(ides_delta.days) + 1) + " Idus " + months_acc[input_date.month - 1]
            elif input_date.day == ides.day - 1:
                day = "prīdiē Idus " + months_acc[input_date.month - 1]
            elif input_date.day == ides.day:
                day = "Īdibus " + months_abl[input_date.month - 1]

            # if last day of month (works for leap years!)
            elif input_date.day == calendar.monthrange(input_date.year, input_date.month)[1]:
                if input_date.month == 12:
                    day = "prīdiē Kalendās " + months_acc[0]
                else:
                    day = "prīdiē Kalendās " + months_acc[input_date.month] 
            
            # loop back to January if counting days until next month in December and leap year check
            else:
                if input_date.month == 12:
                    day = "ante diem " + int_to_roman(abs(kalends2_delta.days) + 1) + " Kalendās " + months_acc[0]
                elif input_date.month == 2 and input_date.day == 24:
                    try:
                        # try for leap year
                        input_date.replace(day=29)
                        day = "ante diem bis VI Kalendās Martiās"
                    except ValueError:
                        # not a leap year
                        day = "ante diem " + int_to_roman(abs(kalends2_delta.days) + 1) + " Kalendās " + months_abbr[input_date.month]
                else:
                    day = "ante diem " + int_to_roman(abs(kalends2_delta.days) + 1) + " Kalendās " + months_acc[input_date.month]
        
        if macron_pref:
            return remove_macrons(day)
        else:
            return day
    else:
        logger.error("Input date was not a datetime.datetime object or idiomatic was not a boolean")

def get_time(input_date, macron_pref):
    # get sunrise/sunset from internet, then work out length of hour

    if isinstance(input_date, datetime.datetime):
        # cache data for a whole day, then get new data when day changes
        if not os.path.exists(os.path.join(start_dir, "cache")):
            os.mkdir(os.path.join(start_dir, "cache"))
        try:
            logger.debug("Checking if today's data is cached")
            with open(os.path.join(start_dir, "cache", "sunrisesunset-" + input_date.strftime("%Y%m%d") + ".json"), "r", encoding="utf-8") as response:
                data = response.read()
                jsondata = json.loads(data)
        except:
            try:
                # requests the data for the current day of timezone - ISO 8601 format
                # TODO do not hardcode location - currently London
                logger.debug("Getting data from internet")
                response = urllib.request.urlopen("https://api.sunrise-sunset.org/json?lat=51.509865&lng=-0.118092&formatted=0&date=" + input_date.strftime("%Y-%m-%d"))
                logger.debug("Writing data to file")
                with open(os.path.join(start_dir, "cache", "sunrisesunset-" + input_date.strftime("%Y%m%d") + ".json"), "w", encoding="utf-8") as outfile:
                    data = response.read().decode("utf-8")
                    jsondata = json.loads(data)
                    json.dump(jsondata, outfile)
            except:
                try:
                    logger.debug("Trying to open yesterday's sunrise/set data since network probably down")
                    yesterday = input_date - datetime.timedelta(days=1)
                    with open(os.path.join(start_dir, "cache", "sunrisesunset-" + yesterday.strftime("%Y%m%d") + ".json"), "r", encoding="utf-8") as response:
                        data = response.read()
                        jsondata = json.loads(data)
                except:
                    logger.debug("No internet access and no fallback data files")
                    logger.info("No internet access and no fallback data files, program exiting...")
                    exit()

        sunrise = datetime.datetime.fromisoformat(jsondata["results"]["sunrise"])
        local_timezone = datetime.datetime.now().astimezone().tzinfo
        sunrise = sunrise.astimezone(local_timezone)

        sunset = datetime.datetime.fromisoformat(jsondata["results"]["sunset"])
        local_timezone = datetime.datetime.now().astimezone().tzinfo
        sunset = sunset.astimezone(local_timezone)

        input_date = input_date.replace(tzinfo=local_timezone)
        logger.debug(f"\n Input date: {input_date}\n Sunrise:    {sunrise}\n Sunset:     {sunset}")

        day_duration = sunset - sunrise
        hour_length = day_duration/12
        midday = sunrise + (day_duration/2)
        morning_portion = input_date - sunrise
        afternoon_portion = sunset - input_date
        logger.debug(f"\n Hour length:      {hour_length}\n Midday:           {midday}\n Morning length:   {morning_portion}\n Afternoon length: {afternoon_portion}")

        if input_date < sunrise:
            hour = int_to_roman(math.floor(abs(morning_portion/hour_length)) + 1)
            time = "hōra " + hour + " ante sōlis ortum"
        elif input_date == sunrise:
            time = "sōlis ortus"
        elif input_date < midday:
            hour = int_to_roman(math.floor(morning_portion/hour_length) + 1)
            time = "hōra " + hour + " post sōlis ortum"
        elif input_date == midday:
            time = "merīdiēs"
        elif input_date < sunset:
            hour = int_to_roman(math.floor(afternoon_portion/hour_length) + 1)
            time = "hōra " + hour + " ante sōlis occasum"
        elif input_date == sunset:
            time = "sōlis occasus"
        elif input_date > sunset:
            hour = int_to_roman(math.floor(abs(afternoon_portion/hour_length)) + 1)
            time = "hōra " + hour + " post sōlis occasum"
        
        if macron_pref:
            return remove_macrons(time)
        else:
            return time
    else:
        logger.error("Input date was not a datetime.datetime object")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts dates and times into a Roman format")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--json", help="output in JSON for portability", action="store_true")
    group.add_argument("--simple", help="only print the Roman format", action="store_true")
    parser.add_argument("--idiomatic", help="abbreviated dates to be more idiomatic", action="store_true")
    parser.add_argument("--no-macrons", help="print without any long vowel marks", action="store_true")
    parser.add_argument("--custom", help="convert a custom date e.g. 2000-01-23 (ISO 8601)")
    parser.add_argument("--debug", help="print calculations etc. for debugging", action="store_true")
    args = parser.parse_args()

    input_date = datetime.datetime.now()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.idiomatic:
        idiom_pref = True
    else:
        idiom_pref = False
    
    if args.no_macrons:
        macron_pref = True
    else:
        macron_pref = False

    if args.custom:
        # TODO custom time not supported
        try:
            input_date = datetime.datetime.fromisoformat(args.custom)
        except:
            # TODO dates before AD 1 (i.e. 1 BC and earlier) are refused
            # TODO dates after 9999-12-13 are not supported by the datetime library :(
            logger.error("Custom date not in ISO 8601 format")
            sys.exit()

    if args.json:
        if args.idiomatic:
            logger.warning("JSON output already contains the idiomatic date")
        print(json.dumps({
                    "normal": {
                        "time": input_date.strftime("%H:%M"),
                        "day": input_date.strftime("%A"),
                        "date": input_date.strftime(f"{input_date.day} %B"),
                        "year": input_date.strftime("%Y")
                    },
                    "roman": {
                        "time": get_time(input_date, macron_pref),
                        "day": get_day(input_date, macron_pref),
                        "date": get_date(input_date, macron_pref, idiomatic=False),
                        "idiomatic_date": get_date(input_date, macron_pref, idiomatic=True),
                        "year": get_year(input_date)
                    }
                }, ensure_ascii=False))
    else:
        if args.simple and args.custom:
            print(get_day(input_date, macron_pref) + "\n" + get_date(input_date, macron_pref, idiom_pref) + "\n" + get_year(input_date) + " AUC")
        elif args.custom:
            # only print out date without time, because custom time not done yet
            print(input_date.strftime(f"%A, {input_date.day} %B %Y AD"))
            print(get_day(input_date, macron_pref) + "\n" + get_date(input_date, macron_pref, idiom_pref) + "\n" + get_year(input_date) + " AUC")
        elif args.simple:
            print(get_time(input_date, macron_pref) + "\n" + get_day(input_date, macron_pref) + "\n" + get_date(input_date, macron_pref, idiom_pref) + "\n" + get_year(input_date) + " AUC")
        else:
            print(input_date.strftime(f"%H:%M, %A, {input_date.day} %B %Y AD"))
            print(get_time(input_date, macron_pref) + "\n" + get_day(input_date, macron_pref) + "\n" + get_date(input_date, macron_pref, idiom_pref) + "\n" + get_year(input_date) + " AUC")
