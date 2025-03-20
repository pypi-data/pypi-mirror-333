# Fund Insight Engine

A Python package providing utility functions for fund code management and analysis. This package helps streamline the process of handling fund-related data and provides insights into fund operations.

## Features

- Fund code retrieval and validation
  - Support for various fund types (equity, mixed, bond, etc.)
  - Fund class categorization (mother fund, general, class fund)
  - Division-based fund code management
- Integration with financial dataset preprocessing
- AWS S3 integration for data storage

## Installation

You can install the package using pip:

```bash
pip install fund-insight-engine
```

## Requirements

- Python >= 3.7
- financial_dataset_preprocessor >= 0.2.9
- aws_s3_controller >= 0.7.5

## Usage

```python
from fund_insight_engine import fund_codes_retriever

# Get fund codes by type
equity_funds = fund_codes_retriever.get_fund_codes_equity_type()
mixed_funds = fund_codes_retriever.get_fund_codes_equity_mixed_type()

# Get fund codes by class
mother_funds = fund_codes_retriever.get_fund_codes_mother()
class_funds = fund_codes_retriever.get_fund_codes_class()

# Get fund names mapping
fund_names = fund_codes_retriever.get_mapping_fund_names_main()
```

## Version History

### 0.1.1

- Enhanced fund code utilities
  - Added mapping functions by fund type, class, and division
  - Added FUND_CLASSES and FUND_TYPES constants
  - Added pseudo_consts.py for future use
  - Fixed date_ref parameter handling in division mapping functions
  - Improved code organization and type hints

### 0.1.0 (Initial Release)

- Basic fund code management functionality
  - Fund type-based retrieval
  - Fund class-based retrieval
  - Division-based management
- AWS S3 integration
- Financial dataset preprocessing integration

## License

This project is licensed under the MIT License.

## Author

**June Young Park**
AI Management Development Team Lead & Quant Strategist at LIFE Asset Management

LIFE Asset Management is a hedge fund management firm that integrates value investing and engagement strategies with quantitative approaches and financial technology, headquartered in Seoul, South Korea.

## Contact

- Email: juneyoungpaak@gmail.com
- Location: TWO IFC, Yeouido, Seoul
