import re

class DataValidator:
    """Method to validate an email address."""
    def validate_email(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, self.data))
    
    """Method to validate a phone number."""
    def validate_phone(self):
        pattern = r'^\+?[1-9]\d{1,14}$'
        return bool(re.match(pattern, self.data))
    
    """Method to validate a date string (supports YYYY-MM-DD or YYYY/MM/DD)."""
    def validate_date(self):
        pattern = r"^(?:(?:18|19|20)\d{2})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])$"
        return bool(re.match(pattern, self.data))

    """Method to validate a URL."""
    def validate_url(self):
        pattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, self.data))
