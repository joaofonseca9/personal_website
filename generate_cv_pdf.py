#!/usr/bin/env python3
"""
Generate a Harvard-style CV PDF from _data/data.yml using LaTeX.

This script reads the CV data from the Jekyll data file and generates
a professional PDF in the Harvard CV format with a blue header bar.
"""

import os
import shutil
import subprocess

import yaml

def load_cv_data(yaml_path="_data/data.yml"):
    """Load CV data from YAML file."""
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def escape_latex(text):
    """Escape special LaTeX characters."""
    if text is None:
        return ""
    text = str(text)
    # Order matters - escape backslash first
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text

def format_details(details):
    """Format experience details as LaTeX itemize list."""
    if not details:
        return ""

    lines = []
    for line in details.strip().split('\n'):
        line = line.strip()
        if line.startswith('- '):
            line = line[2:]  # Remove the markdown bullet
        if line:
            lines.append(f"    \\item {escape_latex(line)}")

    if not lines:
        return ""

    return "\\begin{itemize}[leftmargin=*, nosep]\n" + "\n".join(lines) + "\n  \\end{itemize}"

def generate_latex(data, config):
    """Generate LaTeX document from CV data."""

    # Contact info from config
    name = config.get('title', 'João Fonseca')
    email = config.get('email', 'joaopbf9@hotmail.com')
    phone = '+351 916 477 261'
    location = 'Porto, Portugal'
    github_username = config.get('github_username', 'joaofonseca9')
    website = f'{github_username}.github.io'

    # Profile info from data
    profile = data.get('profile', {})
    photo_path = profile.get('photo', 'img/profile.jpg')
    linkedin_url = profile.get('linkedin', 'https://www.linkedin.com/in/joão-fonseca-69b438189/')
    github_url = profile.get('github', f'https://github.com/{github_username}')

    # Check if profile photo exists
    has_photo = os.path.exists(photo_path)

    latex = r"""\documentclass[a4paper,10pt]{article}

% Packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{parskip}

% Page geometry
\geometry{top=0.6in, bottom=0.6in, left=0.7in, right=0.7in}

% Colors
\definecolor{darkblue}{RGB}{0, 51, 102}
\definecolor{linkblue}{RGB}{0, 102, 204}

% Hyperlinks
\hypersetup{
    colorlinks=true,
    linkcolor=linkblue,
    urlcolor=linkblue,
}

% Section formatting
\titleformat{\section}
  {\large\bfseries\color{darkblue}}
  {}
  {0em}
  {}
  [\titlerule]

\titlespacing*{\section}{0pt}{12pt}{6pt}

% Custom commands
\newcommand{\cvsection}[1]{\section*{#1}}

\begin{document}

% Header
\begin{center}
{\Huge\bfseries """ + escape_latex(name) + r"""} \\[0.3cm]
{\large """ + escape_latex(data.get('header', {}).get('subtitle', 'Product Owner / Data Engineer')) + r"""} \\[0.3cm]
""" + escape_latex(email) + r""" $\cdot$ """ + escape_latex(phone) + r""" $\cdot$ """ + escape_latex(location) + r""" \\
\href{https://""" + website + r"""}{""" + escape_latex(website) + r"""} $\cdot$ \href{""" + linkedin_url + r"""}{LinkedIn} $\cdot$ \href{""" + github_url + r"""}{GitHub}
\end{center}

\vspace{0.3cm}

% About Me
\cvsection{About Me}
""" + escape_latex(data.get('about', '').strip()) + r"""

% Experience
\cvsection{Experience}
"""

    # Add experiences
    experiences = data.get('experiences', {}).get('info', [])
    for i, exp in enumerate(experiences):
        role = escape_latex(exp.get('role', ''))
        time = escape_latex(exp.get('time', ''))
        company = escape_latex(exp.get('company', ''))
        details = exp.get('details', '')

        latex += f"""
\\textbf{{{role}}} \\hfill {time} \\\\
\\textit{{{company}}}
{format_details(details)}
"""
        if i < len(experiences) - 1:
            latex += "\\vspace{0.3cm}\n"

    # Education
    latex += r"""
\cvsection{Education}
"""
    education = data.get('education', {}).get('info', [])
    for edu in education:
        degree = escape_latex(edu.get('degree', ''))
        university = escape_latex(edu.get('university', ''))
        time = escape_latex(edu.get('time', ''))
        gpa = escape_latex(edu.get('gpa', ''))

        latex += f"""
\\textbf{{{university}}} | {degree} \\hfill {time} \\\\
GPA: {gpa}
"""

    # Certifications
    certifications = data.get('education', {}).get('certifications', [])
    if certifications:
        latex += r"""
\cvsection{Certifications}
"""
        for cert in certifications:
            name = escape_latex(cert.get('name', ''))
            issuer = escape_latex(cert.get('issuer', ''))
            time = escape_latex(str(cert.get('time', '')))
            details = escape_latex(cert.get('details', ''))

            latex += f"\\textbf{{{name}}} | {issuer} \\hfill {time} \\\\\n"
            if details:
                latex += f"{details}\n\n"

    # Skills
    latex += r"""
\cvsection{Skills}
"""
    skills = data.get('skills', {})

    # Software skills
    software = skills.get('software', [])
    if software:
        skill_items = []
        for cat in software:
            items = cat.get('items', [])
            for item in items:
                if isinstance(item, dict):
                    skill_items.append(item.get('name', ''))
                else:
                    skill_items.append(str(item))
        latex += "\\textbf{Software:} " + escape_latex(" | ".join(skill_items)) + "\n\n"

    # Technical skills
    technical = skills.get('technical', [])
    if technical:
        latex += "\\textbf{Technical Areas:} " + escape_latex(" | ".join(technical)) + "\n\n"

    # Publications
    latex += r"""
\cvsection{Publications}
"""
    publications = data.get('publications', [])
    for pub in publications:
        title = escape_latex(pub.get('title', ''))
        journal = escape_latex(pub.get('journal', ''))
        year = pub.get('year', '')
        role = escape_latex(pub.get('role', ''))
        access = escape_latex(pub.get('access', ''))

        latex += f"""\\textbf{{"{title}"}} \\\\
{journal} ({year}) - {role}, Published, {access}

"""

    # Awards
    latex += r"""
\cvsection{Awards}
"""
    awards = data.get('awards', [])
    for award in awards:
        title = escape_latex(award.get('title', ''))
        description = escape_latex(award.get('description', ''))
        year = award.get('year', '')

        latex += f"\\textbf{{{title}}}, \"{description}\", {year}\n"

    latex += r"""
\end{document}
"""

    return latex

