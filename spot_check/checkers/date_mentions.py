import os
import re
from bs4 import BeautifulSoup
from datetime import datetime
from .utils import find_vertical_for_html, build_studio_link


def parse_iso_date(date_string):
    """Parse ISO date string to datetime object"""
    try:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except:
        return None


def find_date_in_text(text):
    """
    Find all dates in various formats:
    - Month DD, YYYY (January 01, 2026)
    - DD/MM/YYYY (01/01/2026)
    - MM/DD/YYYY (01/01/2026)
    - DD Month YYYY (01 January 2026)
    
    Returns list of (matched_text, start_index) tuples
    """
    dates_found = []
    
    # Pattern 1: Month DD, YYYY (e.g., January 01, 2026)
    month_pattern = r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})\b'
    for match in re.finditer(month_pattern, text, re.IGNORECASE):
        dates_found.append((match.group(0), match.start()))
    
    # Pattern 2: DD/MM/YYYY or MM/DD/YYYY (e.g., 01/01/2026)
    slash_pattern = r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b'
    for match in re.finditer(slash_pattern, text):
        dates_found.append((match.group(0), match.start()))
    
    # Pattern 3: DD Month YYYY (e.g., 01 January 2026)
    day_month_pattern = r'\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b'
    for match in re.finditer(day_month_pattern, text, re.IGNORECASE):
        dates_found.append((match.group(0), match.start()))
    
    return dates_found


def parse_found_date(date_text):
    """
    Try to parse a found date text into a datetime object.
    Handles multiple formats, including case-insensitive month names.
    Returns timezone-aware datetime (UTC) to match course dates.
    """
    from datetime import timezone
    
    try:
        normalized = date_text.strip()
        
        formats = [
            '%B %d, %Y',   # January 01, 2024
            '%B %d %Y',    # January 01 2024
            '%d %B %Y',    # 01 January 2024
            '%m/%d/%Y',    # 01/15/2024
            '%d/%m/%Y',    # 15/01/2024
        ]
        
        for fmt in formats:
            try:
                if '%B' in fmt:
                    try:
                        dt = datetime.strptime(normalized, fmt)
                    except ValueError:
                        dt = datetime.strptime(normalized.title(), fmt)
                else:
                    dt = datetime.strptime(normalized, fmt)
                
                # Make timezone-aware (UTC)
                return dt.replace(tzinfo=timezone.utc)
            except ValueError:
                continue
        
        return None
    except Exception as e:
        print(f"DEBUG: Error parsing date '{date_text}': {str(e)}")
        return None
    
def find_date_mentions(course_dir, course_info):
    """
    Find all date mentions in HTML files that are outside course date range.
    Returns a list of dicts with date mention info.
    """
    mentions = []
    html_dir = os.path.join(course_dir, 'course', 'html')
    
    if not os.path.exists(html_dir):
        print(f"DEBUG: No html directory found at {html_dir}")
        return mentions
    
    # Parse course dates
    course_start = parse_iso_date(course_info.get('start_date', ''))
    course_end = parse_iso_date(course_info.get('end_date', ''))
    
    if not course_start or not course_end:
        print(f"DEBUG: Could not parse course dates")
        print(f"DEBUG: start_date = {course_info.get('start_date', '')}")
        print(f"DEBUG: end_date = {course_info.get('end_date', '')}")
        return mentions
    
    print(f"DEBUG: Course date range: {course_start} to {course_end}")
    print(f"DEBUG: Searching in {html_dir}")
    
    # List all files in html directory
    if os.path.exists(html_dir):
        files = os.listdir(html_dir)
        print(f"DEBUG: Files in html directory: {files}")
    
    # Loop through all HTML files
    for filename in os.listdir(html_dir):
        filepath = os.path.join(html_dir, filename)
        
        print(f"\nDEBUG: Processing {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"DEBUG: File size: {len(content)} bytes")
            
            # Parse HTML content
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
            
            print(f"DEBUG: Extracted text length: {len(text)} bytes")
            print(f"DEBUG: First 200 chars: {text[:200]}")
            
            # Find all dates in text
            dates_found = find_date_in_text(text)
            
            print(f"DEBUG: Found {len(dates_found)} potential dates in {filename}")
            for date_text, idx in dates_found:
                print(f"DEBUG:   - Date found: '{date_text}' at index {idx}")
            
            for date_text, idx in dates_found:
                # Parse the date
                parsed_date = parse_found_date(date_text)
                
                print(f"DEBUG: Attempting to parse '{date_text}'")
                if parsed_date:
                    print(f"DEBUG:   Parsed as: {parsed_date}")
                    is_outside = parsed_date < course_start or parsed_date > course_end
                    print(f"DEBUG:   Outside range? {is_outside}")
                else:
                    print(f"DEBUG:   Failed to parse!")
                    continue
                
                if not is_outside:
                    print(f"DEBUG:   Skipping - date is within range")
                    continue
                
                # Extract context
                words = text.split()
                current_pos = 0
                word_index = 0
                
                for i, word in enumerate(words):
                    current_pos = text.find(word, current_pos)
                    if current_pos >= idx:
                        word_index = i
                        break
                    current_pos += len(word)
                
                start_word = max(0, word_index - 3)
                end_word = min(len(words), word_index + len(date_text.split()) + 3)
                
                context_words = words[start_word:end_word]
                context = ' '.join(context_words)
                
                # Find the vertical for this HTML file
                vertical_info = find_vertical_for_html(course_dir, filename)
                studio_link = build_studio_link(course_info, vertical_info) if vertical_info else None
                
                mention = {
                    'date': date_text,
                    'context': context,
                    'html_file': filename,
                    'vertical_info': vertical_info,
                    'studio_link': studio_link
                }
                mentions.append(mention)
                
                print(f"DEBUG: ✓ Added to mentions: {date_text}")
        
        except Exception as e:
            print(f"DEBUG: Error processing {filename}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\nDEBUG: Total mentions found: {len(mentions)}")
    return mentions