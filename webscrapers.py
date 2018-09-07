from arsenal_web import *
from calendar import monthrange
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from event import Event
from organization import Organization
import timestring

keywords = ["Free food", " food ", " snacks ", " coffee ", " donut ", " pizza ", "ice cream", "lunch", " dinner ", " brunch ", " dine ", "brain freeze"]
def getCSDepartment():

    ORG_NAME = "Computer Science"
    URLs = find_links("https://apps.cs.utexas.edu/calendar/", "colorbox-load")
    events = []
    print URLs
    for URL in URLs:
        event = {}
        URL = "https://apps.cs.utexas.edu" + URL
        webPage = get_soup(URL)
        name = webPage.find(attrs={'class': "page__title title"}).text

        for container in webPage.find_all(attrs={'class': "field-item even"}):
            if container.find(attrs={'class': "date-display-single"}):
                date = container.text

            elif container.text.find("Room:") >= 0:
                location = container.text

            elif container.has_attr('property'):
                description = container.text

        print name
        print date
        print location
        print URL
        print description
        event['name'] = name
        event['datetime'] = str(timestring.Date(date))
        event['location'] = location
        event['hyperlink'] = URL
        event['description'] = description
        event['event_id'] = 0
        event['org_name'] = ORG_NAME
        event['verified'] = 1

        triggered = False
        for keyword in keywords:
            if event['description'].find(keyword) >= 0 and not triggered:
                    events.append(event)
                    triggered = True
                    print URL
                    print "\n"

    return events

def getCNSDepartment():

    ORG_NAME = "College of Natural Sciences"
    events = []

    for month in ["10", "11", "12"]:            # data for october, november, december
        URLs = find_links("https://cns.utexas.edu/events/month.calendar/2017/" + month, "cal_titlelink")

        for URL in URLs:
            event = {}
            URL = "https://cns.utexas.edu/" + URL
            webPage = get_soup(URL)


            name = webPage.find(attrs={'class': "jev_evdt_title"}).text
            date = webPage.find(attrs={'class': "jev_evdt_summary"}).text.split("Previous")[0].strip()
            location = webPage.find(attrs={'class': "jev_evdt_location"}).text
            description = webPage.find(attrs={'class': "jev_evdt_desc"}).text

            event['name'] = name
            event['datetime'] = str(timestring.Date(date))
            event['location'] = location
            event['hyperlink'] = URL
            event['description'] = description
            event['event_id'] = 0
            event['org_name'] = ORG_NAME
            event['verified'] = 1

            triggered = False
            for keyword in keywords:
                if event['description'].find(keyword) >= 0 and not triggered:
                    events.append(event)
                    triggered = True
                    print URL
                    print "\n"

    return events

def getUT():

    ORG_NAME = "UT Campus"
    events = []
    for month in ["10", "11", "12"]:            # data for october, november, december
        for day in range(1, monthrange(2017, int(month))[1]+1):
            URLs = find_links("https://calendar.utexas.edu/calendar/day/2017/" + month + "/" + str(day) + "?hide_recurring=1", "summary")

            for URL in URLs:
                event = {}
                webPage = get_soup(URL)

                name = " ".join(webPage.find(attrs={'class': "summary"}).text.strip().split())
                date = " ".join(webPage.find(attrs={'class': "dateright"}).text.strip().split())
                location = " ".join(webPage.find(attrs={'class': "location"}).text.strip().split())
                description = " ".join(webPage.find(attrs={'class': "description"}).text.strip().split())

                event['name'] = name
                event['datetime'] = str(timestring.Date(date))
                event['location'] = location
                event['hyperlink'] = URL
                event['description'] = description
                event['event_id'] = 0
                event['org_name'] = ORG_NAME
                event['verified'] = 1
                triggered = False
                for keyword in keywords:
                    if event['description'].find(keyword) >= 0 and not triggered:
                        events.append(event)
                        triggered = True
                        print URL
                        print "\n"

    return events


def getMcCombsBBA():

    ORG_NAME = "McCombs - BBA"
    URL = "https://my.mccombs.utexas.edu/BBA/Calendar"
    webPage = get_soup(URL)
    events = webPage.find_all(attrs={'class': "calendar-event-wrapper"})
    month = webPage.find_all(attrs={'class': "calendar-month"})
    monthIndex = 0
    events_list = []

    for event in events:

        eventDict = {}
        try:
            event.find(attrs={'class': "calendar-event-date"}).text

            #date
            date = event.find(attrs={'class': "calendar-event-date"}).text
            list = date.split(",")
            if date.find(" 1st") >= 0:                      # new month
                monthIndex += 1
            date = month[monthIndex].text[:-5] + list[1] + " " + event.find(attrs={'class': "calendar-event-time"}).text.split(",")[0]

            #name
            name = event.find(attrs={'class': "calendar-event-title"}).text

            #location
            location = event.find(attrs={'class': "calendar-event-time"}).text
            list = location.split(",")
            location = list[len(list)-1].strip()

            #description
            description = event.find(attrs={'class': "calendar-event-description"}).text.strip()

        except:
            #date is already defined

            #name
            name = event.find(attrs={'class': "calendar-event-title"}).text

            #location
            location = event.find(attrs={'class': "calendar-event-time"}).text
            list = location.split(",")
            location = list[len(list)-1].strip()

            #description
            description = event.find(attrs={'class': "calendar-event-description"}).text.strip()

        eventDict['name'] = name
        eventDict['datetime'] = str(timestring.Date(date))
        eventDict['location'] = location
        eventDict['hyperlink'] = URL
        eventDict['description'] = description
        eventDict['event_id'] = 0
        eventDict['org_name'] = ORG_NAME
        eventDict['verified'] = 1

        triggered = False
        for keyword in keywords:
            if eventDict['description'].find(keyword) >= 0 and not triggered:
                    events_list.append(eventDict)
                    triggered = True
                    print URL
                    print "\n"


    return events_list

