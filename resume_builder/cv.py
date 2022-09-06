import pandas as pd
from .templates import *
import logging
import yaml

# Get logger
logger = logging.getLogger('cv')

class cv: 
    """
    Contains information for CV
    """
    def __init__(self, name, subheader_info, education, skills, jobs):
        """
        Initialize cv
        """
        self.name = name
        self.subheader_info = subheader_info
        self.education = education
        self.skills = skills
        self.jobs = jobs
        logger.info('CV Processed')
        logger.info('  name: %s', self.name)
        logger.info('  subheader_info: %s', self.subheader_info)
        logger.info('  skills:')
        for category, items in self.skills.items():
            logger.info('    %s: %s', category, items)
        logger.info('  education:')
        for title, detail in self.education.items():
            logger.info('    %s', title)
            logger.info('      address: %s', detail['address'])
            logger.info('      completed: %s', detail['completed'])
            logger.info('      GPA: %s', detail['GPA'])
        logger.info('  jobs:\n%s', self.jobs)


def cv_from_yaml(fname):
    """
    Generate cv from YAML file
    """
    with open (fname, 'r') as f:
        data = yaml.safe_load(f)
    skills = data['skills']
    name = data['name']
    address = data['subheader_info']
    education = data['education']
    jobs = pd.DataFrame.from_records(data['experience'])
    jobs['start'] = pd.to_datetime(jobs['start'])
    jobs['end'] = pd.to_datetime(jobs['end'])
    jobs['type'] = jobs['type'].str.upper()
    jobs = jobs.sort_values('start', ascending=False)
    return cv(name, address, education, skills, jobs)


def cv_from_csv(fjobs, fskills, basic_info):
    """
    Generate cv from csv files
    """
    jobs = pd.read_csv(fjobs)
    jobs.tags = jobs.tags.apply(lambda x: x.split(', '))
    jobs.detail = jobs.detail.apply(lambda x: x.split(', '))
    jobs['start'] = pd.to_datetime(jobs['start'])
    jobs['end'] = pd.to_datetime(jobs['end'])
    jobs = jobs.sort_values('start', ascending = False)
    jobs['type'] = jobs['type'].apply(lambda x: x.upper())
    basic = pd.read_csv(basic_info)
    basic.edu_1 = basic.edu_1.apply(lambda x:str(x).split('/ '))
    education = {
        basic.edu_1.item()[0]: 
        {
            'address':basic.edu_1.item()[1], 
            'completed': basic.edu_1.item()[2],
            'GPA': basic.edu_1.item()[3]
        }
    }
    address = basic.address.item()
    skills = pd.read_csv(fskills)
    for col in skills:
        skills[col] = skills[col].apply(lambda x: x.split(', '))
    skills = skills.to_dict()
    for i in skills:
        skills[i] = skills[i][0]
    name = basic.name.item()
    return cv(name, address, education, skills, jobs)