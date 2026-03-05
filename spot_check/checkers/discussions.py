import os
import json
from datetime import datetime


def parse_iso_date(date_string):
    """Parse ISO date string to datetime object"""
    try:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except:
        return None


def find_discussions_issues(course_dir, course_info):
    """
    Check discussion settings for issues.
    Checks for blackout dates and posting restrictions.
    Returns dict with discussion status and flags.
    """
    discussions_info = {
        'status': None,  # 'open' or 'closed'
        'flags': [],
        'blackout_dates': [],
        'posting_restrictions': None
    }
    
    print("DEBUG: Checking discussions settings")
    
    # Parse course dates
    course_start = parse_iso_date(course_info.get('start_date', ''))
    course_end = parse_iso_date(course_info.get('end_date', ''))
    
    if not course_start or not course_end:
        print("DEBUG: Could not parse course dates for discussions check")
        return discussions_info
    
    # Read policy.json
    policy_path = os.path.join(course_dir, 'course', 'policies', course_info.get('course_run', ''), 'policy.json')
    
    try:
        with open(policy_path, 'r') as f:
            policy = json.load(f)
        
        # Check discussion_blackouts
        blackout_dates = policy.get('discussion_blackouts', [])
        if blackout_dates:
            discussions_info['blackout_dates'] = blackout_dates
            
            # Check if any blackout overlaps with course run
            for blackout in blackout_dates:
                try:
                    blackout_start = parse_iso_date(blackout.get('start', ''))
                    blackout_end = parse_iso_date(blackout.get('end', ''))
                    
                    if blackout_start and blackout_end:
                        # Check for overlap with course dates
                        if (blackout_start < course_end and blackout_end > course_start):
                            discussions_info['flags'].append(('Blackout Dates Overlap', '⚠️'))
                            print(f"DEBUG: Found overlapping blackout dates")
                except:
                    pass
        
        # Check posting_restrictions
        posting_restrictions = policy.get('posting_restrictions', 'disabled')
        discussions_info['posting_restrictions'] = posting_restrictions
        
        if posting_restrictions == 'disabled':
            discussions_info['status'] = 'open'
            print("DEBUG: Discussions are OPEN")
        else:
            discussions_info['status'] = 'closed'
            discussions_info['flags'].append(('Discussions Closed', '⚠️'))
            print("DEBUG: Discussions are CLOSED")
    
    except Exception as e:
        print(f"DEBUG: Error reading discussions settings: {str(e)}")
    
    return discussions_info 