def getMcCombsGeneral():

    ORG_NAME = "McCombs - General"
    URL = "https://www.mccombs.utexas.edu/calendars"
    webPage = get_soup(URL)
    events = webPage.find_all(attrs={'class': "calendar-event"})
    events_list = []
    for event in events:
        eventDict = {}
        try:
            URL = event.find('a')['href']
            name = " ".join(event.find(attrs={'class': "calendar-event-title"}).text.strip().split())
            description = " ".join(event.find(attrs={'class': "calendar-event-description"}).text.strip().split())
            date = " ".join(event.find(attrs={'class': "time-div"}).text.strip().split())

            webPage = get_soup(URL)

            try:
                location = " ".join(webPage.find(attrs={'class': "venue-address address inline"}).text.strip().split())
                eventDict['name'] = name
                eventDict['datetime'] = str(timestring.Date(date))
                eventDict['location'] = location
                eventDict['hyperlink'] = URL
                eventDict['description'] = description
                eventDict['event_id'] = 0
                eventDict['org_name'] = ORG_NAME
                eventDict['verified'] = 1
                triggered = False
                for keyword in keywords:
                    if eventDict['description'].find(keyword) >= 0 and not triggered:
                        events_list.append(eventDict)
                        triggered = True
                        print URL
                        print "\n"

            except:
                try:
                    location = " ".join(webPage.find(attrs={'class': "address inline"}).text.strip().split())
                    eventDict['name'] = name
                    eventDict['datetime'] = str(timestring.Date(date))
                    eventDict['location'] = location
                    eventDict['hyperlink'] = URL
                    eventDict['description'] = description
                    eventDict['event_id'] = 0
                    eventDict['org_name'] = ORG_NAME
                    eventDict['verified'] = 1
                    triggered = False
                    for keyword in keywords:
                        if eventDict['description'].find(keyword) >= 0 and not triggered:
                            events_list.append(eventDict)
                            triggered = True
                            print URL
                            print "\n"

                except:
                    continue

        except:
            continue

    return events_list

def getLibrary():

    ORG_NAME = "UT Library"
    events = []

    for month in ["10", "11", "12"]:  # data for october, november, december
        URLs = find_links("http://www.lib.utexas.edu/calendar/month/2017-" + month, "single-day future")

        for URL in URLs:
            event = {}
            URL = "http://www.lib.utexas.edu" + URL
            webPage = get_soup(URL)
            name = webPage.find(attrs={'class': "title"}).text.strip()
            date = webPage.find(attrs={'class': "date-display-single"}).text.strip()
            location = webPage.find(attrs={'class': "field field-name-field-cal-event-location field-type-list-text field-label-hidden"}).text.strip()
            description = webPage.find(attrs={'class': "field field-name-field-cal-event-description field-type-text-long field-label-hidden"}).text.strip()

            event['name'] = name
            event['datetime'] = str(timestring.Date(date))
            event['location'] = location
            event['hyperlink'] = URL
            event['description'] = description
            event['event_id'] = 0
            event['org_name'] = ORG_NAME
            event['verified'] = 1
            triggered = False
            for keyword in keywords:
                if event['description'].find(keyword) >= 0 and not triggered:
                    events.append(event)
                    triggered = True
                    print URL
                    print "\n"

    return events

def getHornsLink():

    ORG_NAME = "Student Organizations"
    webPage = BeautifulSoup(urllib2.urlopen("https://utexas.campuslabs.com/engage/events/events.rss"), 'xml')
    URLs = webPage.find_all('link')
    browser = webdriver.PhantomJS()
    events = []

    for URL in URLs[1:]:
        event = {}
        URL = URL.text
        browser.get(URL)

        element_present = EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Google'))
        WebDriverWait(browser, 5).until(element_present)

        HTML = browser.page_source
        webPage = BeautifulSoup(HTML, 'html.parser')

        if webPage.prettify().find("Free Food") >= 0:
            name = webPage.title.string

            for header in webPage.find_all('h2'):
                if header.text.find('Date and Time') >= 0:
                    date = header.find_next_sibling('p').text.strip()
                elif header.text.find('Location') >= 0:
                    location = header.find_next_sibling('div').text.strip()

            description = " ".join(webPage.find(attrs={'class': "DescriptionText"}).text.strip().split())

            event['name'] = name
            event['datetime'] = str(timestring.Date(date))
            event['location'] = location
            event['hyperlink'] = URL
            event['description'] = description
            event['event_id'] = 0
            event['org_name'] = ORG_NAME
            event['verified'] = 1
            events.append(event)
            print URL
            print "\n"

    return events

getCSDepartment()
