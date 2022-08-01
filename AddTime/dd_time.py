def GetDaysLeft(days):
  if days == 1:
      return "(next day)"
  elif days > 1:
      return f"({days} days later)"
  return ""

def add_time(start, duration, day=False):
    week_days =  ['monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    #starting vars
    DaysLater = 0
    OnlyOneDay = 24
    HalfDay = 12

    StartHour, StartMin = start.split(":")
    StartMin, DayPeriod = StartMin.split(" ")
    HoursDuration, MinutesDuration = duration.split(":")

    #converting data type
    StartHour = int(StartHour)
    StartMin = int(StartMin)  
    HoursDuration = int(HoursDuration)
    MinutesDuration = int(MinutesDuration)
    DayPeriod = DayPeriod.strip().lower()

    TotalOfMins = StartMin + MinutesDuration
    TotalOfHours = StartHour + HoursDuration

    #in case of excess, treat it and convert it
    if TotalOfMins >= 60:
        TotalOfHours += int(TotalOfMins / 60)
        TotalOfMins = int(TotalOfMins % 60)

    if HoursDuration or MinutesDuration:  #true
        if DayPeriod == "pm" and TotalOfHours > HalfDay:
            if TotalOfHours % OnlyOneDay >= 1.0:
                DaysLater += 1

        if TotalOfHours >= HalfDay:
            HoursLeft = TotalOfHours / OnlyOneDay #HourLeft is an integer
            DaysLater += int(HoursLeft)

        TimeTotalHours = TotalOfHours
        while True:
            if TimeTotalHours < HalfDay:
                break
            if TimeTotalHours >= HalfDay:
                if DayPeriod == "am":
                    DayPeriod = "pm"
                elif DayPeriod == "pm":
                    DayPeriod = "am"
                TimeTotalHours -= HalfDay

    HoursRemaining = int(TotalOfHours % HalfDay) or StartHour + 1
    MinutesRemaining = int(TotalOfMins % 60)

    #formatting the results 
    Result = f'{HoursRemaining}:{MinutesRemaining:02} {DayPeriod.upper()}'
    if day: # add day of the week
        day = day.strip().lower()
        WeekDay = int((week_days.index(day) + DaysLater) % 7)
        WeekDayUpdated = week_days[WeekDay]
        Result += f', {WeekDayUpdated.title()} {DaysLater(DaysLater)}'

    else:
        Result = " ".join((Result, GetDaysLeft(DaysLater)))

    return Result.strip()