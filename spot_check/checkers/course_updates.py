import os
import json
from datetime import datetime
import re


def parse_iso_date(date_string):
    """Parse ISO date string to datetime object"""
    try:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except:
        return None


def extract_dates_from_text(text):
    """
    Extract dates from text using regex patterns.
    Supports: Month DD, YYYY | DD/MM/YYYY | MM/DD/YYYY | DD Month YYYY
    Returns list of date strings found.
    """
    dates = []
    
    # Month name patterns
    month_pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
    
    patterns = [
        rf'{month_pattern}\s+\d{{1,2}},?\s+\d{{4}}',  # January 01, 2026 or January 01 2026
        r'\d{{1,2}}/\d{{1,2}}/\d{{4}}',  # 01/01/2026 or 1/1/2026
        rf'\d{{1,2}}\s+{month_pattern}\s+\d{{4}}',  # 01 January 2026
    ]
    
    for pattern in patterns:
        found = re.findall(pattern, text, re.IGNORECASE)
        dates.extend(found)
    
    return dates


def find_course_updates_issues(course_dir, course_info):
    """
    Check course updates for issues.
    Flags updates from before course start date and dates in content outside course range.
    Returns list of dicts with update info and flags.
    """
    updates_issues = []
    
    print("DEBUG: Checking course updates")
    
    # Parse course dates
    course_start = parse_iso_date(course_info.get('start_date', ''))
    course_end = parse_iso_date(course_info.get('end_date', ''))
    
    if not course_start or not course_end:
        print("DEBUG: Could not parse course dates for updates check")
        return updates_issues
    
    # Read updates.items.json
    updates_path = os.path.join(course_dir, 'course', 'info', 'updates.items.json')
    
    try:
        with open(updates_path, 'r') as f:
            updates = json.load(f)
        
        for update in updates:
            if update.get('status') != 'visible':
                continue
            
            update_date_str = update.get('date', '')
            content = update.get('content', '')
            update_id = update.get('id', 'unknown')
            
            flags = []
            
            # Check if update date is before course start
            if update_date_str:
                try:
                    # Parse the date string (e.g., "October 25, 2022")
                    update_date = datetime.strptime(update_date_str, '%B %d, %Y').replace(tzinfo=course_start.tzinfo)
                    
                    if update_date < course_start:
                        flags.append(('Update Date Before Course Start', '⚠️'))
                        print(f"DEBUG: Found update from before course start: {update_date_str}")
                except:
                    pass
            
            # Check for dates in content outside course range
            if content:
                dates_in_content = extract_dates_from_text(content)
                for date_str in dates_in_content:
                    try:
                        # Try to parse the date
                        for fmt in ['%B %d, %Y', '%B %d %Y', '%d/%m/%Y', '%m/%d/%Y', '%d %B %Y']:
                            try:
                                content_date = datetime.strptime(date_str, fmt).replace(tzinfo=course_start.tzinfo)
                                
                                if content_date < course_start or content_date > course_end:
                                    flags.append(('Date in Content Outside Range', '⚠️'))
                                    print(f"DEBUG: Found date in update content outside range: {date_str}")
                                break
                            except ValueError:
                                continue
                    except:
                        pass
            
            # Only include if there are flags
            if flags:
                update_info = {
                    'id': update_id,
                    'date': update_date_str,
                    'content': content,
                    'flags': flags
                }
                updates_issues.append(update_info)
    
    except FileNotFoundError:
        print("DEBUG: updates.items.json not found")
    except Exception as e:
        print(f"DEBUG: Error reading course updates: {str(e)}")
    
    return updates_issues