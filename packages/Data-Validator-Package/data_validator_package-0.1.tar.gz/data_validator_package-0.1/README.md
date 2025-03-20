# Data Validator Package
This repository contains a simple data validator package built using python programming language. It is designed to validate personal data fields including email addresses, phone numbers, dates and URLs. It uses regular expressions and date parsing to ensure data correctness, making it easy to integrate data validation into your projects.

## Features
- Email Validation: This verifies that an email address conforms to the standard format.
- Phone Number Validation: This validates phone numbers (supports international formats).
- Date Validation:This checks that dates are in allowed formats (e.g., YYYY-MM-DD or DD/MM/YYYY) and that they represent valid calendar dates.
- URL Validation: This confirms that a URL is properly formatted.

## Installation
- Clone the repository to your local machaine
- ```
    git clone https://github.com/Data-Epic/data-validator-Adenike-Awotunde.git
    cd Data_Validator_Package
    ```
  
## Usage
Here's a quick example of how to use the Data Validator:
```
from Data_Validator_Package.data_validator import DataValidator

# Create an instance of DataValidator
validator = DataValidator()

# Set values
validator.set_email("awotundeadenike@outlook.com")
validator.set_phone_no("+2348012345678")
validator.set_date("1999-02-05")
validator.set_url("https://google.com")

# Validate data
if validator.validate_email():
    print("Email is valid.")
else:
    print("Email is invalid.")
```

## Running Tests
This package uses pytest for unit testing. To run the tests, navigate to the Data_Validator_Test directory and run:
```
pytest
```
## Contributing
Contributions to this package are welcome. To contribute, kindly: 
- Fork the repository.
- Create a new branch.
- Make your changes and commit them.
- Push to the branch and create a pull request. 

## License
This project is licensed under the MIT License. 

## Contact
For questions or suggestions, please open an issue or contact adenikeisblessed@gmail.com


