import dateutil
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher

import requests
import json
import datetime
from pytz import timezone

token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6ImFjY2VzcyJ9.eyJhY2NvdW50SWQiOiI1YzYyYzIxMDNkZjgyYzAwMTlkNzI4ZGQiLCJ1c2VySWQiOiI1YzYyYzFlOTZiNjFhOTAwMTcxY2Y5OTQiLCJpYXQiOjE1NzM2NDExMTMsImV4cCI6MTU3NjIzMzExMywiYXVkIjoiaHR0cHM6Ly9zY2h1bC1jbG91ZC5vcmciLCJpc3MiOiJmZWF0aGVycyIsInN1YiI6IjVjNjJjMjEwM2RmODJjMDAxOWQ3MjhkZCIsImp0aSI6ImM2MzZmZTBlLWU0MTMtNDcxZS1iY2Q4LTVhMGMwYTc3M2QxYyJ9.OqKuxPKYki-lFWdMO5uorwJJ14T19ybFfCme_LmG9P8"


class GetFirstLesson(Action):
    def name(self) -> Text:
        return "action_first-lesson"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        weekdayMapping = {
            0: "MO",
            1: "TU",
            2: "WE",
            3: "TH",
            4: "FR",
            5: "SA",
            6: "SO"
        }

        r = requests.get('https://api.schul-cloud.org/calendar?all=true', headers={"content-type": "application/json",
                                                                                   "Authorization": token})
        status = r.status_code
        print(status)
        if status == 200:
            response = json.loads(r.content)
            print(response)
            weekday = datetime.datetime.today().weekday()
            weekdayShort = weekdayMapping[weekday]
            # weekdayShort = "WE"  # hardcoded for testing reasons

            currentEarliestLesson = None
            currentEarliestLessonStartingTime = None
            currentRoom = None

            for lesson in response:
                if lesson['title'] == 'Blubas':
                    continue
                subjectWeekday = lesson['included'][0]['attributes']['wkst']
                if subjectWeekday == weekdayShort:
                    startingDate = lesson['attributes']['dtstart']
                    startTime = datetime.datetime.strptime(
                        startingDate, "%Y-%m-%dT%H:%M:%S.000Z").time()

            if (currentEarliestLesson == None) or (currentEarliestLessonStartingTime > startTime):
                currentEarliestLesson = lesson
                currentEarliestLessonStartingTime = startTime
                currentRoom = lesson['attributes']['location']

                if currentEarliestLesson == None:
                    dispatcher.utter_message('Heute findet kein Unterricht statt.')
                    return []
                else:
                    timestampStr = currentEarliestLessonStartingTime.strftime("%H:%M")
                    dispatcher.utter_message(
                        'Deine erste Stunde heute ist ' + currentEarliestLesson['title'] + ' um ' + str(
                            timestampStr) + ' im Raum ' + currentRoom + '.')
                    return []
            else:
                return []


class GetNews(Action):
    def name(self):
        return "action_get-news"

    def run(self, dispatcher, tracker, domain):

        r = requests.get('https://api.schul-cloud.org/news', headers={"content-type": "application/json",
                                                                      "Authorization": token})
        status = r.status_code
        if status == 200:
            response = json.loads(r.content)
            mostRecentNews = response['data'][::-1]
            if len(mostRecentNews) > 0:
                mostRecentNews1 = mostRecentNews[0]['title']
                mostRecentNews2 = mostRecentNews[1]['title']
                mostRecentNews3 = mostRecentNews[2]['title']

                dispatcher.utter_message(
                    'Die drei aktuellsten Neuigkeiten aus der Schule sind: \n (1) ' + mostRecentNews1
                    + '\n (2) ' + mostRecentNews2 + '\n (3) ' + mostRecentNews3 + '.')
                return []
            else:
                dispatcher.utter_message('Es gibt keine aktuellen Neuigkeiten.')
                return []
        else:
            return []


class GetNewsDetails(Action):
    def name(self):
        return "action_get-news-details"

    def run(self, dispatcher, tracker, domain):

        r = requests.get('https://api.schul-cloud.org/news', headers={"content-type": "application/json",
                                                                      "Authorization": token})
        status = r.status_code
        if status == 200:
            response = json.loads(r.content)
            # mostRecentNews = response['data'][::-1]
            topic = tracker.get_slot('news-topic')
            print(str(topic))
            dispatcher.utter_message('Die Neuigkeiten sind: ')
            return []
        else:
            return []


