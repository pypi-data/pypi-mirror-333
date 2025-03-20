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
        try:
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

            if not self._is_complex_value(self.parts[2]) and not self._is_complex_value(self.parts[4]):
                return True, ""

            if not self._days_no_conflict(self.parts[2], self.parts[4]):
                return (
                    False,
                    f"Day of month and day of week conflict in {self.parts[2]} and {self.parts[4]}",
                )
        except Exception as e:
            return False, f"Unable to parse: {str(e)}"
        return True, ""

    def _is_complex_value(self, value):
        """Check if the value is a complex field."""
        return "/" in value or "-" in value or "," in value or "#" in value        

    def _validate_minute(self):
        """Validates a string if it is a valid minute value."""
        return self._validate_generic(self.parts[0], r"(?:[0-9]|[1-5][0-9])")

    def _validate_hour(self):
        """Validates a string if it is a valid hour value."""
        return self._validate_generic(self.parts[1], r"(?:[0-9]|1[0-9]|2[0-3])")

    def _validate_day_of_month(self):
        """Validates a string if it is a valid day of month value."""
        day_range = r"(?:[1-9]|[1-2][0-9]|3[0-1])"
        additional_patterns = [r"^(?:" + day_range + r")C$", r"^(?:L|W|LW)$", r"^(?:[1-31])L$", r"^L-(?:[1-30])$"]
        return self._validate_generic(self.parts[2], day_range, additional_patterns)

    def _validate_month(self):
        """Validates a string if it is a valid month value."""
        number_range = r"(?:[1-9]|1[0-2])"
        month_range = r"(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)"
        return self._validate_generic(self.parts[3], number_range, [month_range])

    def _validate_day_of_week(self):
        """Validates a string if it is a valid day of week value."""
        dow_range = r"(?:[1-7])"
        # hash pattern is number-hash-number. some examples are: 1#3, 3#5
        additional_patterns = [r"^\*|[1-6]#[1-7]", r"^(?:SUN|MON|TUE|WED|THU|FRI|SAT)(?:-(?:SUN|MON|TUE|WED|THU|FRI|SAT))?$", r"^(?:SUN|MON|TUE|WED|THU|FRI|SAT)(?:,(?:SUN|MON|TUE|WED|THU|FRI|SAT))*$", r"^(?:[1-7])L$", r"^(?:" + dow_range + r")C$", r"^(?:L|W|LW)$"] 
        return self._validate_generic(self.parts[4], dow_range, additional_patterns)

    def _validate_year(self):
        """Validates a string if it is a valid year value."""
        return self._validate_generic(self.parts[5], r"(?:19[7-9]\d|2\d{3})")

    def _validate_generic(self, value, base_pattern, additional_patterns=None):
        """Generic validation method for cron fields."""
        combined_pattern = r"(?:{}{})".format(base_pattern, "|" + "|".join(additional_patterns) if additional_patterns else "")
        list_pattern = r"^(?:" + combined_pattern + r")(?:,\s*" + combined_pattern + r")*$"
        range_pattern = r"^" + combined_pattern + r"\s*-\s*" + combined_pattern + r"$"
        step_pattern = r"^" + combined_pattern + r"\s*/\s*" + combined_pattern + r"$|^\*/\s*" + base_pattern + r"$"
        wildcard_pattern = r"^(?:\*|\?)$"

        if re.match(wildcard_pattern, value):
            return True
        elif re.match(list_pattern, value):
            return True
        elif re.match(range_pattern, value):
            return self._validate_range_order(value)
        elif re.match(step_pattern, value):
            return True
        else:
            return False

    def _validate_range_order(self, value):
        """Validates if the range is in the correct order (low <= high)."""
        parts = value.split("-")
        if len(parts) != 2:
            return False

        try:
            low = int(parts[0])
            high = int(parts[1])
            return low <= high
        except ValueError:
            return False

    def _days_no_conflict(self, dom, dow):
        """Validates two strings based on the given rules."""
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
