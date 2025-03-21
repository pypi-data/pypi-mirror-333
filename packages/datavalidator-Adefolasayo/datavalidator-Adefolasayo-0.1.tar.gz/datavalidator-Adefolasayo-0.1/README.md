# Data Validator

This project provides a Python class, `DataValidator`, for validating various data types, including dates, emails, phone numbers, and URLs. It uses `pytest` for unit testing to ensure the reliability of the validation functions.

## Features

-   **Date Validation:** Validates dates, checking for valid year, month, and day ranges.
-   **Email Validation:** Validates email addresses, ensuring they conform to standard email formats.
-   **Phone Number Validation:** Validates phone numbers, checking for correct length and numeric characters.
-   **URL Validation:** Validates URLs, ensuring they have a valid scheme and domain.
-   **Comprehensive Unit Tests:** Includes a suite of `pytest` tests to verify the accuracy of the validation methods.

## Getting Started

### Prerequisites

-   Python 3.x
-   `pytest` (install using `pip install pytest`)

### Installation

1.  Clone the repository:

    ```bash
    git clone [repository_url]
    ```

2.  Navigate to the project directory:

    ```bash
    cd DataValidator
    ```

### Usage

1.  **Running Tests:**

    To run the unit tests, navigate to the project's root directory and execute:

    ```bash
    pytest
    ```

    Or, to run a specific test file:

    ```bash
    pytest tests/test_validator.py
    ```

2.  **Using the `DataValidator` Class:**

    ```python
    from validator import DataValidator

    validator = DataValidator()

    # Date validation
    is_date_valid, date_message = validator.validate_date(2023, 10, 26)
    print(f"Date validation: {is_date_valid}, Message: {date_message}")

    # Email validation
    is_email_valid, email_message = validator.validate_email()
    print(f"Email validation: {is_email_valid}, Message: {email_message}")

    # Phone number validation
    is_phone_valid, phone_message = validator.validate_phone()
    print(f"Phone validation: {is_phone_valid}, Message: {phone_message}")

    # URL validation
    is_url_valid, url_message = validator.validate_url()
    print(f"URL validation: {is_url_valid}, Message: {url_message}")

    ```



# data-validator-Adefolasayo-Gboyega-adejuwon
