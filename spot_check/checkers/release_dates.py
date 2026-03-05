import os
import xml.etree.ElementTree as ET
from datetime import datetime


def parse_iso_date(date_string):
    """Parse ISO date string to datetime object"""
    try:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except:
        return None


def check_release_dates(course_dir, course_info):
    """
    Check release dates in chapters and sequentials.
    Returns a dict with flagged dates and whether course is self-paced.
    """
    result = {
        'is_self_paced': course_info.get('self_paced', False),
        'flagged_dates': [],
        'course_start': None,
        'course_end': None
    }
    
    # If self-paced, skip this check
    if result['is_self_paced']:
        print("DEBUG: Course is self-paced, skipping release dates check")
        return result
    
    # Parse course start and end dates
    course_start = parse_iso_date(course_info.get('start_date', ''))
    course_end = parse_iso_date(course_info.get('end_date', ''))
    
    result['course_start'] = course_start
    result['course_end'] = course_end
    
    if not course_start or not course_end:
        print("DEBUG: Could not parse course dates")
        return result
    
    print(f"DEBUG: Checking release dates between {course_start} and {course_end}")
    
    # Search chapters and sequentials
    search_dirs = [
        ('chapter', os.path.join(course_dir, 'course', 'chapter')),
        ('sequential', os.path.join(course_dir, 'course', 'sequential')),
        ('chapter_draft', os.path.join(course_dir, 'course', 'drafts', 'chapter')),
        ('sequential_draft', os.path.join(course_dir, 'course', 'drafts', 'sequential')),
    ]
    
    for item_type, search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
        
        print(f"DEBUG: Searching for release dates in {search_dir}")
        
        for filename in os.listdir(search_dir):
            if not filename.endswith('.xml'):
                continue
            
            filepath = os.path.join(search_dir, filename)
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()
                
                # Check for start attribute (release date)
                start_date_str = root.get('start', '')
                if not start_date_str:
                    continue
                
                start_date = parse_iso_date(start_date_str)
                if not start_date:
                    continue
                
                # Check if outside course range
                is_outside = start_date < course_start or start_date > course_end
                
                if is_outside:
                    item_name = root.get('display_name', 'Unknown')
                    
                    # Determine reason
                    if start_date < course_start:
                        reason = "Release date is before course start date"
                    else:
                        reason = "Release date is after course end date"
                    
                    result['flagged_dates'].append({
                        'name': item_name,
                        'type': item_type.replace('_draft', ''),
                        'release_date': start_date_str,
                        'reason': reason
                    })
                    
                    print(f"DEBUG: Found flagged release date in {item_name}: {reason}")
            
            except Exception as e:
                print(f"DEBUG: Error reading {filename}: {str(e)}")
    
    print(f"DEBUG: Found {len(result['flagged_dates'])} flagged release dates")
    return result