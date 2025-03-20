"""A module to describe a given cron expression. The module provides a Cron class that can be used to describe a given cron expression.
Example:
    To describe a cron expression, create a Cron object with the expression as an argument:
        cron = Cron("* * * * *")
        print(cron.description)
    This will output:
        Every minute
"""

import datetime
from . import ExpressionParser, ExpressionValidator


class Cron:
    """A class to describe a given cron expression.
    Attributes:
        expression (str): The cron expression to describe.
        description (str): The human-readable description of the cron expression
    """

    def __init__(self, expression):
        """Initialize the Cron object.
        Args:
            expression (str): The cron expression to describe.
        """
        self.expression = expression
        self.description = self._parse_expression()
        self.next_run = self._next_run()

    def _parse_expression(self):
        """Parse the cron expression and return a human-readable description.
        Returns:
            str: A human-readable description of the cron expression.
        """
        description = ""

        # Split the expression into its components by space
        components = self.expression.split(" ")

        # Check if the expression has 5-6 components
        components_ctr = len(components)
        if components_ctr < 5 or components_ctr > 6:
            description = (
                f"({self.expression}) has {components_ctr} components, expected 5 or 6"
            )
        elif components_ctr == 5:
            components.append("*")  # for the year component which is optional

        if self.expression == "* * * * *":
            return "Every minute"

        # Check if the expression has valid components
        is_valid, check_message = self._check_expression(components)
        if not is_valid:
            description = check_message
        else:
            # Parse the expression
            description = ExpressionParser.ExpressionParser(components).description

        # Return the description
        return description

    def _check_expression(self, parts):
        """Check if the expression has valid components.
        Args:
            parts (list): The components of the cron expression.
        Returns:
            bool: True if the expression is valid, False otherwise.
            str: A message describing the result of the check.
        """
        is_valid = True
        validator_message = ""

        # validate minute
        validator = ExpressionValidator.ExpressionValidator(parts)
        is_valid, validator_message = validator.validate()

        return is_valid, validator_message

    def _next_run(self, current_time=None):
        """Get the next run time of the cron expression. (Not implemented yet)
        Args:
            current_time (datetime): The current time.
        Returns:
            datetime: The next run time of the cron expression.
        """

        if current_time is None:
            # Get the current time plus 1 minute
            current_time = datetime.datetime.now() + datetime.timedelta(minutes=1)

        # Get the next run time
        next_run = current_time.replace(
            second=0, microsecond=0
        )  # set seconds and microseconds to 0

        return next_run
