"""ExpressionParser class which is used to parse the cron expression into a human-readable format."""


class ExpressionParser(object):
    """A class to parse the cron expression into a human-readable format.
    Attributes:
        parts (list): The components of the cron expression.
        description (str): The human-readable description of the cron expression.
    """

    def __init__(self, parts):
        """Initialize the ExpressionParser object."""
        self.parts = parts
        self.description = self._describe()

    def _describe(self):
        """Parse the expression into a dictionary of parts"""
        description = ""

        minute, hour, day_of_month, month, day_of_week, year = self.parts

        #print(f"Minute: {minute}\nHour: {hour}\nDay of Month: {day_of_month}\nMonth: {month}\nDay of Week: {day_of_week}")

        time_desc = self._describe_time(minute, hour)
        date_desc = self._describe_date(day_of_month, month, day_of_week)

        if date_desc:
            description = f"{time_desc}, {date_desc}"
        else:
            description = f"{time_desc}"

        if year != "*":
            description += f" {self._describe_field(year, 'year')}"

        if description:
            if len(description) > 1:
                description = description[0].upper() + description[1:].rstrip().lstrip()

        return description

    def _describe_time(self, minute, hour):
        time_desc = ""
        if minute == "*":
            if hour == "*":
                time_desc = "Every minute"
            elif hour.isdigit():
                if hour == "0":
                    time_desc += "Every minute at midnight"
                elif hour == "12":
                    time_desc += " at noon"
                else:
                    time_desc += f", {self._describe_field(hour, 'hour')}"
            return time_desc
        elif minute.isdigit():
            if hour == "*":
                if minute == "0":
                    time_desc = "At the top of the hour"
                elif minute == "15":
                    time_desc = "At quarter past the hour"
                elif minute == "30":
                    time_desc = "At half past the hour"
                elif minute == "45":
                    time_desc = "At quarter to the hour"
                else:
                    time_desc = f"At {minute} minutes past the hour"
                return time_desc
            elif hour.isdigit():
                if minute == "0":
                    if hour == "0":
                        return "At midnight"
                    elif hour == "12":
                        return "At noon"
                    return f"At {self._format_time(hour, '00', True)}"
                else:
                    return f"At {self._format_time(hour, minute)}"
            else:
                return f"At {minute} minutes past {self._describe_field(hour, 'hour')}"
        else:
            if "/" in minute:
                base, step = minute.split("/")
                if base == "*":
                    return f"Every {step} minutes"
                else:
                    last_minute = self._compute_last_minute(int(step))
                    print(f"last_minute: {last_minute}")
                    return f"Every {step} minutes, starting at {self._format_time(hour, 0, True)} until {self._format_time(hour, str(last_minute))}"
            return f"At {self._describe_field(minute, 'minute')} {self._describe_field(hour, 'hour')}"

    def _compute_last_minute(self, step):
        """Compute the last minute within an hour which is the biggest minute value that is a multiple of the step value and less than 60."""
        return (59 // step) * step

    def _describe_date(self, day_of_month, month, day_of_week):
        date_desc = []

        # set day-of-month/week to * if it is ?
        day_of_month = "*" if day_of_month == "?" else day_of_month
        day_of_week = "*" if day_of_week == "?" else day_of_week

        # prune the date description if all fields are *
        if day_of_month == "*" and month == "*" and day_of_week == "*":
            return ""
        else:
            if day_of_month == "*" or day_of_month == "?":
                day_of_month = ""
            if month == "*":
                month = ""
            if day_of_week == "*" or day_of_week == "?":
                day_of_week = ""

        dom_desc = ""
        month_desc = ""
        dow_desc = ""

        # get day of month, month and day of week description
        if day_of_month != "*":  # day of month
            dom_desc = f"{self._describe_day_of_month(day_of_month)}"
            date_desc.append(dom_desc)

        if month != "*":  # month
            month_desc = f"{self._describe_month(month)}"
            date_desc.append(month_desc)

        if day_of_week != "*":  # day of week
            dow_desc = f"{self._describe_day_of_week(day_of_week)}"
            date_desc.append(dow_desc)

        if date_desc:  # combine date descriptions, strip extra spaces
            date_desc = " ".join(date_desc).rstrip().lstrip().replace("  ", " ")

        return date_desc

    def is_complex_field(self, field):
        """Check if the field is a complex field."""
        return "/" in field or "-" in field or "," in field or "#" in field

    def _describe_field(self, field, field_type):
        # print(f"field: {field} field_type: {field_type}")
        if "/" in field:  # step value
            base, step = field.split("/")
            suffix = "s" if step != "1" else ""
            print(f"field_type: {field_type}={field}")
            if base == "*":
                return f"every {step} {field_type}{suffix}"
            else:
                print(f"base: {base} step: {step}")
                if field_type == "minute":
                    if base == "0":
                        return f"every {step} minute{suffix} starting at"
                    else:
                        return f"every {step} minute{suffix} starting at {base}"
                elif field_type == "hour":
                    return f"every {step} hour{suffix} starting at {self._format_time(base, '00', True)}"
                elif field_type == "day_of_month":
                    return f"every {step} day{suffix} starting from the {base}"
                else:
                    return f"every {step} starting from {base}"
        elif "-" in field:  # range value
            start, end = field.split("-")
            if field_type == "minute":
                return f"minutes {start} through {end} past the hour"
            elif field_type == "hour":
                return f"{self._format_time(start, '00', True)} to {self._format_time(end, '00', True)}"
            elif field_type == "day_of_month":
                return f"from the {start} to the {end}"
            else:
                return f"from {start} to {end}"
        elif "," in field:  # list value
            if field_type == "minute":
                list_of_minutes = [
                    self._describe_field(minute, "minute")
                    for minute in field.split(",")
                ]
                last_minute = list_of_minutes.pop()
                return f"{', '.join(list_of_minutes)} and {last_minute}"
            elif field_type == "hour":
                list_of_hours = [
                    self._format_time(hour, "00", True) for hour in field.split(",")
                ]
                last_hour = list_of_hours.pop()
                return f"{', '.join(list_of_hours)} and {last_hour}"
            elif field_type == "day_of_month":
                list_of_days = [self._ordinal_day(day) for day in field.split(",")]
                last_day = list_of_days.pop()
                return f"on {', '.join(list_of_days)} and {last_day} day of the month"
            elif field_type == "day_of_week":
                list_of_days = [
                    self._describe_day_of_week(day) for day in field.split(",")
                ]
                if len(list_of_days) > 1:
                    last_day = list_of_days.pop()

                if len(list_of_days) == 1:
                    return f"{list_of_days[0]} and {last_day}"
                else:
                    return f"{', '.join(list_of_days)} and {last_day}"
            else:
                return ", ".join(field.split(","))
        else:  # single value
            if field.isdigit():  # numeric value
                field = int(field)
                if field_type == "minute":
                    return f"{field} minutes past the hour"
                elif field_type == "hour":
                    return f"{self._format_time(field, '00')}"
                elif field_type == "day_of_month":
                    return f"on {self._ordinal_day(field)} day of the month"
                elif field_type == "month":
                    return self._describe_month(field)
                elif field_type == "day_of_week":
                    return self._describe_day_of_week(field)
                elif field_type == "year":
                    return f"during year of {field}"
            else:  # string value
                if field_type == "minute":
                    return f"{field} minutes past the hour"
                elif field_type == "hour":
                    return f"{self._format_time(field, '00')}"
                elif field_type == "day_of_month":
                    if field.isdigit():
                        return f"{self._ordinal_day(field)} day of the month"
                    else:
                        if field == "L":
                            return "the last day of the month"
                        elif field == "LW":
                            return "the last weekday of the month"
                        elif "L-" in field:
                            day = field.replace("L-", "")
                            return f"the last {self._ordinal_day(day)} of every month"
                        else:
                            return ""
                elif field_type == "month":
                    return self._describe_month(field)
                elif field_type == "day_of_week":
                    return self._describe_day_of_week(field)
            return ""

    def _describe_day_of_month(self, field):
        return self._describe_field(field, "day_of_month")

    def _describe_day_of_week(self, field):
        days = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        short_days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        if "," in field:
            list_of_days = field.upper().split(",")
            if list_of_days[0].isdigit():  # check if list is numbers
                list_of_days = [days[int(day)] for day in field.split(",")]
            else:
                list_of_days = [
                    days[short_days.index(day)] for day in field.upper().split(",")
                ]
            last_day = list_of_days.pop()
            return f"{', '.join(list_of_days)} and {last_day}"
        elif "-" in field:
            if field.upper() == "SUN-SAT":
                return "every day of the week"
            elif field.upper() == "MON-FRI":
                return "weekdays"
            elif field.upper() == "SAT-SUN":
                return "weekends"
            else:
                start, end = field.upper().split("-")
                if start.isdigit():
                    return f"{days[int(start)]} through {days[int(end)]}"
                else:
                    return f"{days[short_days.index(start)]} through {days[short_days.index(end)]}"
        elif "#" in field:
            day, week = field.split("#")
            if day.isdigit():
                day_desc = days[int(int(day) - 1)]
                return f"on the {self._ordinal_word(week)} {day_desc} of the month"
            else:
                if week.isdigit():
                    return f"on the {self._ordinal_word(week)} {days[short_days.index(day.upper())]} of the month"
                else:
                    return ""
        else:
            if field.isdigit():
                return f"only on {days[int(field)]}"
            else:
                if field == "L":  # last day of the month
                    return "on the last day of the month"
                elif field == "LW":  # last weekday of the month
                    return "on the last weekday of the month"
                elif "L-" in field:  # last x day of the month
                    num = field.replace("L-", "")
                    if num.isdigit():
                        no = int(num)
                        return f"on the last {days[no-1]} of the month"
                    else:
                        return ""
                elif "L" in field:  # last x day of the month
                    num = field.replace("L", "")
                    if num.isdigit():
                        no = int(num)
                        return f"on the last {days[no-1]} of the month"
                    else:
                        return ""
                elif "W" in field:  # weekday nearest to the day
                    num = field.replace("W", "")
                    return f"the weekday nearest to the {self._ordinal_day(num)} of the month"
                else:
                    if field.upper() in short_days:
                        return f"only on {days[short_days.index(field.upper())]}"
                    else:
                        return ""

    def _describe_month(self, field):
        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        short_months = [
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
        ]
        if "," in field:
            list_of_months = field.upper().split(",")
            if list_of_months[0].isdigit():
                list_of_months = [months[int(month) - 1] for month in field.split(",")]
            else:
                list_of_months = [
                    months[short_months.index(month)]
                    for month in field.upper().split(",")
                ]
            last_month = list_of_months.pop()
            return f"{', '.join(list_of_months)} and {last_month}"
        elif "-" in field:
            start, end = field.split("-")
            if start.isdigit():
                return f"{months[int(start) - 1]} through {months[int(end) - 1]}"
            else:
                start = start.upper()
                end = end.upper()
                return f"{months[short_months.index(start)]} through {months[short_months.index(end)]}"
        elif "/" in field:
            base, step = field.split("/")
            suffix = "s" if step != "1" else ""
            if base == "*":
                return f"every {step} month{suffix}"
            else:
                if base.isdigit():
                    return f"every {step} month{suffix} starting from {months[int(base) - 1]}"
                else:
                    return f"every {step} month{suffix} starting from {months[short_months.index(base)]}"
        else:
            if field.isdigit():
                return months[int(field) - 1]
            else:
                return (
                    months[short_months.index(int(field))]
                    if field.upper() in short_months
                    else ""
                )

    def _format_time(self, hour, minute, trim=False):
        suffix = "AM"
        if int(hour) > 12:
            suffix = "PM"
            hour = str(int(hour) - 12)

        if minute == "00":
            trim = True

        if hour == "0":
            hour = "12"

        if trim:
            return f"{hour} {suffix}"
        return f"{hour}:{minute.zfill(2)} {suffix}"

    def _ordinal_day(self, num):
        if num:
            suffix = "th"
            day = str(num)
            if day == "1" or day.endswith("1"):
                suffix = "st"
            elif day == "2":
                suffix = "nd"
            elif day == "3" or day.endswith("3"):
                suffix = "rd"
            return f"{day}{suffix}"
        return ""

    def _ordinal_word(self, num):
        """Convert day of month to ordinal word in English"""
        if num:
            day = str(num)
            ordinals = {
                "1": "first",
                "2": "second",
                "3": "third",
                "4": "fourth",
                "5": "fifth",
                "6": "sixth",
                "7": "seventh",
                "8": "eighth",
                "9": "ninth",
                "10": "tenth",
                "11": "eleventh",
                "12": "twelfth",
                "13": "thirteenth",
                "14": "fourteenth",
                "15": "fifteenth",
                "16": "sixteenth",
                "17": "seventeenth",
                "18": "eighteenth",
                "19": "nineteenth",
                "20": "twentieth",
            }
            if day in ordinals:
                return ordinals[day]
            elif day.endswith("1"):
                return f"{day}st"
            elif day.endswith("2"):
                return f"{day}nd"
            elif day.endswith("3"):
                return f"{day}rd"
            else:
                return f"{day}th"
        return ""
