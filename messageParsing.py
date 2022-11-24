from datetime import datetime, timedelta, date

import re
import calendar


class WorkingObjectClass:

    def __init__(
            self,
            message="",
            subject="",
            parentTask="To Do",
            time="",
            priority="",
            info="",
            body=""):
        self.message = message
        self.subject = subject
        self.parentTask = parentTask
        self.time = time
        self.priority = priority
        self.info = info
        self.body = body


def parse(message: str):
    # Init Output Object
    WorkingObject = WorkingObjectClass(message=message.lower())

    # Check for Key Phrases
    def keyphraseCheck():

        if "on the way home" in WorkingObject.message:
            WorkingObject.priority = "WAYH"
            WorkingObject.message = WorkingObject.message.replace("on the way home", '')
            WorkingObject.subject = WorkingObject.message

        if "overtime" in WorkingObject.message:
            WorkingObject.priority = "OT"
            WorkingObject.message = WorkingObject.message.replace("overtime ", '')
            WorkingObject.subject = "Overtime"
            WorkingObject.info = WorkingObject.message

        if "today" in WorkingObject.message:
            WorkingObject.time = str(date.today())
            WorkingObject.message = WorkingObject.message.replace("today", '')

        if "tomorrow" in WorkingObject.message:
            tomorrowDate = date.today() + timedelta(days=1)
            WorkingObject.time = str(tomorrowDate)
            WorkingObject.message = WorkingObject.message.replace("tomorrow", '')

        DaysOfTheWeek = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5,
                         'sunday': 6}

        for DayOfWeek in DaysOfTheWeek:
            dayAsInt = DaysOfTheWeek[DayOfWeek]

            if DayOfWeek in WorkingObject.message:
                DayAsObject = datetime.today()
                DayAsObject += timedelta(1)

                while DayAsObject.weekday() != dayAsInt:
                    DayAsObject += timedelta(1)

                WorkingObject.time = datetime.strftime(DayAsObject.date(), "%m/%d/%Y")
                WorkingObject.message = re.sub(f"(?:{DayOfWeek}|next {DayOfWeek})", "", WorkingObject.message)

    # Assemble the Body of the outgoing Message
    def assembleMessage():
        if WorkingObject.parentTask != "":
            WorkingObject.body = WorkingObject.body + f"[# {WorkingObject.parentTask}]"
        if WorkingObject.priority != "":
            WorkingObject.body = WorkingObject.body + f"[/ {WorkingObject.priority}]"
        if WorkingObject.info != "":
            WorkingObject.body = WorkingObject.body + f" {WorkingObject.info}"
        if WorkingObject.time != "":
            WorkingObject.body = WorkingObject.body + f" {WorkingObject.time}"

        WorkingObject.subject = WorkingObject.message

    keyphraseCheck()
    assembleMessage()

    return WorkingObject


def test():
    email = parse("Mow the lawn wednesday")
    # email = parse("overtime 30 minutes")

    print(f"{email.subject}\n{email.body}")


#test()
