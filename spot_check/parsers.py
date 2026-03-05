import json
import xml.etree.ElementTree as ET
import os
import glob
from datetime import datetime

def parse_course_info(extract_dir):
    """Parse course information from the extracted tarball"""
    
    course_info = {
        'title': None,
        'course_number': None,
        'course_run': None,
        'start_date': None,
        'end_date': None,
        'self_paced': None,
        'errors': []
    }
    
    # Parse policies/policy.json
    policy_path = os.path.join(extract_dir, 'course', 'policies', 'policy.json')
    try:
        with open(policy_path, 'r') as f:
            policy = json.load(f)
            course_info['title'] = policy.get('display_name', 'Unknown')
            course_info['start_date'] = policy.get('start', 'Unknown')
            course_info['end_date'] = policy.get('end', 'Unknown')
    except Exception as e:
        course_info['errors'].append(f"Error reading policy.json: {str(e)}")
    
    # Parse course/[run].xml
    course_xml_pattern = os.path.join(extract_dir, 'course', '*.xml')
    course_xml_files = glob.glob(course_xml_pattern)
    
    if course_xml_files:
        try:
            tree = ET.parse(course_xml_files[0])
            root = tree.getroot()
            
            course_info['course_number'] = root.get('course', 'Unknown')
            course_info['course_run'] = root.get('url_name', 'Unknown')
            course_info['self_paced'] = root.get('self_paced', 'false') == 'true'
        except Exception as e:
            course_info['errors'].append(f"Error reading course XML: {str(e)}")
    
    # Validate all fields
    for field in ['title', 'course_number', 'course_run', 'start_date', 'end_date']:
        if not course_info[field] or course_info[field] == 'Unknown':
            course_info['errors'].append(f"Missing or invalid: {field}")
    
    return course_info