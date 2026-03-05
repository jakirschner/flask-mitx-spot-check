import json
import xml.etree.ElementTree as ET
import os
import glob
from datetime import datetime

def parse_course_info(extract_dir):
    """Parse course information from the extracted tarball"""
    
    # The course is in a 'course' subfolder within extract_dir
    course_dir = os.path.join(extract_dir, 'course')
    
    course_info = {
        'title': None,
        'course_number': None,
        'course_run': None,
        'org': None,
        'start_date': None,
        'end_date': None,
        'self_paced': None,
        'errors': []
    }
    
    # Step 1: Parse course/course.xml to get course_number, course_run, org
    course_metadata_path = os.path.join(course_dir, 'course.xml')
    
    if os.path.exists(course_metadata_path):
        try:
            tree = ET.parse(course_metadata_path)
            root = tree.getroot()
            
            course_info['course_number'] = root.get('course', 'Unknown')
            course_info['course_run'] = root.get('url_name', 'Unknown')
            course_info['org'] = root.get('org', 'Unknown')
            
        except Exception as e:
            course_info['errors'].append(f"Error reading course.xml: {str(e)}")
    else:
        course_info['errors'].append(f"course.xml not found at {course_metadata_path}")
    
    # Step 2: Parse course/[run].xml to get title, dates, self_paced
    course_xml_pattern = os.path.join(course_dir, 'course', '*.xml')
    course_xml_files = glob.glob(course_xml_pattern)
    
    if course_xml_files:
        try:
            tree = ET.parse(course_xml_files[0])
            root = tree.getroot()
            
            course_info['title'] = root.get('display_name', 'Unknown')
            course_info['start_date'] = root.get('start', 'Unknown')
            course_info['end_date'] = root.get('end', 'Unknown')
            course_info['self_paced'] = root.get('self_paced', 'false') == 'true'
            
        except Exception as e:
            course_info['errors'].append(f"Error reading course detail XML: {str(e)}")
    else:
        course_info['errors'].append("No course detail XML file found")
    
    # Validate all fields
    for field in ['title', 'course_number', 'course_run', 'org', 'start_date', 'end_date']:
        if not course_info[field] or course_info[field] == 'Unknown':
            course_info['errors'].append(f"Missing or invalid: {field}")
    
    return course_info