import re  # Import the regular expressions module

class DataValidator:
    """
    A class to validate personal data like emails, phone numbers, dates, and URLs.
    """

    def validate_email(self, email):
        """
        Validates an email address.

        Parameters:
        email (str): The email to validate.

        Returns:
        bool: True if valid, False otherwise.
        """
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email))

    def validate_phone(self, phone):
        """
        Validates a phone number.

        Parameters:
        phone (str): The phone number to validate.

        Returns:
        bool: True if valid, False otherwise.
        """
        pattern = r'^\+?(\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'  # Requires at least 10 digits
        return bool(re.match(pattern, phone))



    def validate_date(self, date):
        """
        Validates a date in YYYY-MM-DD format.

        Parameters:
        date (str): The date to validate.

        Returns:
        bool: True if valid, False otherwise.
        """
        pattern = r'^\d{4}-\d{2}-\d{2}$'  # Example format: 2024-03-14
        return bool(re.match(pattern, date))

    def validate_url(self, url):
        """
        Validates a URL.

        Parameters:
        url (str): The URL to validate.

        Returns:
        bool: True if valid, False otherwise.
        """
        pattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))