class GetNextLesson(Action):
    def name(self):
        return "action_next-lesson"

    def run(self, dispatcher, tracker, domain):
        weekdayMapping = {
            0: "MO",
            1: "TU",
            2: "WE",
            3: "TH",
            4: "FR",
            5: "SA",
            6: "SO"
        }

        r = requests.get('https://api.schul-cloud.org/calendar?all=true', headers={"content-type": "application/json",
                                                                                   "Authorization": token})
        status = r.status_code
        if status == 200:
            response = json.loads(r.content)
            weekday = datetime.datetime.today().weekday()
            # weekdayShort = weekdayMapping[weekday]
            weekdayShort = "WE"  # hardcoded for testing reasons

            currentEarliestLesson = None
            currentEarliestLessonStartingTime = None
            now = datetime.datetime.now()
            amsterdam = timezone('Europe/Amsterdam')
            now = now.astimezone(amsterdam).time()

            for lesson in response:
                if lesson['title'] == 'Blubas':
                    continue
                subjectWeekday = lesson['included'][0]['attributes']['wkst']
                if subjectWeekday == weekdayShort:
                    startingDate = lesson['attributes']['dtstart']
                    startTime = datetime.datetime.strptime(
                        startingDate, "%Y-%m-%dT%H:%M:%S.000Z").time()

                if startTime > now:
                    if (currentEarliestLesson == None) or (currentEarliestLessonStartingTime > startTime):
                        currentEarliestLesson = lesson
                        currentEarliestLessonStartingTime = startTime

                if currentEarliestLesson == None:
                    dispatcher.utter_message('Heute findet kein Unterricht (mehr) statt.')
                    return []
                else:
                    timestampStr = currentEarliestLessonStartingTime.strftime("%H:%M")
                    dispatcher.utter_message('Deine nächste Stunde ist ' +
                                             currentEarliestLesson['title'] + ' um ' + str(timestampStr))
                    subjectToSave = currentEarliestLesson['title'].lower().split(' ')
                    return [SlotSet('subject', subjectToSave[0])]
        else:
            return []


class GetSchoolEnd(Action):
    def name(self):
        return "action_school-ends"

    def run(self, dispatcher, tracker, domain):
        weekdayMapping = {
            0: "MO",
            1: "TU",
            2: "WE",
            3: "TH",
            4: "FR",
            5: "SA",
            6: "SO"
        }

        r = requests.get('https://api.schul-cloud.org/calendar?all=true', headers={"content-type": "application/json",
                                                                                   "Authorization": token})
        status = r.status_code
        print(r.status_code)
        print(r.headers)
        if status == 200:
            response = json.loads(r.content)
            weekday = datetime.datetime.today().weekday()
            # weekdayShort = weekdayMapping[weekday]
            weekdayShort = "WE"  # hardcoded for testing reasons

            currentLastLesson = None
            currentLastestEndingTime = None

            for lesson in response:
                if lesson['title'] == 'Blubas':
                    continue
                subjectWeekday = lesson['included'][0]['attributes']['wkst']
                if subjectWeekday == weekdayShort:
                    endDate = lesson['attributes']['dtend']
                    endTime = datetime.datetime.strptime(
                        endDate, "%Y-%m-%dT%H:%M:%S.000Z").time()

                    if (currentLastLesson == None) or (currentLastestEndingTime < endTime):
                        currentLastLesson = lesson
                        currentLastestEndingTime = endTime

            if currentLastLesson == None:
                dispatcher.utter_message('Heute hast du keine Schule.')
                return []
            else:
                timestampStr = currentLastestEndingTime.strftime("%H:%M")
                dispatcher.utter_message('Die Schuld endet heute um ' + str(timestampStr) + '.')
                return []
        else:
            return []


class GetLessonRoom(Action):
    def name(self):
        return "action_get-lesson-room"

    def run(self, dispatcher, tracker, domain):
        weekdayMapping = {
            0: "MO",
            1: "TU",
            2: "WE",
            3: "TH",
            4: "FR",
            5: "SA",
            6: "SO"
        }
        currentSubject = tracker.get_slot("subject")
        subjectExists = False

        r = requests.get('https://api.schul-cloud.org/calendar?all=true', headers={"content-type": "application/json",
                                                                                   "Authorization": token})
        status = r.status_code
        if status == 200:
            response = json.loads(r.content)
            weekday = datetime.datetime.today().weekday()
            # weekdayShort = weekdayMapping[weekday]
            weekdayShort = "WE"  # hardcoded for testing reasons

            for lesson in response:
                if currentSubject in lesson['title'].lower():
                    subjectExists = True
                    subjectWeekday = lesson['included'][0]['attributes']['wkst']
                    if subjectWeekday == weekdayShort:
                        location = lesson['attributes']['location']
                        dispatcher.utter_message(
                            currentSubject.capitalize() + ' findet im Raum ' + location + ' statt.')
                        return []
            if (subjectExists):
                dispatcher.utter_message(currentSubject.capitalize() + ' findet heute nicht statt.')
                return []
            else:
                dispatcher.utter_message(currentSubject.capitalize() + ' ist kein bekanntes Unterrichtsfach.')
                return []
        else:
            return []


