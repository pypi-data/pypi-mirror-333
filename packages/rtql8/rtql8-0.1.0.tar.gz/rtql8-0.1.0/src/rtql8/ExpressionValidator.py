"""
This module contains the ExpressionValidator class which is used to validate a given cron expression.
"""

import re


class ExpressionValidator(object):
    """A class to validate a given cron expression."""

    def __init__(self, parts):
        """Initialize the ExpressionValidator object."""
        self.parts = parts

    def validate(self):
        """Validates the cron expression."""
        if not self._validate_minute():
            return False, f"Invalid minute value in {self.parts[0]}"
        if not self._validate_hour():
            return False, f"Invalid hour value in {self.parts[1]}"
        if not self._validate_day_of_month():
            return False, f"Invalid day of month value in {self.parts[2]}"
        if not self._validate_month():
            return False, f"Invalid month value in {self.parts[3]}"
        if not self._validate_day_of_week():
            return False, f"Invalid day of week value in {self.parts[4]}"
        if not self._validate_year():
            return False, f"Invalid year value in {self.parts[5]}"
        if not self._days_no_conflict(self.parts[2], self.parts[4]):
            return (
                False,
                f"Day of month and day of week conflict in {self.parts[2]} and {self.parts[4]}",
            )
        return True, ""

    def _validate_minute(self):
        """
        Validates a string if it is a valid minute value, or just *
        or with an operator between minutes such as [0-59], [1,2,3], [*/5].
        """
        value = self.parts[0]

        minute_range = r"(?:[0-9]|[1-5][0-9])"
        list_pattern = r"^(?:" + minute_range + r")(?:,\s*" + minute_range + r")*$"
        range_pattern = r"^" + minute_range + r"\s*-\s*" + minute_range + r"$"
        step_pattern = (
            r"^"
            + minute_range
            + r"\s*/\s*"
            + minute_range
            + r"$|^"
            + r"\*/\s*"
            + minute_range
            + r"$"
        )
        wildcard_pattern = r"^\*$"

        if re.match(list_pattern, value):
            return True
        elif re.match(range_pattern, value):
            return True
        elif re.match(step_pattern, value):
            return True
        elif re.match(wildcard_pattern, value):
            return True
        else:
            return False

    def _validate_hour(self):
        """
        Validates a string with the following rules:
        - Numbers must be in the range 0-23.
        - Symbols (',', '-', '/') can only appear between numbers.
        - '*' can only appear as a standalone value or before a slash.

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        value = self.parts[1]

        hour_range = r"(?:[0-9]|1[0-9]|2[0-3])"  # Updated for 0-23 range
        list_pattern = r"^(?:" + hour_range + r")(?:,\s*" + hour_range + r")*$"
        range_pattern = r"^" + hour_range + r"\s*-\s*" + hour_range + r"$"
        step_pattern = (
            r"^"
            + hour_range
            + r"\s*/\s*"
            + hour_range
            + r"$|^"
            + r"\*/\s*"
            + hour_range
            + r"$"
        )
        wildcard_alone_pattern = r"^\*$"

        if re.match(list_pattern, value):
            return True
        elif re.match(range_pattern, value):
            return True
        elif re.match(step_pattern, value):
            return True
        elif re.match(wildcard_alone_pattern, value):
            return True
        else:
            return False

    def _validate_day_of_month(self):
        """
        Validates a day or month
        """
        value = self.parts[2]

        day_range = r"(?:[1-9]|[1-2][0-9]|3[0-1])"
        c_pattern = r"^(?:" + day_range + r")C$"
        lw_pattern = r"^(?:L|W|LW)$"
        one_to_seven_l_pattern = r"^(?:[1-7])L$"

        combined_pattern = (
            r"(?:"
            + day_range
            + r"|"
            + c_pattern
            + r"|"
            + lw_pattern
            + r"|"
            + one_to_seven_l_pattern
            + r")"
        )

        list_pattern = (
            r"^(?:" + combined_pattern + r")(?:,\s*" + combined_pattern + r")*$"
        )
        range_pattern = r"^" + combined_pattern + r"\s*-\s*" + combined_pattern + r"$"
        step_pattern = (
            r"^"
            + combined_pattern
            + r"\s*/\s*"
            + combined_pattern
            + r"$|^"
            + r"\*/\s*"
            + day_range
            + r"$"
        )
        wildcard_alone_pattern = r"^(?:\*|\?)$"

        if re.match(wildcard_alone_pattern, value):
            return True
        elif re.match(c_pattern, value):
            return True
        elif re.match(lw_pattern, value):
            return True
        elif re.match(one_to_seven_l_pattern, value):
            return True
        elif re.match(list_pattern, value):
            return True
        elif re.match(range_pattern, value):
            return True
        elif re.match(step_pattern, value):
            return True
        else:
            return False

    def _validate_month(self):
        """
        Validates a string with the refined wildcard rule.
        """
        value = self.parts[3]

        number_range = r"(?:[1-9]|1[0-2])"
        month_range = r"(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)"
        combined_number_pattern = r"(?:" + number_range + r")"
        combined_month_pattern = r"(?:" + month_range + r")"

        list_pattern_number = (
            r"^(?:"
            + combined_number_pattern
            + r")(?:,\s*"
            + combined_number_pattern
            + r")*$"
        )
        list_pattern_month = (
            r"^(?:"
            + combined_month_pattern
            + r")(?:,\s*"
            + combined_month_pattern
            + r")*$"
        )
        range_pattern_number = (
            r"^" + combined_number_pattern + r"\s*-\s*" + combined_number_pattern + r"$"
        )
        range_pattern_month = (
            r"^" + combined_month_pattern + r"\s*-\s*" + combined_month_pattern + r"$"
        )
        step_pattern = (
            r"^"
            + combined_number_pattern
            + r"\s*/\s*"
            + combined_number_pattern
            + r"$|^"
            + r"\*/\s*"
            + number_range
            + r"$"
        )
        wildcard_alone_pattern = r"^(?:\*|\?)$"

        if re.match(wildcard_alone_pattern, value):
            return True
        elif re.match(list_pattern_number, value):
            return True
        elif re.match(list_pattern_month, value):
            return True
        elif re.match(range_pattern_number, value):
            return self._validate_range_order_number(value)
        elif re.match(range_pattern_month, value):
            return self._validate_range_order_month(value)
        elif re.match(step_pattern, value):
            return True
        else:
            return False

    def _validate_range_order_number(self, value):
        """
        Validates number range order (low <= high).
        """
        parts = value.split("-")
        if len(parts) != 2:
            return False

        try:
            low = int(parts[0].strip())
            high = int(parts[1].strip())
            return low <= high
        except ValueError:
            return False

    def _validate_range_order_month(self, value):
        """
        Validates month range order (low <= high).
        """
        parts = value.split("-")
        if len(parts) != 2:
            return False

        months = [
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
        try:
            low = months.index(parts[0].strip())
            high = months.index(parts[1].strip())
            return low <= high
        except ValueError:
            return False

    def _validate_range_order(self, value):
        """
        Validates if the range is in the correct order (low <= high).
        """
        parts = value.split("-")
        if len(parts) != 2:
            return False

        try:
            low = int(parts[0])
            high = int(parts[1])
            return low <= high
        except ValueError:
            return False

    def _validate_day_of_week(self):
        """
        Validates a string with the refined wildcard rule.
        """
        value = self.parts[4]

        dow_range = r"(?:[1-7])"
        dom_range = r"(?:[1-9]|[1-2][0-9]|3[0-1])"
        c_pattern = r"^(?:" + dom_range + r")C$"
        lw_pattern = r"^(?:L|W|LW)$"
        one_to_seven_l_pattern = r"^(?:[1-7])L$"
        day_pattern = (
            r"^(?:SUN|MON|TUE|WED|THU|FRI|SAT)(?:-(?:SUN|MON|TUE|WED|THU|FRI|SAT))?$"
        )
        day_pattern_comma_separated = (
            r"^(?:SUN|MON|TUE|WED|THU|FRI|SAT)(?:,(?:SUN|MON|TUE|WED|THU|FRI|SAT))*$"
        )
        combined_pattern = (
            r"(?:"
            + dow_range
            + r"|"
            + c_pattern
            + r"|"
            + lw_pattern
            + r"|"
            + one_to_seven_l_pattern
            + r"|"
            + day_pattern
            + r"|"
            + day_pattern_comma_separated
            + r")"
        )

        list_pattern = (
            r"^(?:" + combined_pattern + r")(?:,\s*" + combined_pattern + r")*$"
        )
        range_pattern = r"^" + combined_pattern + r"\s*-\s*" + combined_pattern + r"$"
        step_pattern = (
            r"^"
            + combined_pattern
            + r"\s*/\s*"
            + combined_pattern
            + r"$|^"
            + r"\*/\s*"
            + dow_range
            + r"$"
        )
        hash_pattern = r"^" + combined_pattern + r"\s*#\s*" + combined_pattern + r"$"
        wildcard_alone_pattern = r"^(?:\*|\?)$"

        if re.match(wildcard_alone_pattern, value):
            return True
        elif re.match(c_pattern, value):
            return True
        elif re.match(lw_pattern, value):
            return True
        elif re.match(one_to_seven_l_pattern, value):
            return True
        elif re.match(day_pattern, value):
            return True
        elif re.match(day_pattern_comma_separated, value):
            return True
        elif re.match(list_pattern, value):
            return True
        elif re.match(range_pattern, value):
            return True
        elif re.match(hash_pattern, value):
            return True
        elif re.match(step_pattern, value):
            return True
        else:
            return False

    def _validate_year(self):
        """
        Validates a string with the refined wildcard rule.
        """
        value = self.parts[5]

        year_range = r"(?:19[7-9]\d|2\d{3})"
        combined_pattern = r"(?:" + year_range + r")"

        list_pattern = (
            r"^(?:" + combined_pattern + r")(?:,\s*" + combined_pattern + r")*$"
        )
        range_pattern = r"^" + combined_pattern + r"\s*-\s*" + combined_pattern + r"$"
        wildcard_alone_pattern = r"^(?:\*|\?)$"

        if re.match(wildcard_alone_pattern, value):
            return True
        elif re.match(list_pattern, value):
            return True
        elif re.match(range_pattern, value):
            return self._validate_range_order(value)
        else:
            return False

    def _days_no_conflict(self, dom, dow):
        """
        Validates two strings based on the given rules:
        - Mutual exclusion of L, W, C in both strings.
        - If one string contains L, W, or C, the other can only have * or ?.
        - Only one string can contain ?.
        - If one string is complex, other string can only contain * or ?.
        """

        has_lwc1 = bool(re.search(r"[LWC]", dom))
        has_lwc2 = bool(re.search(r"[LWC#]", dow))

        has_other1 = bool(re.search(r"[^\*\?]", dom))
        has_other2 = bool(re.search(r"[^\*\?]", dow))

        has_question_mark1 = "?" in dom
        has_question_mark2 = "?" in dow

        if has_lwc1 and has_lwc2:
            return False  # L, W, C, #  cannot be in both strings

        if has_lwc1:
            return not has_other2

        if has_lwc2:
            return not has_other1

        if has_question_mark1 and has_question_mark2:
            return False  # Only one string can contain ?

        if has_other1:
            return not has_other2

        if has_other2:
            return not has_other1

        return True
