"""
Next Priority : Let's making something that will make our PDF
    We'll make it barebones to start with : 
        Let's have at most 5 sections:
            - Header, Skills, Work Experience, Relevant Projects, Education 
"""
from fpdf import FPDF

class template_basic(FPDF):
    """
    Default Colors: 
        Headers (Blue) : 66, 81, 245 
        Texts (Grey) : 39, 39, 46
    
    Let's assume that all of our data is going to be thrown in as a dictionary --

    input format: 
        jobs = { 
            company : {
                'location' : string,
                'title' : string,
                'date' : string (month year),
                'detail' : list },
        }

        projects ={
            project name : {
                'date' : string (month year), 
                'detail' : list,
                'skills' : string, (optional)
            } 
        }

        skills = {
            skill_1 : string,
            skill_2 : string,
            skill_3 : string,..., 
            skill_n : string
        }
    """
    linespace = 6

    def head(self, name, address):
        """
        Build header
        """
        self.set_font(self.font, 'B', self.title_font_size)
        w = self.get_string_width(name) + 6
        self.set_x((210 - w) / 2)
        self.set_text_color(66, 81, 245)
        self.cell(w, 7, txt=name, align='C', new_y='NEXT')
        self.set_text_color(39, 39, 46)
        self.ln(0.5)
        self.set_font(self.font, size=self.body_font_size)
        if type(address) is list:
            bullet = ' **\u00b7** '
            address = bullet.join(address)
        self.cell(0, 5, txt=address, align='C', new_y="NEXT", new_x="LMARGIN", markdown=True)
        
    def section_header(self, header):
        """
        Create section header for each section
        """
        self.set_font(self.font, size=self.header_font_size)
        self.ln(1)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(66, 81, 245)
        self.cell(0, self.linespace, header, align='L', new_x="LMARGIN", new_y="NEXT", markdown=True)
        x = self.get_x()
        y = self.get_y()
        self.line(x, y, 200, y)
        self.ln(1)
        self.set_text_color(39, 39, 46)

    def skills(self, skills):
        """
        Skills sections
        """
        self.section_header('**Skills**')
        for skill in skills:
            self.set_font(self.font, 'B', self.body_font_size)
            self.cell(0, self.linespace, skill + ': ', align='L', new_x="END")
            self.set_font(self.font, '', self.body_font_size)
            skill_string = ', '.join(skills.get(skill))
            self.multi_cell(0, self.linespace, skill_string, new_x="LMARGIN", new_y="NEXT", align='L')
        self.ln(1)
        
    def work_exp(self, w_exp):
        """
        Work experience sections
        """
        self.section_header('**Professional Experience**')
        for company in w_exp:
            info = w_exp.get(company)
            date_location = info.get('location') + ', ' + info.get('date') 
            title = info.get('title')
            self.set_font(self.font, 'B', self.body_font_size)
            self.cell(0, self.linespace, title, align='L', new_y="NEXT", new_x="LMARGIN")
            self.cell(0, self.linespace - 1, company, align='L')
            self.set_font(self.font, size=self.body_font_size)
            self.cell(0, self.linespace - 1, txt=date_location, align='R', new_x="LMARGIN", new_y="NEXT", markdown=True)
            self.set_font(self.font, size=self.body_font_size)
            for detail in info.get('detail'):
                self.set_x(self.get_x() + 5)
                self.multi_cell(0, self.linespace, txt=f'\u00b7 {detail}', align='L', new_y="NEXT", new_x="LMARGIN", markdown=True)
            self.ln(.5)
        self.ln(1)

    def proj_exp(self, p_exp):
        """
        Project experience sections
        """
        self.section_header('**Relevant Projects**')
        for project in p_exp:
            info = p_exp.get(project)
            date = info.get('date')
            self.set_font(self.font, 'B', self.body_font_size)
            if date is None:
                date = ''
            self.cell(0, self.linespace, project, align='L', new_x="END")
            self.set_font(self.font, 'I', self.body_font_size-2)
            if info.get('skills'):
                skills = f"(Skills: {info.get('skills')})"
                self.cell(0, self.linespace, skills, align='L')
            self.set_font(self.font, size=self.body_font_size)
            self.cell(0, self.linespace, txt=date, align='R', new_x="LMARGIN", new_y="NEXT", markdown=True)
            self.set_font(self.font, size=self.body_font_size)
            for detail in info.get('detail'):
                self.set_x(self.get_x() + 5)
                self.multi_cell(0, self.linespace, txt=f'\u00b7 {detail}', align='L', new_y="NEXT", new_x="LMARGIN", markdown=True)
            self.ln(.5)
        self.ln(1)

    def education(self, education):
        """
        Education sections
        """
        self.section_header('**Education**')
        for degree in education:
            self.set_font(self.font, 'B', self.body_font_size)
            self.cell(0, self.linespace, degree, new_x="END", new_y="NEXT", align='L')
            self.set_font(self.font, '', self.body_font_size)
            degree_info = education.get(degree)
            address = degree_info.get('address')
            date = degree_info.get('completed')
            gpa = degree_info.get('GPA')
            self.cell(0, self.linespace, date + ' | ' + gpa, new_x="LMARGIN", align='R')
            self.cell(0, self.linespace, address , new_x="LMARGIN", new_y="NEXT", align='L')
        self.ln(1)
    
    def fill_resume(self, name, address, skills, w_exp, edu, p_exp=None, header_font_size=12, body_font_size=10.5, title_font_size=20, font='Helvetica'):
        """
        Build resume
        """
        self.header_font_size = header_font_size
        self.body_font_size = body_font_size
        self.title_font_size = title_font_size
        self.font = font
        self.add_page()
        self.head(name, address)
        self.education(edu)
        self.skills(skills)
        if p_exp: 
            self.proj_exp(p_exp)
        self.work_exp(w_exp)