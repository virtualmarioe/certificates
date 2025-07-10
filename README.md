# Certificate Generator

A Python script to generate professional LaTeX certificates for multiple people from a CSV file.

## Features

- Generate individual PDF certificates for each person
- Create a combined PDF with all certificates
- Professional certificate design with decorative borders
- Support for custom completion dates
- Automatic certificate ID generation
- Clean LaTeX output

## Requirements

- Python 3.6+
- XeLaTeX (for PDF compilation)
- Required Python packages: `csv`, `datetime`, `os`, `subprocess`, `shutil`

## Installation

1. Clone this repository
2. Install a LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
3. Ensure XeLaTeX is available in your PATH

## Usage

### 1. Prepare your data

Create a `names.csv` file with the following columns:
- `Lastname`: Last name of the person
- `Name`: First name of the person  
- `completion_date`: Completion date in YYYY-MM-DD format (optional)

Example:
```csv
Lastname,Name,completion_date
Doe,John,2025-01-15
Smith,Jane,2025-01-20
```

### 2. Generate certificates

Run the script:
```bash
python generate_certificates.py
```

This will:
- Generate individual PDF certificates in the `pdfs/` folder
- Create a combined PDF with all certificates
- Generate a LaTeX file (`certificates.tex`) for manual compilation

### 3. Output files

- `pdfs/`: Directory containing individual PDF certificates
- `pdfs/all_certificates.pdf`: Combined PDF with all certificates
- `certificates.tex`: LaTeX source file

## File Structure

```
certificate/
├── generate_certificates.py    # Main script
├── certificate_template.tex    # LaTeX template
├── certificates.tex           # Generated LaTeX file
├── names.csv                  # Input data (ignored by git)
├── pdfs/                      # Output directory
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Git Ignore Rules

The following files are excluded from version control:
- `names.csv` (contains personal data)
- `*.pdf` (generated certificates)
- LaTeX auxiliary files
- Temporary and cache files

## Customization

You can modify the certificate design by editing the LaTeX template in the `CertificateGenerator` class. The template includes:
- Professional border design
- Custom colors and fonts
- Signature sections
- Certificate numbering

## License

This project is open source and available under the MIT License. 