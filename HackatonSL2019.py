import urllib.request
import urllib.parse
import ssl
import datetime
import json
from datetime import timedelta
from dateutil import parser


def read_fromdate(date):
    try:
        return parser.parse(date)
    except:
        return datetime.date.today()


def read_todate(date, fromdate):
    try:
        return parser.parse(date)
    except:
        return fromdate + timedelta(days=7)


def return_date(fromdate, todate):
    fromdate = str(fromdate.year) + "." + str("{:0>2d}".format(fromdate.month)) + "." + str("{:0>2d}".format(fromdate.day))
    todate = str(todate.year) + "." + str("{:0>2d}".format(todate.month)) + "." + str("{:0>2d}".format(todate.day))
    return fromdate, todate


def find_person(surname, name, patronimic = ""):
    surname = urllib.parse.quote_plus(surname)
    name = urllib.parse.quote_plus(name)
    patronimic = urllib.parse.quote_plus(patronimic)
    if patronimic == "":
        url = "https://ruz.hse.ru/api/search?term={}%20{}%20&type=student".format(surname, name)
    else:
        url = "https://ruz.hse.ru/api/search?term={}%20{}%20{}%20&type=student".format(surname, name, patronimic)
    user_agent = "Mozilla/5.0"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    doc = urllib.request.urlopen(req, context=ctx)
    data = json.loads(doc.read().decode('utf8'))
    return str(data[0]["id"])


def url_timetable(studid, fromdate, todate, lang="1"):
    url = "https://ruz.hse.ru/api/schedule/student/" + studid + "?start=" + fromdate + "&finish=" + todate + "&lng=" + lang
    user_agent = "Mozilla/5.0"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    doc = urllib.request.urlopen(req, context=ctx)
    data = json.loads(doc.read().decode('utf8'))
    return data


def read_timetable(data):
    if len(data) == 0:
        print("нет пар, отдыхай)")
    else:
        for para in data:
            print(para["date"])
            print(para["beginLesson"] + " - " + para["endLesson"])
            print(para["discipline"])
            print(para["auditorium"] + " - " + para["building"])
            print(para["lecturer"])
            print("------")
            print("------")


if __name__ == "__main__":
    fromdate = read_fromdate("")
    todate = read_todate("", fromdate)
    fromdate, todate = return_date(fromdate, todate)
    studid = find_person("мазур", "екатерина", "сергеевна")
    timetable = url_timetable(studid, fromdate, todate)
    read_timetable(timetable)

