import os
from datetime import datetime
import xml.etree.ElementTree as ET
from .utils import find_vertical_for_html, build_studio_link


def parse_iso_date(date_string):
    """Parse ISO date string to datetime object"""
    try:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except:
        return None


def find_ora_dates(course_dir, course_info):
    """
    Find all ORA (Open Response Assessment) components and check their dates.
    Returns a list of dicts with ORA date info and flags.
    """
    oras = []
    
    # Parse course dates
    course_start = parse_iso_date(course_info.get('start_date', ''))
    course_end = parse_iso_date(course_info.get('end_date', ''))
    
    if not course_start or not course_end:
        print("DEBUG: Could not parse course dates for ORA check")
        return oras
    
    print(f"DEBUG: Searching for ORA dates")
    print(f"DEBUG: Course date range: {course_start} to {course_end}")
    
    # Search in both draft and non-draft verticals
    for vertical_dir in [
        os.path.join(course_dir, 'course', 'vertical'),
        os.path.join(course_dir, 'course', 'drafts', 'vertical')
    ]:
        if not os.path.exists(vertical_dir):
            continue
        
        for vertical_file in os.listdir(vertical_dir):
            if not vertical_file.endswith('.xml'):
                continue
            
            vertical_path = os.path.join(vertical_dir, vertical_file)
            try:
                tree = ET.parse(vertical_path)
                root = tree.getroot()
                
                # Look for openassessment elements
                for ora_elem in root.findall('.//openassessment'):
                    ora_info = {
                        'display_name': ora_elem.get('display_name', 'Unknown ORA'),
                        'vertical_id': vertical_file.replace('.xml', ''),
                        'vertical_name': root.get('display_name', 'Unknown'),
                        'is_draft': 'drafts' in vertical_dir,
                        'flags': [],
                        'dates': {},
                        'grading_config': {}
                    }
                    
                    # Extract submission dates
                    submission_start = ora_elem.get('submission_start', '')
                    submission_due = ora_elem.get('submission_due', '')
                    
                    if submission_start:
                        sub_start = parse_iso_date(submission_start)
                        if sub_start:
                            ora_info['dates']['Response Start'] = submission_start
                            if sub_start < course_start or sub_start > course_end:
                                ora_info['flags'].append(('Response Start', '❌'))
                    
                    if submission_due:
                        sub_due = parse_iso_date(submission_due)
                        if sub_due:
                            ora_info['dates']['Response End'] = submission_due
                            if sub_due < course_start or sub_due > course_end:
                                ora_info['flags'].append(('Response End', '❌'))
                    
                    # Look for peer assessment dates
                    for assessment in ora_elem.findall('.//assessment[@name="peer-assessment"]'):
                        assess_start = assessment.get('start', '')
                        assess_due = assessment.get('due', '')
                        must_grade = int(assessment.get('must_grade', 0))
                        must_be_graded_by = int(assessment.get('must_be_graded_by', 0))
                        
                        ora_info['grading_config'] = {
                            'must_grade': must_grade,
                            'must_be_graded_by': must_be_graded_by
                        }
                        
                        if assess_start:
                            assess_start_dt = parse_iso_date(assess_start)
                            if assess_start_dt:
                                ora_info['dates']['Peer Start'] = assess_start
                                if assess_start_dt < course_start or assess_start_dt > course_end:
                                    ora_info['flags'].append(('Peer Start', '❌'))
                        
                        if assess_due:
                            assess_due_dt = parse_iso_date(assess_due)
                            if assess_due_dt:
                                ora_info['dates']['Peer End'] = assess_due
                                if assess_due_dt < course_start or assess_due_dt > course_end:
                                    ora_info['flags'].append(('Peer End', '❌'))
                        
                        # Check if must_grade > must_be_graded_by
                        if must_grade > 0 and must_be_graded_by > 0:
                            if must_grade <= must_be_graded_by:
                                ora_info['flags'].append(('Grading Config', '⚠️'))
                        
                        # Check for date overlap (response end should be before peer start)
                        if submission_due and assess_start:
                            resp_end_dt = parse_iso_date(submission_due)
                            assess_start_dt = parse_iso_date(assess_start)
                            if resp_end_dt and assess_start_dt:
                                if resp_end_dt >= assess_start_dt:
                                    ora_info['flags'].append(('Date Overlap', '⚠️'))
                    
                    # Only include if there are flags or dates exist
                    if ora_info['flags'] or ora_info['dates']:
                        oras.append(ora_info)
                        print(f"DEBUG: Found ORA: {ora_info['display_name']} with {len(ora_info['flags'])} flags")
            
            except Exception as e:
                print(f"DEBUG: Error parsing {vertical_file}: {str(e)}")
    
    print(f"DEBUG: Found {len(oras)} ORAs total")
    return oras