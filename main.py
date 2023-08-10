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


# Argument parser
parser = argparse.ArgumentParser(description='Generate a resume. Filter experience based on input tags')
parser.add_argument('--tags', '-t', metavar='TAG', action='store', nargs='+', type=str, required=True, help='Tags to filter for')
parser.add_argument('--input', '-i', action='store', type=str, required=True, help='Input YAML file')
parser.add_argument('--output', '-o', action='store', type=str, required=True, help='Output file name')
parser.add_argument('--max-experience', '-e', type=int, required=False, default=7, help='Maximum experience')
parser.add_argument('--max-skills', '-s', type=int, required=False, default=7, help='Maximum skills shown in skill section')
parser.add_argument('--debug', '-d', action='store_true', help='Print debug logging')
args = parser.parse_args()