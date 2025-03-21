import re

class DataValidator:
    """A class for validating personal data such as emails, phone numbers, dates, and URLs."""

    def validate_email(self, email: str) -> bool:
        """Validates an email address."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def validate_phone(self, phone: str) -> bool:
        """Validates a Nigerian phone number in local or international format."""
        pattern = r"^(?:\+234|0)(70|80|81|90|91)\d{8}$"
        return bool(re.match(pattern, phone))

    def validate_date(self, date: str) -> bool:
        """Validates a date in DD/MM/YYYY format with correct days for each month."""
        pattern = r"""^(
            (0[1-9]|1\d|2[0-8])/(0[1-9]|1[0-2])/\d{4} | 
            (29/(0[13-9]|1[0-2])/\d{4}) |  
            (30/(0[13-9]|1[0-2])/\d{4}) |  
            (31/(0[13578]|1[02])/\d{4}) |  
            (29/02/((19|20|21)[0-9][0-9]))  
        )$"""
        return bool(re.match(pattern, date, re.VERBOSE))

    def validate_url(self, url: str) -> bool:
        """Validates a URL supporting http, https, www, and domain extensions."""
        pattern = r"^(https?:\/\/)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?(\/\S*)?$"
        return bool(re.match(pattern, url))


# ✅ **Ensure test cases only run when script is executed directly**
if __name__ == "__main__":
    validator = DataValidator()

    # 📧 Email Tests
    print(validator.validate_email("user@example.com"))  # ✅ True
    print(validator.validate_email("invalid-email.com"))  # ❌ False

    # 📱 Phone Tests
    print(validator.validate_phone("+2348012345678"))  # ✅ True
    print(validator.validate_phone("08012345678"))     # ✅ True
    print(validator.validate_phone("081 234 5678"))    # ❌ False

    # 📆 Date Tests
    print(validator.validate_date("31/01/2024"))  # ✅ True
    print(validator.validate_date("30/02/2024"))  # ❌ False
    print(validator.validate_date("29/02/2024"))  # ✅ True
    print(validator.validate_date("31/04/2025"))  # ❌ False

    # 🌍 URL Tests
    print(validator.validate_url("https://www.google.com"))   # ✅ True
    print(validator.validate_url("http://example.org"))       # ✅ True
    print(validator.validate_url("www.example.net"))          # ✅ True
    print(validator.validate_url("https://google"))           # ❌ False
    print(validator.validate_url("htp://invalid.com"))        # ❌ False
