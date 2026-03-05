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
    Handles multiple formats.
    """
    try:
        # Try common formats
        for fmt in ['%B %d, %Y', '%B %d %Y', '%d %B %Y', '%m/%d/%Y', '%d/%m/%Y']:
            try:
                return datetime.strptime(date_text, fmt)
            except ValueError:
                continue
        return None
    except:
        return None


def find_date_mentions(course_dir, course_info):
    """
    Find all date mentions in HTML files that are outside course date range.
    Returns a list of dicts with date mention info.
    """
    mentions = []
    html_dir = os.path.join(course_dir, 'course', 'html')
    
    if not os.path.exists(html_dir):
        print("DEBUG: No html directory found for date mentions")
        return mentions
    
    # Parse course dates
    course_start = parse_iso_date(course_info.get('start_date', ''))
    course_end = parse_iso_date(course_info.get('end_date', ''))
    
    if not course_start or not course_end:
        print("DEBUG: Could not parse course dates for date mentions check")
        return mentions
    
    print(f"DEBUG: Searching for date mentions in {html_dir}")
    print(f"DEBUG: Course date range: {course_start} to {course_end}")
    
    # Loop through all HTML files
    for filename in os.listdir(html_dir):
        if not (filename.endswith('.xml') or filename.endswith('.html')):
            continue
        
        filepath = os.path.join(html_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse HTML content
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
            
            # Find all dates in text
            dates_found = find_date_in_text(text)
            
            for date_text, idx in dates_found:
                # Parse the date
                parsed_date = parse_found_date(date_text)
                
                if not parsed_date:
                    continue
                
                # Check if outside course range
                is_outside = parsed_date < course_start or parsed_date > course_end
                
                if not is_outside:
                    continue  # Only flag dates outside range
                
                # Extract context (3 words before and after)
                words = text.split()
                current_pos = 0
                word_index = 0
                
                for i, word in enumerate(words):
                    current_pos = text.find(word, current_pos)
                    if current_pos >= idx:
                        word_index = i
                        break
                    current_pos += len(word)
                
                # Get 3 words before and after
                start_word = max(0, word_index - 3)
                end_word = min(len(words), word_index + len(date_text.split()) + 3)
                
                context_words = words[start_word:end_word]
                context = ' '.join(context_words)
                
                # Find the vertical for this HTML file
                vertical_info = find_vertical_for_html(course_dir, filename)
                studio_link = build_studio_link(course_info, vertical_info) if vertical_info else None
                
                mentions.append({
                    'date': date_text,
                    'context': context,
                    'html_file': filename,
                    'vertical_info': vertical_info,
                    'studio_link': studio_link
                })
                
                print(f"DEBUG: Found date mention in {filename}: {date_text}")
        
        except Exception as e:
            print(f"DEBUG: Error searching {filename} for dates: {str(e)}")
    
    print(f"DEBUG: Found {len(mentions)} date mentions total")
    return mentions