"""
Eventual Goal for this file is to run everything to the command line

Arguments:
   - data 
   - template
   - max_experience
   - max_skills
   - display_project_skills 
   - file name
   - keys
"""
import argparse
from . import Template


# Argument parser
parser = argparse.ArgumentParser(prog='py -m resume_builder',
                                 description='Generate a resume. Filter experience based on input tags')
parser.add_argument('input',            type=str, help='Input YAML file')
parser.add_argument('--tags',           '-t', metavar='TAG', nargs='+', type=str, required=False, help='Tags to filter for')
parser.add_argument('--output',         '-o', type=str, required=False, help='Output file name')
parser.add_argument('--max-experience', '-e', type=int, required=False, default=7, help='Maximum experience')
parser.add_argument('--max-skills',     '-s', type=int, required=False, default=7, help='Maximum skills shown in skill section')
parser.add_argument('--debug',          '-d', action='store_true', help='Print debug logging')


if __name__ == '__main__':
   args = parser.parse_args()
   output = args.output or args.input.replace('.yaml', '.pdf')
   resume = Template()
   resume.output(output)