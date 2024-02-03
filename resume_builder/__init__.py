import argparse
from .template.fpdf import FPDFResumeTemplate
import os.path
import yaml


def run_program():
    """
    Run program
    """
    # Argument parser
    parser = argparse.ArgumentParser(prog='py -m resume_builder',
                                    description='Generate a resume. Filter experience based on input tags')
    parser.add_argument('input',            type=str, help='Input YAML file')
    parser.add_argument('--tags',           '-t', metavar='TAG', nargs='+', type=str, required=False, help='Tags to filter for')
    parser.add_argument('--output',         '-o', type=str, required=False, help='Output file name')
    parser.add_argument('--max-experience', '-e', type=int, required=False, default=7, help='Maximum experience')
    parser.add_argument('--max-skills',     '-s', type=int, required=False, default=7, help='Maximum skills shown in skill section')
    parser.add_argument('--debug',          '-d', action='store_true', help='Print debug logging')

    # Arguments
    args = parser.parse_args()
    input_path = args.input
    output = args.output or os.path.basename(input_path).replace('.yaml', '.pdf')

    # Load data
    with open(input_path, 'r') as f:
        resume = yaml.safe_load(f)

    # Build resume
    template = FPDFResumeTemplate()
    pdf = template.compile(resume)
    pdf.output(output)