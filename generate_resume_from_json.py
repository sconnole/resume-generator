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
        if data["should_add_clearance"] is True:
            self.cell(
                0,
                6,
                "Active Security Clearance: Top Secret",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
                align="C",
            )
        self.ln(4)

    def section_title(self, title):
        self.set_font("Verdana", "B", 10)
        page_width = self.w - self.l_margin - self.r_margin
        self.cell(page_width, 8, title.upper(), border=1, ln=1, align="C", fill=False)
        self.ln(2)

    def add_summary(self, summary):
        self.set_font("Verdana", "", 9)
        self.multi_cell(0, 5.5, sanitize(summary), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

    def add_job(self, job):
        self.set_font("Verdana", "B", 9)
        self.cell(0, 5, sanitize(job["company"]), new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_xy(150, self.get_y())
        self.cell(
            0, 5, sanitize(job["dates"]), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )

        self.set_font("Verdana", "I", 9)

        if "title" in job:
            self.cell(0, 5, sanitize(job["title"]), new_x=XPos.RIGHT, new_y=YPos.TOP)
        if "location" in job:
            self.set_xy(150, self.get_y())
            self.cell(
                0,
                5,
                sanitize(job["location"]),
                align="R",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )

        responsibilities = job.get("responsibilities", [])
        if responsibilities:
            for bullet in responsibilities:
                try:
                    self.cell(5)
                    self.multi_cell(
                        0,
                        5.5,
                        "- " + sanitize(bullet),
                        new_x=XPos.LMARGIN,
                        new_y=YPos.NEXT,
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
        self.cell(0, 5, sanitize(edu["description"]), new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_xy(150, self.get_y())
        self.cell(
            0,
            5,
            f'Graduation Date: {edu["graduation_date"]}',
            align="R",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

        self.ln(2)

    def add_skills(self, skills):
        def render_skill_section(title, items):
            if items:
                self.set_font("Verdana", "B", 8)
                self.cell(26, 5, f"{title}:")

                self.set_font("Verdana", "", 8)
                self.multi_cell(0, 5, ", ".join(items))
                self.ln(1)

        render_skill_section("Leadership", skills.get("leadership"))
        render_skill_section("Code", skills.get("code"))
        render_skill_section("Infrastructure", skills.get("infrastructure"))
        render_skill_section("Interests", skills.get("interests"))


with open("./leadership-experience.json", "r") as f:
    data = json.load(f)

pdf = ResumePDF()
pdf.set_margins(left=8, top=5, right=8)
pdf.set_auto_page_break(auto=True, margin=10)

pdf.add_font("Verdana", "", "fonts/Verdana.ttf")
pdf.add_font("Verdana", "B", "fonts/Verdana Bold.ttf")
pdf.add_font("Verdana", "I", "fonts/Verdana Italic.ttf")
pdf.add_font("Verdana", "BI", "fonts/Verdana Bold Italic.ttf")

pdf.add_page()

# Summary
if "summary" in data:
    pdf.section_title("Summary")
    pdf.add_summary(data["summary"])

# Professional Experience
pdf.section_title("Professional Experience")
for job in data["professional_experience"]:
    pdf.add_job(job)

# Entrepreneurial Work
if "entrepreneurial_experience" in data:
    pdf.section_title("Entrepreneurial Work")
    pdf.add_job(data["entrepreneurial_experience"])

# Education
if "education" in data:
    pdf.section_title("Education")
    for education in data["education"]:
        pdf.add_education(education)

if "extracurricular_activities" in data:
    pdf.section_title("Extracurricular Activities")
    for activity in data["extracurricular_activities"]:
        pdf.add_job(activity)

# Skills
if "skills" in data:
    pdf.section_title("Skills & Interests")
    pdf.add_skills(data["skills"])

# Output file
pdf.output("Sean-Connole-Resume.pdf")
