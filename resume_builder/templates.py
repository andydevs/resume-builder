"""
Next Priority : Let's making something that will make our PDF
    We'll make it barebones to start with : 
        Let's have at most 5 sections:
            - Header, Skills, Work Experience, Relevant Projects, Education 
"""
from fpdf import FPDF
import logging

logger = logging.getLogger('template')

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
    def __init__(self,
        max_experience=7,
        max_skills=7,
        display_project_skills=False,
        header_font_size=12,
        body_font_size=10.5,
        title_font_size=20,
        font='Helvetica',
        linespace=6):
        """
        Initialize
        """
        self.max_experience = max_experience
        self.max_skills = max_skills
        self.display_project_skills = display_project_skills
        self.linespace = linespace
        self.header_font_size = header_font_size
        self.body_font_size = body_font_size
        self.title_font_size = title_font_size
        self.font = font
        super().__init__()

    def build_experience(self, cv, tags):
        """
        Build truncated list of work experience and project experience
        """
        logger.info('Build experience')
        filtered_jobs = cv.jobs[cv.jobs.tags.apply(lambda x: any(k in x for k in tags))]
        logger.debug('After filtered tags: \n%s', filtered_jobs)
 
        # Holders for work and project experience
        experience = { 'work': {}, 'projects': {} }

        # Get work experiences up to max_list
        work_items = filtered_jobs[filtered_jobs.type == 'J'].head(self.max_experience)
        work_items['date'] = self._format_experience_date_ranges(work_items)
        work_items = work_items[['company', 'title', 'location', 'date', 'detail']]
        logger.debug('Work experience items: \n%s', work_items)
        experience['work'] = work_items.set_index('company').to_dict('index')

        # Add project experience if no. work items < max_list
        if len(work_items) < self.max_experience:
            project_items = filtered_jobs[filtered_jobs.type == 'P']
            project_items = project_items.head(self.max_experience - len(work_items))
            project_items['date'] = self._format_experience_date_ranges(project_items)
            project_items = project_items[['title', 'date', 'skills', 'detail']]
            if not self.display_project_skills:
                # Drop skills column if we're not displaying it
                project_items = project_items.drop(columns=['skills'])
            logger.debug('Project experience items: \n%s', project_items)
            experience['projects'] = project_items.set_index('title').to_dict('index')

        # Return experience
        logger.info('Experience Dict: %s', experience)
        return experience
        
    def build_skills(self, cv):
        """
        Build truncated lists of skills
        """
        logger.info('Build skills')
        trunc_skills = { group:skills[:self.max_skills] for group, skills in cv.skills.items() }
        logger.info('Truncated skills: %s', trunc_skills)
        return trunc_skills

    def _format_experience_date_ranges(self, item):
        """
        Work experience and project experience date range formatting
        (e.g. June 2020 - Present, April 2018 - August 2018)
        """
        date_format = '%B %Y'
        start_str = item.start.dt.strftime(date_format)
        end_str = item.end.dt.strftime(date_format).fillna('Present')
        return f'{start_str} - {end_str}'

    def head(self, cv):
        """
        Build header
        """
        self.set_font(self.font, 'B', self.title_font_size)
        w = self.get_string_width(cv.name) + 6
        self.set_x((210 - w) / 2)
        self.set_text_color(66, 81, 245)
        self.cell(w, 7, txt=cv.name, align='C', new_y='NEXT')
        self.set_text_color(39, 39, 46)
        self.ln(0.5)
        self.set_font(self.font, size=self.body_font_size)
        if type(cv.subheader_info) is list:
            bullet = ' **\u00b7** '
            cv.subheader_info = bullet.join(cv.subheader_info)
        self.cell(0, 5, txt=cv.subheader_info, align='C', new_y="NEXT", new_x="LMARGIN", markdown=True)
        
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

    def skills(self, cv):
        """
        Skills sections
        """
        self.section_header('**Skills**')
        for skill in cv.skills:
            self.set_font(self.font, 'B', self.body_font_size)
            self.cell(0, self.linespace, skill + ': ', align='L', new_x="END")
            self.set_font(self.font, '', self.body_font_size)
            skill_string = ', '.join(cv.skills.get(skill))
            self.multi_cell(0, self.linespace, skill_string, new_x="LMARGIN", new_y="NEXT", align='L')
        self.ln(1)
        
    def work_exp(self, cv, tags):
        """
        Work experience sections
        """
        w_exp = self.build_experience(cv, tags)['work']
        if not w_exp: return
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

    def proj_exp(self, cv, tags):
        """
        Project experience sections
        """
        p_exp = self.build_experience(cv, tags)['projects']
        if not p_exp: return
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

    def education(self, cv):
        """
        Education sections
        """
        self.section_header('**Education**')
        for degree in cv.education:
            self.set_font(self.font, 'B', self.body_font_size)
            self.cell(0, self.linespace, degree, new_x="END", new_y="NEXT", align='L')
            self.set_font(self.font, '', self.body_font_size)
            degree_info = cv.education.get(degree)
            address = degree_info.get('address')
            date = degree_info.get('completed')
            gpa = degree_info.get('GPA')
            self.cell(0, self.linespace, date + ' | ' + gpa, new_x="LMARGIN", align='R')
            self.cell(0, self.linespace, address , new_x="LMARGIN", new_y="NEXT", align='L')
        self.ln(1)
    
    def apply(self, cv, tags):
        """
        Build resume
        """
        self.add_page()
        self.head(cv)
        self.education(cv)
        self.skills(cv)
        self.proj_exp(cv, tags)
        self.work_exp(cv, tags)