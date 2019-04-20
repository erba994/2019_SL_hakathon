import urllib.request
import urllib.parse
import ssl
import datetime
import time
import json
from datetime import timedelta


def return_date(userdate=datetime.date.today(), delta=7):
    fromdate = str(userdate.year) + "." + str(userdate.month) + "." + str(userdate.day)
    delta = timedelta(days=delta)
    sumdate = userdate + delta
    todate = str(sumdate.year) + "." + str(sumdate.month) + "." + str(sumdate.day)
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
    return data[0]["id"]

def url_timetable(fromdate, todate, groupo="9531"):
    newurl = "https://www.hse.ru/api/timetable/lessons" + "?fromdate=" + fromdate + "&todate=" + todate + "&groupoid=" + groupo + "&receiverType=3"
    return newurl


def access_site(url):
    user_agent = "Mozilla/5.0"
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    doc = urllib.request.urlopen(req)
    time.sleep(3)
    data = json.loads(doc.read().decode('utf8'))
    return data


if __name__ == "__main__":
    fromdate, todate = return_date()
    tree = access_site(url_timetable(fromdate, todate))

