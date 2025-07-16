# Certificate Generator

A Python-based LaTeX certificate generation system for creating professional certificates with custom branding and batch processing capabilities.

## Features

- **Batch Processing**: Generate certificates for multiple participants from CSV files
- **Professional Branding**: Custom background images and university branding
- **Flexible Templates**: Easy-to-customize LaTeX templates with placeholders
- **Multiple Output Formats**: Individual PDFs and combined multi-page PDFs
- **Error Handling**: Robust handling of missing files and parsing errors

## Requirements

- Python 3.6+
- XeLaTeX (TeX Live or MiKTeX distribution)
- Required Python packages: `datetime`, `csv`, `subprocess`, `os`, `shutil`

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd certificates
```

2. Run the setup script to check requirements:
```bash
python3 setup.py
```

3. Install a LaTeX distribution if needed:
   - **macOS**: Install MacTeX
   - **Windows**: Install MiKTeX
   - **Linux**: Install TeX Live

## Setup

1. **Prepare your data**: Create a CSV file named `names.csv` with the following columns:
   ```
   Lastname,Name,completion_date
   Doe,John,2025-01-15
   Smith,Jane,2025-01-20
   ```

2. **Add your branding assets**:
   - Place your background image as `certificate_base_page.png`
   - Add any logo files referenced in the template

3. **Customize the template** (optional):
   - Edit `certificate_template.tex` to match your institution's branding
   - Modify colors, fonts, and layout as needed

## Usage

### Basic Usage

Run the certificate generator:
```bash
python3 generate_certificates.py
```

This will:
- Generate individual PDF certificates for each person in `names.csv`
- Create a combined PDF with all certificates
- Save all files to the `pdfs/` directory

### Customization

You can modify the certificate content by editing the variables in `generate_certificates.py`:

```python
workshop_title = "Your Workshop Title"
tutors = "Instructor Name"
duration = "Duration"
contents = [
    "Content item 1",
    "Content item 2",
    # Add more content items
]
date = "2025-01-15"
date_range = "2025-01-01 to 2025-01-15"
signatory1 = "Instructor Name"
signatory2 = "Chair Name"
location = "Location"
```

## File Structure

```
certificates/
├── generate_certificates.py      # Main generation script
├── certificate_template.tex      # LaTeX template
├── sample_names.csv             # Example CSV file
├── names.csv                    # Your participant data (not in repo)
├── certificate_base_page.png    # Background image (not in repo)
├── pdfs/                        # Generated PDFs (not in repo)
└── README.md                    # This file
```

## Template Customization

The LaTeX template (`certificate_template.tex`) uses placeholders that are replaced with actual data:

- `{{NAME}}` - Participant's full name
- `{{WORKSHOP}}` - Workshop/course title
- `{{DATE}}` - Completion date
- `{{DATE_RANGE}}` - Course date range
- `{{TUTORS}}` - Instructor names
- `{{DURATION}}` - Course duration
- `{{CONTENTS}}` - Course content items
- `{{SIGNATORY1}}` - First signatory
- `{{SIGNATORY2}}` - Second signatory

## Privacy and Security

This repository is configured to exclude sensitive files:

- **CSV files** containing participant data
- **Generated PDFs** with participant information
- **LaTeX files** with participant names
- **Background images** with institutional branding

The `.gitignore` file ensures these files are not accidentally committed to version control.

## Troubleshooting

### Common Issues

1. **XeLaTeX not found**: Install a LaTeX distribution
2. **Font issues**: Ensure Arial font is available or change to a system font
3. **Background image missing**: Place your background image as `certificate_base_page.png`
4. **CSV parsing errors**: Check that your CSV file has the correct column headers

### Debug Mode

For testing, you can uncomment the debug section in `generate_certificates.py` to generate a single test certificate.

## License

[Add your license information here]

## Contributing

[Add contribution guidelines if desired] 