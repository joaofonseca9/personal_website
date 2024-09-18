from bs4 import BeautifulSoup
import os

def extract_content_from_rendered_html(html_file):
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    about = soup.find(id="about").text if soup.find(id="about") else ""
    experience = [exp.text for exp in soup.find_all(class_="experience-item")]
    education = [edu.text for edu in soup.find_all(class_="education-item")]
    skills = [skill.text for skill in soup.find_all(class_="skill-item")]

    return {
        "about": about,
        "experience": experience,
        "education": education,
        "skills": skills
    }

def create_latex_cv(content):
    latex_template = r"""
    \documentclass[a4paper,10pt]{article}
    \usepackage{geometry}
    \geometry{top=1in, bottom=1in, left=1in, right=1in}
    \usepackage{enumitem}
    \begin{document}

    \title{Curriculum Vitae}
    \author{Your Name}
    \date{\today}
    \maketitle

    \section*{About}
    """ + content['about'] + r"""

    \section*{Experience}
    \begin{itemize}
    """
    
    for exp in content['experience']:
        latex_template += r"\item " + exp + "\n"
    
    latex_template += r"""
    \end{itemize}

    \section*{Education}
    \begin{itemize}
    """
    
    for edu in content['education']:
        latex_template += r"\item " + edu + "\n"
    
    latex_template += r"""
    \end{itemize}

    \section*{Skills}
    \begin{itemize}
    """
    
    for skill in content['skills']:
        latex_template += r"\item " + skill + "\n"
    
    latex_template += r"""
    \end{itemize}
    \end{document}
    """
    
    with open("cv.tex", "w") as file:
        file.write(latex_template)



def convert_latex_to_pdf(latex_file):
    os.system(f"pdflatex {latex_file}")

# Usage
content = extract_content_from_rendered_html("_layouts/front.html")
create_latex_cv(content)
convert_latex_to_pdf("cv.tex")