class GetLessonTimeEnd(Action):
    def name(self):
        return "action_get_lesson_time_end"

    def run(self, dispatcher, tracker, domain):
        weekdayMapping = {
            0: "MO",
            1: "TU",
            2: "WE",
            3: "TH",
            4: "FR",
            5: "SA",
            6: "SO"
        }
        currentSubject = tracker.get_slot("subject")
        subjectExists = False

        r = requests.get('https://api.schul-cloud.org/calendar?all=true', headers={"content-type": "application/json",
                                                                                   "Authorization": token})
        status = r.status_code
        if status == 200:
            response = json.loads(r.content)
            weekday = datetime.datetime.today().weekday()
            # weekdayShort = weekdayMapping[weekday]
            weekdayShort = "WE"  # hardcoded for testing reasons

            for lesson in response:
                if currentSubject in lesson['title'].lower():
                    subjectExists = True
                    subjectWeekday = lesson['included'][0]['attributes']['wkst']
                    if subjectWeekday == weekdayShort:
                        startingDate = lesson['attributes']['dtend']
                        startTime = datetime.datetime.strptime(
                            startingDate, "%Y-%m-%dT%H:%M:%S.000Z")

                        timestampStr = startTime.strftime("%H:%M")

                        dispatcher.utter_message(currentSubject.capitalize(
                        ) + ' endet um ' + str(timestampStr) + '.')

                        return []
            if (subjectExists):
                dispatcher.utter_message(
                    currentSubject.capitalize() + ' findet heute nicht statt.')
                return []
            else:
                dispatcher.utter_message(
                    currentSubject.capitalize() + ' ist kein bekanntes Unterrichtsfach.')
                return []
        else:
            dispatcher.utter_message('some error occured' + str(status))
            return []


class GetLessonTimeStart(Action):
    def name(self):
        return "action_get_lesson_time_start"

    def run(self, dispatcher, tracker, domain):
        weekdayMapping = {
            0: "MO",
            1: "TU",
            2: "WE",
            3: "TH",
            4: "FR",
            5: "SA",
            6: "SO"
        }
        currentSubject = tracker.get_slot("subject")
        subjectExists = False

        r = requests.get('https://api.schul-cloud.org/calendar?all=true', headers={"content-type": "application/json",
                                                                                   "Authorization": token})
        status = r.status_code
        if status == 200:
            response = json.loads(r.content)
            weekday = datetime.datetime.today().weekday()
            # weekdayShort = weekdayMapping[weekday]
            weekdayShort = "WE"  # hardcoded for testing reasons

            for lesson in response:
                if currentSubject in lesson['title'].lower():
                    subjectExists = True
                    subjectWeekday = lesson['included'][0]['attributes']['wkst']
                    if subjectWeekday == weekdayShort:
                        startingDate = lesson['attributes']['dtstart']
                        startTime = datetime.datetime.strptime(
                            startingDate, "%Y-%m-%dT%H:%M:%S.000Z")

                        timestampStr = startTime.strftime("%H:%M")

                        dispatcher.utter_message(currentSubject.capitalize(
                        ) + ' findet um ' + str(timestampStr) + ' statt.')

                        return []
            if (subjectExists):
                dispatcher.utter_message(
                    currentSubject.capitalize() + ' findet heute nicht statt.')
                return []
            else:
                dispatcher.utter_message(
                    currentSubject.capitalize() + ' ist kein bekanntes Unterrichtsfach.')
                return []
        else:
            return []


class SubjectSet(Action):
    def name(self):
        return "action_subject-set"

    def run(self, dispatcher, tracker, domain):
        subject = tracker.get_slot('subject')
        if subject:
            return [SlotSet('subject-set', True)]
        else:
            return [SlotSet('subject-set', False)]


class ActionCheckStatus(Action):
    def name(self):
        return "action_check_status"

    def run(self, dispatcher, tracker, domain):
        r = requests.get('https://api.schul-cloud.org/calendar', headers={"content-type": "application/json",
                                                                          "Authorization": token})
        status = r.status_code
        print(r.status_code)
        print(r.headers)
        if status == 200:
            response = json.loads(r.content)
            starttime = dateutil.parser.parse(response[0]['attributes']['dtstart'])

            print(starttime)
            dispatcher.utter_message(
                response[0]['attributes']['summary'] + ' um ' + starttime.strftime('%H:%M'))
        else:
            dispatcher.utter_message("some error occured")
            return []
