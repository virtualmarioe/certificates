#!/usr/bin/env python3
"""
Certificate Generator Script
Generates LaTeX certificates for multiple people from a list of names.
"""

import os
import datetime
from typing import List

class CertificateGenerator:
    def __init__(self, template_file: str = "certificate_template.tex"):
        with open(template_file, 'r', encoding='utf-8') as f:
            self.template = f.read()

    def fill_template(self, fields: dict) -> str:
        latex = self.template
        for key, value in fields.items():
            latex = latex.replace(f"{{{{{key}}}}}", value)
        return latex

    def generate_certificates_from_list(self, names: list, output_file: str = "certificates.tex",
                                        workshop_title: str = "Workshop Title",
                                        tutors: str = "Instructor",
                                        duration: str = "Duration_hours",
                                        contents: list = None,
                                        date: str = None,
                                        date_range: str = None,
                                        signatory1: str = "Instructor",
                                        signatory2: str = "Chair",
                                        location: str = "Location") -> str:
        if contents is None:
            contents = [
                "Content_item 1",
                "Content_item 2",
                "Content_item 3",
                "Content_item 4"
            ]
        if date is None:
            date = datetime.date.today().strftime("%Y-%m-%d")
        if date_range is None:
            date_range = date
        
        # Create a proper combined LaTeX document
        combined_content = []
        combined_content.append(r"""% Combined Certificates Template for BPCN
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{fontspec}
\usepackage{array}
\usepackage{tabularx}
\usepackage{eso-pic} % Use eso-pic for background image
\usepackage{tikz}
\usepackage{setspace}

% Page setup
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=0.5cm}
\pagestyle{empty}

% Colors
\definecolor{darkblue}{RGB}{0,47,93}
\definecolor{lightblue}{RGB}{101,139,200}
\definecolor{grayText}{RGB}{136,136,136}

% Fonts
\setmainfont{Arial}

% Set background image using eso-pic (only if file exists)
\IfFileExists{../../certificate_base_page.png}{
  \AddToShipoutPictureBG{
    \put(-0.1cm,0){\includegraphics[width=\paperwidth,height=\paperheight]{../../certificate_base_page.png}}
  }
}{
  % No background image - blank page
}

\begin{document}
""")
        
        for name in names:
            fields = {
                "NAME": name,
                "SUBTITLE": "",
                "WORKSHOP": workshop_title,
                "DATE": date,
                "DATE_RANGE": date_range,
                "TUTORS": tutors,
                "DURATION": duration,
                "CONTENTS": "\n        ".join([f"\\item {item}" for item in contents]),
                "SIGNATORY1": signatory1,
                "SIGNATORY2": signatory2,
            }
            
            # Get the template content and extract just the document body
            template_content = self.fill_template(fields)
            
            # Extract the content between \begin{document} and \end{document}
            start_marker = r"\begin{document}"
            end_marker = r"\end{document}"
            start_pos = template_content.find(start_marker)
            end_pos = template_content.find(end_marker)
            
            if start_pos != -1 and end_pos != -1:
                # Extract the document body (content between \begin{document} and \end{document})
                document_body = template_content[start_pos + len(start_marker):end_pos].strip()
                combined_content.append(document_body)
                # Add a page break between certificates
                combined_content.append(r"\newpage")
        
        # Close the document
        combined_content.append(r"\end{document}")
        
        # Write the combined document
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(combined_content))
        return output_file

    def generate_certificates_from_csv(self, csv_file: str, output_file: str = "certificates.tex", **kwargs) -> str:
        import csv
        names = []
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Combine Lastname and Name columns if present, with proper whitespace handling
                if 'Lastname' in row and 'Name' in row:
                    lastname = row['Lastname'].strip()
                    firstname = row['Name'].strip()
                    full_name = f"{lastname} {firstname}".strip()
                elif 'Lastname' in row and ' Name' in row:  # Handle space in column name
                    lastname = row['Lastname'].strip()
                    firstname = row[' Name'].strip()
                    full_name = f"{lastname} {firstname}".strip()
                else:
                    full_name = row.get('Name', '').strip()
                names.append(full_name)
        return self.generate_certificates_from_list(names, output_file=output_file, **kwargs)

    def generate_individual_certificates_from_csv(self, csv_file: str,
                                                lastname_column: str = "Lastname",
                                                name_column: str = "Name",
                                                completion_date_column: str = "completion_date",
                                                output_dir: str = "output/pdfs",
                                                workshop_title: str = "Workshop_Title",
                                                tutors: str = "Instructor",
                                                duration: str = "Duration_hours",
                                                contents: list = None,
                                                date: str = None,
                                                date_range: str = None,
                                                signatory1: str = "Instructor",
                                                signatory2: str = "Chair",
                                                location: str = "Jena") -> list:
        import csv
        import subprocess
        import shutil
        os.makedirs(output_dir, exist_ok=True)
        names = []
        completion_dates = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            for row in reader:
                lastname = row.get(lastname_column, '').strip()
                firstname = row.get(name_column, '').strip()
                # Handle case where column name has a space
                if not firstname and ' Name' in row:
                    firstname = row[' Name'].strip()
                full_name = f"{lastname} {firstname}".strip()
                names.append(full_name)
                if completion_date_column and completion_date_column in row and row[completion_date_column].strip():
                    try:
                        date_obj = datetime.datetime.strptime(
                            row[completion_date_column].strip(), "%Y-%m-%d"
                        ).date()
                        completion_dates.append(date_obj.strftime("%Y-%m-%d"))
                    except ValueError:
                        completion_dates.append(datetime.date.today().strftime("%Y-%m-%d"))
                else:
                    completion_dates.append(datetime.date.today().strftime("%Y-%m-%d"))
        if contents is None:
            contents = [
                "Overview of local HPC resources",
                "Structure of HPC systems",
                "Usage of a HPC system for numerical intensive applications",
                "Interactive use"
            ]
        if date is None:
            date = datetime.date.today().strftime("%Y-%m-%d")
        if date_range is None:
            date_range = date
        generated_pdfs = []
        for i, (name, person_date) in enumerate(zip(names, completion_dates), 1):
            fields = {
                "NAME": name,
                "SUBTITLE": "",
                "WORKSHOP": workshop_title,
                "DATE": person_date,
                "DATE_RANGE": date_range,
                "TUTORS": tutors,
                "DURATION": duration,
                "CONTENTS": "\n        ".join([f"\\item {item}" for item in contents]),
                "SIGNATORY1": signatory1,
                "SIGNATORY2": signatory2,
            }
            latex_content = self.fill_template(fields)
            # Ensure each individual certificate is a complete LaTeX document
            # (No need to add \documentclass, \begin{document}, or \end{document} since the template already includes them)
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            
            # Create tex directory if it doesn't exist
            tex_dir = "output/tex"
            os.makedirs(tex_dir, exist_ok=True)
            
            latex_filename = os.path.join(tex_dir, f"certificate_{safe_name}.tex")
            pdf_filename = f"certificate_{safe_name}.pdf"
            with open(latex_filename, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            try:
                result = subprocess.run(
                    ["xelatex", "-interaction=nonstopmode", f"certificate_{safe_name}.tex"],
                    capture_output=True,
                    text=True,
                    cwd=tex_dir
                )
                if result.returncode == 0 and os.path.exists(os.path.join(tex_dir, pdf_filename)):
                    pdf_source = os.path.join(tex_dir, pdf_filename)
                    pdf_destination = os.path.join(output_dir, pdf_filename)
                    shutil.move(pdf_source, pdf_destination)
                    generated_pdfs.append(pdf_destination)
                    for ext in ['.aux', '.log', '.out']:
                        aux_file = os.path.join(tex_dir, f"certificate_{safe_name}{ext}")
                        if os.path.exists(aux_file):
                            os.remove(aux_file)
                    print(f"Generated: {pdf_destination}")
                else:
                    print(f"Failed to generate PDF for {name}")
            except Exception as e:
                print(f"Error generating PDF for {name}: {e}")
            # Keep LaTeX files in tex directory for reference
        return generated_pdfs


def main():
    """Generate certificates from CSV file."""
    generator = CertificateGenerator()
    # Common certificate fields (using the same content as debug mode)
    workshop_title = "Neuro-AI: Artificial Intelligence Applications in Neuroscience"
    tutors = "Dr. Mario Archila"
    duration = "26 h"
    contents = [
        "Fundamentals of Neuroscience and Artificial Intelligence (AI)",
        "Neuroscience concepts for AI and Neuro-AI",
        "Basic AI methods and algorithms",
        "Machine Learning and Deep Neural Networks",
        "Deep Learning in Neuroscience",
        "Ethical considerations and biases in AI",
        "Clinical Applications of Neuro-AI"
    ]
    date = "2025-07-17"
    date_range = "10.04.2025 to 10.07.2025"
    signatory1 = "Dr. Mario Archila"
    signatory2 = "Prof. Dr. Gyula Kovács"
    location = "Jena"
    
    # Check if names.csv exists and generate certificates from it
    csv_file = "names.csv"
    if os.path.exists(csv_file):
        print("Generating certificates from names.csv...")
        # Generate individual certificates for each person
        print("Generating individual certificates...")
        individual_pdfs = generator.generate_individual_certificates_from_csv(
            csv_file,
            output_dir="output/pdfs",
            workshop_title=workshop_title,
            tutors=tutors,
            duration=duration,
            contents=contents,
            date=date,
            date_range=date_range,
            signatory1=signatory1,
            signatory2=signatory2,
            location=location
        )
        print(f"Generated {len(individual_pdfs)} individual certificates in pdfs/ folder")
        # Also generate a combined PDF with all certificates
        print("Generating combined certificate file...")
        output_file = generator.generate_certificates_from_csv(
            csv_file,
            output_file="output/tex/certificates.tex",
            workshop_title=workshop_title,
            tutors=tutors,
            duration=duration,
            contents=contents,
            date=date,
            date_range=date_range,
            signatory1=signatory1,
            signatory2=signatory2,
            location=location
        )
        print(f"Generated LaTeX file: {output_file}")
        # Compile to PDF
        print("Compiling combined PDF...")
        try:
            import subprocess
            # Change to the tex directory for compilation
            tex_dir = "output/tex"
            os.makedirs(tex_dir, exist_ok=True)
            result = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "certificates.tex"],
                capture_output=True,
                text=True,
                cwd=tex_dir
            )
            if result.returncode == 0:
                print("PDF compilation successful!")
                # Move PDF to pdfs folder
                pdf_source = os.path.join(tex_dir, "certificates.pdf")
                if os.path.exists(pdf_source):
                    import shutil
                    pdf_destination = os.path.join("output/pdfs", "all_certificates.pdf")
                    shutil.move(pdf_source, pdf_destination)
                    print(f"Combined PDF saved to: {pdf_destination}")
                    # Clean up auxiliary files
                    for ext in ['.aux', '.log', '.out']:
                        aux_file = os.path.join(tex_dir, f"certificates{ext}")
                        if os.path.exists(aux_file):
                            os.remove(aux_file)
                    print("Auxiliary files cleaned up.")
                else:
                    print("PDF file not found after compilation.")
            else:
                print("PDF compilation failed!")
                print("Error output:")
                print(result.stderr)
        except FileNotFoundError:
            print("XeLaTeX not found. Please install a LaTeX distribution (like TeX Live or MiKTeX).")
        except Exception as e:
            print(f"Error during compilation: {e}")
    else:
        print(f"CSV file '{csv_file}' not found. Please create it with 'Lastname', 'Name', and 'completion_date' columns.")
        # Fallback to example list
        names = [
            "Lincoln,Abraham",
            "King,Martin Luther",
            "Mandela,Nelson"
        ]
        print("Generating certificates from example list...")
        output_file = generator.generate_certificates_from_list(names)
        print(f"Generated: {output_file}")

    # Debug mode (commented out but preserved)
    """
    # Debug single certificate
    name = "Debug Testuser"
    workshop_title = "Neuro-AI: Artificial Intelligence Applications in Neuroscience"
    date_range = "10.04.2025 to 10.07.2025"
    tutors = "Dr. Mario Archila"
    duration = "26:00 h"
    contents = [
        "Fundamentals of Neuroscience and Artificial Intelligence (AI)",
        "Neuroscience concepts for AI and Neuro-AI",
        "Basic AI methods and algorithms",
        "Machine Learning, and Deep Neural Networks",
        "Deep Learning in Neuroscience",
        "Ethical considerations and biases in AI",
        "Clinical Applications of Neuro-AI"
    ]
    date = "2025-07-17"
    
    # Signatories
    signatory1 = "Dr. Mario Archila"
    signatory2 = "Prof. Dr. Gyula Kovács"
    location = "Jena"
    print("Generating debug certificate for one name...")
    output_file = generator.generate_certificates_from_list(
        [name],
        output_file="debug_certificate.tex",
        workshop_title=workshop_title,
        tutors=tutors,
        duration=duration,
        contents=contents,
        date=date,
        date_range=date_range,
        signatory1=signatory1,
        signatory2=signatory2,
        location=location
    )
    print(f"Generated LaTeX file: {output_file}")
    # Compile to PDF
    print("Compiling debug PDF...")
    try:
        import subprocess
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", output_file],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("PDF compilation successful!")
        else:
            print("PDF compilation failed!")
            print("Error output:")
            print(result.stderr)
    except FileNotFoundError:
        print("XeLaTeX not found. Please install a LaTeX distribution (like TeX Live or MiKTeX).")
    except Exception as e:
        print(f"Error during compilation: {e}")
    """

if __name__ == "__main__":
    main() 