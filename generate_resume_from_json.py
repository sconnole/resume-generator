import json
from fpdf import FPDF
from fpdf.enums import XPos, YPos


def sanitize(text):
    if not isinstance(text, str):
        return ""
    # Replace dashes and bullets with ASCII-friendly chars
    return text.replace("–", "-").replace("—", "-").replace("\u2022", "-")


class ResumePDF(FPDF):
    def header(self):
        self.set_font("Verdana", "B", 12)
        self.cell(
            0, 8, sanitize(data["name"]), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C"
        )
        self.set_font("Verdana", "", 9)
        contact = data["contact"]
        self.cell(
            0,
            6,
            f'{contact["phone"]} | {contact["email"]} | {contact["linkedin"]}',
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align="C",
        )
        self.ln(4)

    def section_title(self, title):
        self.set_font("Verdana", "B", 11)
        self.cell(0, 6, title.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.line(self.l_margin, self.get_y(), 200, self.get_y())
        self.ln(2)

    def add_job(self, job):
        # Header row: Company on left, Dates on right
        self.set_font("Verdana", "B", 9)
        self.cell(0, 5, sanitize(job["company"]), new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_xy(150, self.get_y())
        self.cell(
            0, 5, sanitize(job["dates"]), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )

        # Second row: Title (italic) on left, Location (italic) on right
        self.set_font("Verdana", "I", 9)
        self.cell(0, 5, sanitize(job["title"]), new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_xy(150, self.get_y())
        self.cell(
            0,
            5,
            sanitize(job["location"]),
            align="R",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

        # Bullets with safe rendering
        self.set_font("Verdana", "", 9)
        for bullet in job["responsibilities"]:
            if not isinstance(bullet, str):
                continue
            try:
                self.cell(5)  # indent
                self.multi_cell(
                    0, 5.5, "- " + sanitize(bullet), new_x=XPos.LMARGIN, new_y=YPos.NEXT
                )
            except Exception as e:
                self.cell(5)
                self.multi_cell(
                    0, 5.5, "- [Content error]", new_x=XPos.LMARGIN, new_y=YPos.NEXT
                )
                print("⚠️ Error rendering bullet:", bullet)
                print(e)
        self.ln(1)

    def add_education(self, edu):
        self.set_font("Verdana", "B", 9)
        self.cell(0, 5, sanitize(edu["degree"]), new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_xy(150, self.get_y())
        self.cell(
            0,
            5,
            f'Graduation Date: {edu["graduation_date"]}',
            align="R",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

        self.set_font("Verdana", "I", 9)
        self.cell(
            0, 5, sanitize(edu["institution"]), new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
        self.ln(3)

    def add_skills(self, skills):
        self.set_font("Verdana", "", 8)
        skill_text = ", ".join(
            skills["backend"]
            + skills["frontend"]
            + skills["infrastructure_devops"]
            + skills["databases"]
        )
        self.cell(5)  # indent
        self.multi_cell(
            0, 5.5, "- " + sanitize(skill_text), new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
        self.ln(1)


# Load data from JSON
with open("./experience.json", "r") as f:
    data = json.load(f)

# Create PDF
pdf = ResumePDF()
pdf.set_margins(left=8, top=5, right=8)

# Add fonts BEFORE adding pages!
pdf.add_font("Verdana", "", "fonts/Verdana.ttf")
pdf.add_font("Verdana", "B", "fonts/Verdana Bold.ttf")
pdf.add_font("Verdana", "I", "fonts/Verdana Italic.ttf")
pdf.add_font("Verdana", "BI", "fonts/Verdana Bold Italic.ttf")

pdf.add_page()

# Work Experience
pdf.section_title("Professional Experience")
for job in data["professional_experience"]:
    pdf.add_job(job)

# Entrepreneurial Work
pdf.section_title("Entrepreneurial Work")
pdf.add_job(data["entrepreneurial_experience"])

pdf.section_title("Education")
pdf.add_education(data["education"])

pdf.section_title("Skills & Technical Stack")
pdf.add_skills(data["skills"])

# Output file
pdf.output("Sean-Connole-Resume.pdf")
