from fpdf import FPDF


class FPDFResumeTemplate:
    """
    Build resume using FPDF
    """
    font = 'Helvetica'
    bullet = '-'
    MONTHS = [
        'January', 'February', 'March',
        'April', 'May', 'June',
        'July', 'August', 'September',
        'October', 'November', 'December'
    ]

    def title(self, resume):
        """
        Build the PDF title
        """
        # Name
        self.pdf.set_font(family=self.font, style='B', size=32)
        self.pdf.cell(txt=resume['name'], ln=1, h=15)

        # Emails
        self.pdf.set_font(family=self.font, size=11)
        for contact in resume['contact'].values():
            self.pdf.cell(txt=contact, ln=1, h=5)

    def education(self, resume):
        """
        Build education
        """
        self._heading('Education')
        for level in resume['education']:
            self._line(level['degree'])
            self._line(level['school']['title'])
            self._line(f"Completed {level['completed']['month']} {level['completed']['year']}")
            self._line(f"GPA {level['GPA']}")

    def skills(self, resume):
        """
        Build skills section
        """
        self._heading('Skills')
        self.pdf.set_font(family=self.font, size=11)
        with self.pdf.table(first_row_as_headings=False,
                            col_widths=(40,100),
                            line_height=6, 
                            gutter_height=2, 
                            borders_layout='NONE') as table:
            for group in resume['skills']:
                row = table.row()
                self.pdf.set_font(style='B')
                row.cell(group['group'], v_align='T')
                self.pdf.set_font()
                row.cell('\n'.join(f'{self.bullet} {skill}' for skill in group['skills']), v_align='T')

    def projects(self, resume):
        """
        Build projects section
        """
        self._heading('Projects')
        for project in resume['projects']:
            self._subheading(project['title'])
            self._line(' '.join(project['skills']), style='I')
            self._spacer()
            self._bulletlist(project['details'])

    def experience(self, resume):
        """
        Build experience section
        """
        self._heading('Experience')
        for job in resume['experience']:
            self._subheading(job['title'])
            self._line(job['company'])
            date = lambda d: 'Present' if d.get('present', False) else f"{self.MONTHS[d['month'] - 1]} {d['year']}"
            self._line(f"{date(job['start'])} - {date(job['end'])}", style='I')
            self._line(' '.join(job['skills']), style='I')
            self._spacer()
            self._bulletlist(job['detail'])

    def _heading(self, txt):
        """
        Write a heading
        """
        self.pdf.set_font(family=self.font, style='B', size=18)
        self.pdf.cell(txt=txt, ln=1, h=14)

    def _subheading(self, txt):
        """
        Write a subheading
        """
        self.pdf.set_font(family=self.font, style='B', size=14)
        self.pdf.cell(txt=txt, ln=1, h=10)

    def _line(self, txt, style=''):
        """
        Write a line
        """
        self.pdf.set_font(family=self.font, style=style, size=11)
        self.pdf.cell(txt=txt, ln=1)

    def _bulletlist(self, items):
        """
        Write out a flat bulleted list
        """
        for item in items:
            self.pdf.set_font(family=self.font, size=11)
            self.pdf.cell(txt=f'{self.bullet} {item}', ln=1)

    def _spacer(self):
        """
        Print a spacer
        """
        self.pdf.cell(h=2, w=10, ln=1)

    def compile(self, resume):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.title(resume)
        self.education(resume)
        self.skills(resume)
        self.projects(resume)
        self.experience(resume)
        return self.pdf