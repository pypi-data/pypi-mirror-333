# healthInsight-pkg
HealthInsight – A Unified Python Package for Health Indicators

# HealthInsight

## Purpose of the Package
HealthInsight is a Python package designed to calculate various health indicators, including BMI, BAI, BSI, total body water, and mortality rates. It helps individuals and researchers assess different aspects of health and wellness using scientifically accepted formulas.

## Features
- **BMI Calculation** - Body Mass Index classification
- **BAI Calculation** - Body Adipose Index
- **BSI Calculation** - Body Shape Index
- **Total Body Water Calculation**
- **Corpulence Index**
- **Waist-to-Hip Ratio**
- **Mortality Rate Calculations** (Perinatal, Maternal, Infant)
- **Birth Rate Calculation**

## Getting Started
This package is built using Python and follows object-oriented programming principles. It is designed to be lightweight and easy to use for health-related calculations. HealthInsight is available on PyPI, so you can install it using the standard installation methods provided below.

## Installation
To install HealthInsight, ensure you have Python installed (>=3.12) and run:
```sh
pip install healthinsight
```
Or, if using Poetry:
```sh
poetry add healthinsight
```

## Usage
Import the `HealthCalc` class and use the available static methods for different health calculations.
```python
from healthinsight.calculations import HealthCalc
```

## Example
```python
from healthinsight.calculations import HealthCalc

# Calculate BMI
bmi_value, category = HealthCalc.bmi(65, 1.70)
print(f"BMI: {bmi_value}, Category: {category}")

# Calculate BAI
bai_value = HealthCalc.bai(90, 1.75)
print(f"BAI: {bai_value}")
```

## Contributions
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Commit your changes.
4. Submit a pull request.

Ensure to run tests before submitting:
```sh
pytest tests/
```

## Author
Developed by Olajide Oluwafemi Richard. Feel free to reach out for collaboration or inquiries!