def load_config(config_path="_config.yml"):
    """Load Jekyll config."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def generate_pdf(output_dir="."):
    """Generate the PDF from the LaTeX file."""
    # Load data
    data = load_cv_data()
    config = load_config()

    # Generate LaTeX
    latex_content = generate_latex(data, config)

    # Write LaTeX file
    tex_file = os.path.join(output_dir, "cv_harvard.tex")
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(latex_content)

    print(f"Generated LaTeX file: {tex_file}")

    # Check if pdflatex is available
    latex_cmd = None
    if shutil.which("pdflatex"):
        latex_cmd = "pdflatex"
    elif shutil.which("lualatex"):
        latex_cmd = "lualatex"

    if latex_cmd is None:
        print("Warning: No LaTeX compiler found. LaTeX file generated but PDF not created.")
        print("Install TeX Live or MiKTeX to generate PDF locally.")
        return tex_file

    print(f"Using {latex_cmd} to compile PDF...")

    # Run latex twice for proper formatting
    for i in range(2):
        result = subprocess.run(
            [latex_cmd, "-interaction=nonstopmode", "-output-directory", output_dir, tex_file],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            print(f"{latex_cmd} error (pass {i+1}):")
            print(result.stdout)
            print(result.stderr)

    # Clean up auxiliary files
    for ext in ['.aux', '.log', '.out']:
        aux_file = os.path.join(output_dir, f"cv_harvard{ext}")
        if os.path.exists(aux_file):
            os.remove(aux_file)

    pdf_file = os.path.join(output_dir, "cv_harvard.pdf")
    if os.path.exists(pdf_file):
        print(f"Generated PDF: {pdf_file}")
        return pdf_file
    else:
        print("PDF generation failed. Check the LaTeX file for errors.")
        return tex_file

if __name__ == "__main__":
    generate_pdf()
