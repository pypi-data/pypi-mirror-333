# Personal Data Validator

## Overview
Personal Data Validator is a Python package that provides an easy way to validate different types of personal data, including:
- Email addresses
- Phone numbers
- Dates
- URLs

This package is built using Object-Oriented Programming (OOP) principles for better modularity and reusability.

## Installation
To install the package, run:
```bash
pip install datavalidator
```

## Usage
First, import the `DataValidator` class:
```python
from datavalidator.validator import DataValidator
```

### Validating an Email
```python
data = "example@email.com"
validator = DataValidator(data)
print(validator.validate_email())  # Output: True
```

### Validating a Phone Number
```python
data = "+1-800-555-1234"
validator = DataValidator(data)
print(validator.validate_phone())  # Output: True
```

### Validating a Date
```python
data = "2024-03-14"
validator = DataValidator(data)
print(validator.validate_date())  # Output: True
```

### Validating a URL
```python
data = "https://example.com"
validator = DataValidator(data)
print(validator.validate_url())  # Output: True
```

## Running Tests
The project includes unit tests to ensure proper functionality. To run the tests, use:
```bash
pytest tests/
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit changes (`git commit -m "Added new feature"`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

## License
This project is licensed under the MIT License.

## Author
**Oluwakorede Oyewole**  
Email: damisonoyewole@gmail.com

