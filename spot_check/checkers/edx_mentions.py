import os
import re
from bs4 import BeautifulSoup
from .utils import find_vertical_for_html, build_studio_link


def find_edx_mentions(course_dir, course_info):
    """
    Find all mentions of 'edX' (case-insensitive) in HTML files.
    Returns a list of dicts with mention info and context.
    """
    mentions = []
    html_dir = os.path.join(course_dir, 'course', 'html')
    
    if not os.path.exists(html_dir):
        print("DEBUG: No html directory found for edX mentions")
        return mentions
    
    print(f"DEBUG: Searching for edX mentions in {html_dir}")
    
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
            
            # Search for edX (case-insensitive)
            for match in re.finditer(r'edx', text, re.IGNORECASE):
                idx = match.start()
                
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
                end_word = min(len(words), word_index + 4)  # +4 to include "edx"
                
                context_words = words[start_word:end_word]
                context = ' '.join(context_words)
                
                # Skip standard footer text
                if 'powered by open edx' in context.lower() or 'open edx logo' in context.lower():
                    print(f"DEBUG: Skipping standard Open edX logo/footer mention")
                    continue
                
                # Find the vertical for this HTML file
                vertical_info = find_vertical_for_html(course_dir, filename)
                studio_link = build_studio_link(course_info, vertical_info) if vertical_info else None
                
                mentions.append({
                    'context': context,
                    'html_file': filename,
                    'vertical_info': vertical_info,
                    'studio_link': studio_link
                })
                
                print(f"DEBUG: Found edX mention in {filename}: {context}")
        
        except Exception as e:
            print(f"DEBUG: Error searching {filename} for edX: {str(e)}")
    
    print(f"DEBUG: Found {len(mentions)} edX mentions total")
    return mentions