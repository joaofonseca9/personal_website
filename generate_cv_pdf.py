#!/usr/bin/env python3
"""
Generate a Harvard-style CV PDF from _data/data.yml using LaTeX.

This script reads the CV data from the Jekyll data file and generates
a professional PDF in the Harvard CV format with a blue header bar.
"""

import yaml
import subprocess
import os
import re
import shutil

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
\usepackage{fontawesome5}
\usepackage{tikz}
\usepackage{parskip}
\usepackage{tabularx}
\usepackage{multicol}
\usepackage{graphicx}

% Page geometry
\geometry{top=0in, bottom=0.7in, left=0.7in, right=0.7in}

% Colors
\definecolor{headerblue}{RGB}{0, 51, 102}
\definecolor{linkblue}{RGB}{0, 102, 204}

% Hyperlinks
\hypersetup{
    colorlinks=true,
    linkcolor=linkblue,
    urlcolor=linkblue,
}

% Section formatting
\titleformat{\section}
  {\large\bfseries\color{headerblue}}
  {}
  {0em}
  {}
  [\titlerule]

\titlespacing*{\section}{0pt}{12pt}{6pt}

% Custom commands
\newcommand{\cvsection}[1]{\section*{#1}}

\begin{document}

% Header with blue background
\begin{tikzpicture}[remember picture,overlay]
\fill[headerblue] (current page.north west) rectangle ([yshift=-3.2cm]current page.north east);
\end{tikzpicture}

% Header content with photo
"""

    if has_photo:
        latex += r"""
\begin{minipage}[t]{0.15\textwidth}
\vspace{0.3cm}
\begin{tikzpicture}
\clip (0,0) circle (1.1cm);
\node at (0,0) {\includegraphics[width=2.2cm]{""" + photo_path + r"""}};
\end{tikzpicture}
\end{minipage}%
\begin{minipage}[t]{0.45\textwidth}
\vspace{0.4cm}
{\Huge\bfseries\color{white} """ + escape_latex(name) + r"""} \\[0.3cm]
{\large\color{white} Product Owner / Data Engineer}
\end{minipage}%
"""
    else:
        latex += r"""
\begin{minipage}[t]{0.55\textwidth}
\vspace{0.4cm}
{\Huge\bfseries\color{white} """ + escape_latex(name) + r"""} \\[0.3cm]
{\large\color{white} Product Owner / Data Engineer}
\end{minipage}%
"""

    latex += r"""
\begin{minipage}[t]{0.40\textwidth}
\vspace{0.4cm}
\raggedleft
\color{white}
\faEnvelope\ \href{mailto:""" + email + r"""}{""" + escape_latex(email) + r"""} \\
\faPhone\ """ + escape_latex(phone) + r""" \\
\faMapMarker*\ """ + escape_latex(location) + r""" \\
\faGlobe\ \href{https://""" + website + r"""}{""" + escape_latex(website) + r"""} \\[0.2cm]
\faLinkedin\ \href{""" + linkedin_url + r"""}{LinkedIn} \quad
\faGithub\ \href{""" + github_url + r"""}{GitHub}
\end{minipage}

\vspace{1.4cm}

% About Me
\cvsection{About Me}
Bioengineer by training, turned data engineer/scientist with a twist on health data product ownership, development and nurturing incredible teams! Working as Product Owner and data engineer/scientist.

In a polarised world, one of the guaranteed common grounds is health. Despite this, it is also a sector that is still lacking in innovation, with healthcare services constantly failing throughout the world being that first care services or even services with secondary use of data.

My goal is to make a positive impact in the world of health data by using it to provide real world value to the patients and healthcare professionals.

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
            skill_items.extend(items)
        latex += "\\textbf{Software:} " + escape_latex(" | ".join(skill_items)) + "\n\n"

    # Technical skills
    technical = skills.get('technical', [])
    if technical:
        latex += "\\textbf{Technical Areas:} " + escape_latex(" | ".join(technical)) + "\n\n"

    # Soft skills
    soft = skills.get('soft', [])
    if soft:
        latex += "\\textbf{Soft Skills:} " + escape_latex(" | ".join(soft)) + "\n"

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
    if shutil.which("pdflatex") is None:
        print("Warning: pdflatex not found. LaTeX file generated but PDF not created.")
        print("Install TeX Live or MiKTeX to generate PDF locally.")
        return tex_file

    # Run pdflatex twice for proper formatting
    for i in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_file],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"pdflatex error (pass {i+1}):")
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
