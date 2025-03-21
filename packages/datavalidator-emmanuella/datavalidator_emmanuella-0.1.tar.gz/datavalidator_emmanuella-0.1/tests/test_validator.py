import unittest  # Import the unittest module
from datavalidator.validator import DataValidator  # Import the DataValidator class

class TestDataValidator(unittest.TestCase):
    """
    Test class for DataValidator methods.
    """

    def setUp(self):
        """Set up the DataValidator instance before each test."""
        self.validator = DataValidator()

    def test_validate_email(self):
        """Test email validation."""
        self.assertTrue(self.validator.validate_email("test@example.com"))  # Valid email
        self.assertFalse(self.validator.validate_email("invalid-email"))  # Invalid email

    def test_validate_phone(self):
        """Test phone number validation."""
        self.assertTrue(self.validator.validate_phone("+123-456-7890"))  # Valid phone
        self.assertFalse(self.validator.validate_phone("12345"))  # Invalid phone

    def test_validate_date(self):
        """Test date validation."""
        self.assertTrue(self.validator.validate_date("2024-03-14"))  # Valid date
        self.assertFalse(self.validator.validate_date("14-03-2024"))  # Invalid date

    def test_validate_url(self):
        """Test URL validation."""
        self.assertTrue(self.validator.validate_url("https://example.com"))  # Valid URL
        self.assertFalse(self.validator.validate_url("invalid-url"))  # Invalid URL

if __name__ == "__main__":
    unittest.main()

