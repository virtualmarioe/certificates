#!/usr/bin/env python3
"""
Certificate Generator Script
Generates LaTeX certificates for multiple people from a list of names.
"""

import os
import datetime
from typing import List, Dict

class CertificateGenerator:
    def __init__(self):
        self.latex_header = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{tikz}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{fontspec}
\usepackage{fancyhdr}
\usepackage{datetime}
\usepackage{etoolbox}

% Page setup
\geometry{margin=1in}
\pagestyle{empty}

% Colors
\definecolor{primary}{RGB}{25, 118, 210}
\definecolor{secondary}{RGB}{245, 245, 245}
\definecolor{accent}{RGB}{255, 193, 7}

% Font setup (using system fonts)
\setmainfont{Times New Roman}
\newfontfamily\titlefont{Times New Roman}
\newfontfamily\signaturefont{Times New Roman}

% Certificate dimensions
\newlength{\certwidth}
\newlength{\certheight}
\setlength{\certwidth}{8.5in}
\setlength{\certheight}{11in}

% Command to generate certificate for a single person
\newcommand{\generatecertificate}[4]{%
    \begin{center}
        \begin{tikzpicture}[remember picture,overlay]
            % Background border
            \draw[line width=3pt, color=primary] 
                (current page.north west) rectangle (current page.south east);
            
            % Inner border
            \draw[line width=1pt, color=primary!50] 
                ([xshift=0.5in,yshift=-0.5in]current page.north west) 
                rectangle 
                ([xshift=-0.5in,yshift=0.5in]current page.south east);
            
            % Decorative corner elements
            \draw[line width=2pt, color=accent] 
                ([xshift=1in,yshift=-1in]current page.north west) -- 
                ([xshift=2in,yshift=-1in]current page.north west);
            \draw[line width=2pt, color=accent] 
                ([xshift=1in,yshift=-1in]current page.north west) -- 
                ([xshift=1in,yshift=-2in]current page.north west);
            
            \draw[line width=2pt, color=accent] 
                ([xshift=-1in,yshift=-1in]current page.north east) -- 
                ([xshift=-2in,yshift=-1in]current page.north east);
            \draw[line width=2pt, color=accent] 
                ([xshift=-1in,yshift=-1in]current page.north east) -- 
                ([xshift=-1in,yshift=-2in]current page.north east);
            
            \draw[line width=2pt, color=accent] 
                ([xshift=1in,yshift=1in]current page.south west) -- 
                ([xshift=2in,yshift=1in]current page.south west);
            \draw[line width=2pt, color=accent] 
                ([xshift=1in,yshift=1in]current page.south west) -- 
                ([xshift=1in,yshift=2in]current page.south west);
            
            \draw[line width=2pt, color=accent] 
                ([xshift=-1in,yshift=1in]current page.south east) -- 
                ([xshift=-2in,yshift=1in]current page.south east);
            \draw[line width=2pt, color=accent] 
                ([xshift=-1in,yshift=1in]current page.south east) -- 
                ([xshift=-1in,yshift=2in]current page.south east);
        \end{tikzpicture}
        
        % Certificate content
        \vspace*{2cm}
        
        % Header
        \begin{center}
            \titlefont\Huge\textbf{CERTIFICATE OF COMPLETION}
        \end{center}
        
        \vspace{1cm}
        
        % Subtitle
        \begin{center}
            \Large\textcolor{primary}{High Performance Computing (HPC)}\\
            \Large\textcolor{primary}{General Beginner Course}
        \end{center}
        
        \vspace{2cm}
        
        % Main text
        \begin{center}
            \Large This is to certify that
        \end{center}
        
        \vspace{0.5cm}
        
        % Recipient name
        \begin{center}
            \titlefont\Huge\textbf{#1}
        \end{center}
        
        \vspace{0.5cm}
        
        % Certificate text
        \begin{center}
            \Large has successfully completed the requirements for the\\
            \Large\textbf{High Performance Computing General Beginner Course}
        \end{center}
        
        \vspace{1cm}
        
        % Course details
        \begin{center}
            \Large Course Duration: 40 hours\\
            \Large Completion Date: #2\\
            \Large Certificate ID: #3
        \end{center}
        
        \vspace{2cm}
        
        % Signatures section
        \begin{center}
            \begin{tabular}{ccc}
                \rule{3cm}{0.5pt} & \hspace{2cm} & \rule{3cm}{0.5pt} \\
                Course Instructor & & Program Director \\
                \vspace{0.5cm} & & \vspace{0.5cm} \\
                \rule{3cm}{0.5pt} & \hspace{2cm} & \rule{3cm}{0.5pt} \\
                Academic Coordinator & & Date: #4
            \end{tabular}
        \end{center}
        
        \vspace{1cm}
        
        % Footer
        \begin{center}
            \small\textcolor{gray}{This certificate is issued electronically and is valid without signature}
        \end{center}
        
        \vspace{0.5cm}
        
        % Certificate number
        \begin{center}
            \small\textcolor{gray}{Certificate Number: #3}
        \end{center}
    \end{center}
    
    \newpage
}

% Main document
\begin{document}
"""

        self.latex_footer = r"""
\end{document}"""

    def generate_certificate_id(self, index: int, year: str = None) -> str:
        """Generate a unique certificate ID."""
        if year is None:
            year = datetime.datetime.now().strftime("%Y")
        return f"HPC-{year}-{index:03d}"

    def format_date(self, date_obj: datetime.date) -> str:
        """Format date in a readable format."""
        return date_obj.strftime("%B %d, %Y")

    def generate_latex_for_person(self, name: str, completion_date: datetime.date, 
                                certificate_id: str, issue_date: datetime.date = None) -> str:
        """Generate LaTeX code for a single certificate."""
        if issue_date is None:
            issue_date = completion_date
            
        formatted_completion = self.format_date(completion_date)
        formatted_issue = self.format_date(issue_date)
        
        return f"\\generatecertificate{{{name}}}{{{formatted_completion}}}{{{certificate_id}}}{{{formatted_issue}}}"

    def generate_certificates_from_list(self, names: List[str], 
                                      completion_date: datetime.date = None,
                                      output_file: str = "certificates.tex") -> str:
        """
        Generate LaTeX certificates for a list of names.
        
        Args:
            names: List of full names
            completion_date: Date of completion (defaults to today)
            output_file: Output LaTeX file name
            
        Returns:
            Path to the generated LaTeX file
        """
        if completion_date is None:
            completion_date = datetime.date.today()
            
        # Generate LaTeX content
        latex_content = self.latex_header
        
        for i, name in enumerate(names, 1):
            certificate_id = self.generate_certificate_id(i)
            certificate_latex = self.generate_latex_for_person(
                name, completion_date, certificate_id
            )
            latex_content += f"\n{certificate_latex}\n"
            
        latex_content += self.latex_footer
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
            
        return output_file

    def generate_certificates_from_csv(self, csv_file: str, 
                                     lastname_column: str = "Lastname",
                                     name_column: str = "Name",
                                     completion_date_column: str = "completion_date",
                                     output_file: str = "certificates.tex") -> str:
        """
        Generate certificates from a CSV file.
        
        Args:
            csv_file: Path to CSV file
            lastname_column: Column name containing last names
            name_column: Column name containing first names
            completion_date_column: Column name containing completion dates
            output_file: Output LaTeX file name
            
        Returns:
            Path to the generated LaTeX file
        """
        import csv
        
        names = []
        completion_dates = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            for row in reader:
                lastname = row[lastname_column].strip()
                firstname = row[name_column].strip()
                full_name = f"{lastname} {firstname}"
                names.append(full_name)
                if completion_date_column and completion_date_column in row:
                    try:
                        date_obj = datetime.datetime.strptime(
                            row[completion_date_column].strip(), "%Y-%m-%d"
                        ).date()
                        completion_dates.append(date_obj)
                    except ValueError:
                        completion_dates.append(datetime.date.today())
                else:
                    completion_dates.append(datetime.date.today())
        
        # Generate LaTeX content
        latex_content = self.latex_header
        
        for i, (name, completion_date) in enumerate(zip(names, completion_dates), 1):
            certificate_id = self.generate_certificate_id(i)
            certificate_latex = self.generate_latex_for_person(
                name, completion_date, certificate_id
            )
            latex_content += f"\n{certificate_latex}\n"
            
        latex_content += self.latex_footer
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
            
        return output_file

    def generate_individual_certificates_from_csv(self, csv_file: str,
                                                lastname_column: str = "Lastname",
                                                name_column: str = "Name",
                                                completion_date_column: str = "completion_date",
                                                output_dir: str = "pdfs") -> list:
        """
        Generate individual PDF certificates for each person from a CSV file.
        
        Args:
            csv_file: Path to CSV file
            lastname_column: Column name containing last names
            name_column: Column name containing first names
            completion_date_column: Column name containing completion dates
            output_dir: Directory to save individual PDFs
            
        Returns:
            List of paths to generated PDF files
        """
        import csv
        import subprocess
        import shutil
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        names = []
        completion_dates = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            for row in reader:
                lastname = row[lastname_column].strip()
                firstname = row[name_column].strip()
                full_name = f"{lastname} {firstname}"
                names.append(full_name)
                if completion_date_column and completion_date_column in row:
                    try:
                        date_obj = datetime.datetime.strptime(
                            row[completion_date_column].strip(), "%Y-%m-%d"
                        ).date()
                        completion_dates.append(date_obj)
                    except ValueError:
                        completion_dates.append(datetime.date.today())
                else:
                    completion_dates.append(datetime.date.today())
        
        generated_pdfs = []
        
        for i, (name, completion_date) in enumerate(zip(names, completion_dates), 1):
            certificate_id = self.generate_certificate_id(i)
            
            # Create individual LaTeX file for this person
            individual_latex = self.latex_header
            individual_latex += f"\n{self.generate_latex_for_person(name, completion_date, certificate_id)}\n"
            individual_latex += self.latex_footer
            
            # Create safe filename
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            latex_filename = f"certificate_{safe_name}.tex"
            pdf_filename = f"certificate_{safe_name}.pdf"
            
            # Write LaTeX file
            with open(latex_filename, 'w', encoding='utf-8') as f:
                f.write(individual_latex)
            
            # Compile to PDF
            try:
                result = subprocess.run(
                    ["xelatex", "-interaction=nonstopmode", latex_filename],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0 and os.path.exists(pdf_filename):
                    # Move PDF to output directory
                    pdf_destination = os.path.join(output_dir, pdf_filename)
                    shutil.move(pdf_filename, pdf_destination)
                    generated_pdfs.append(pdf_destination)
                    
                    # Clean up auxiliary files
                    for ext in ['.aux', '.log', '.out']:
                        aux_file = f"certificate_{safe_name}{ext}"
                        if os.path.exists(aux_file):
                            os.remove(aux_file)
                    
                    print(f"Generated: {pdf_destination}")
                else:
                    print(f"Failed to generate PDF for {name}")
                    
            except Exception as e:
                print(f"Error generating PDF for {name}: {e}")
            
            # Clean up LaTeX file
            if os.path.exists(latex_filename):
                os.remove(latex_filename)
        
        return generated_pdfs


def main():
    """Example usage of the CertificateGenerator."""
    generator = CertificateGenerator()
    
    # Check if names.csv exists and generate certificates from it
    csv_file = "names.csv"
    if os.path.exists(csv_file):
        print("Generating certificates from names.csv...")
        
        # Generate individual certificates for each person
        print("Generating individual certificates...")
        individual_pdfs = generator.generate_individual_certificates_from_csv(
            csv_file,
            lastname_column="Lastname",
            name_column="Name",
            completion_date_column="completion_date",
            output_dir="pdfs"
        )
        print(f"Generated {len(individual_pdfs)} individual certificates in pdfs/ folder")
        
        # Also generate a combined PDF with all certificates
        print("Generating combined certificate file...")
        output_file = generator.generate_certificates_from_csv(
            csv_file, 
            lastname_column="Lastname",
            name_column="Name",
            completion_date_column="completion_date",
            output_file="certificates.tex"
        )
        print(f"Generated LaTeX file: {output_file}")
        
        # Compile to PDF
        print("Compiling combined PDF...")
        try:
            import subprocess
            result = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "certificates.tex"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("PDF compilation successful!")
                
                # Move PDF to pdfs folder
                if os.path.exists("certificates.pdf"):
                    import shutil
                    pdf_destination = os.path.join("pdfs", "all_certificates.pdf")
                    shutil.move("certificates.pdf", pdf_destination)
                    print(f"Combined PDF saved to: {pdf_destination}")
                    
                    # Clean up auxiliary files
                    for ext in ['.aux', '.log', '.out']:
                        aux_file = f"certificates{ext}"
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
            "Mario Eduardo Archila Meléndez",
            "John Doe",
            "Jane Smith",
            "Alice Johnson",
            "Bob Wilson"
        ]
        
        print("Generating certificates from example list...")
        output_file = generator.generate_certificates_from_list(names)
        print(f"Generated: {output_file}")


if __name__ == "__main__":
    main() 