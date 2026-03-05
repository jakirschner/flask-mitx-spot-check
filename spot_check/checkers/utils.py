import os
import xml.etree.ElementTree as ET

def find_vertical_for_html(course_dir, html_filename):
    """
    Find which vertical contains this HTML file.
    Returns the vertical block ID and display name, or None if not found.
    """
    # Remove extension
    html_url_name = html_filename.replace('.xml', '').replace('.html', '')
    
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
                
                # Look for html elements with matching url_name
                for html_elem in root.findall('.//html'):
                    if html_elem.get('url_name') == html_url_name:
                        # Found it! Return vertical info
                        vertical_name = root.get('display_name', 'Unknown')
                        vertical_id = vertical_file.replace('.xml', '')
                        return {
                            'name': vertical_name,
                            'id': vertical_id,
                            'is_draft': 'drafts' in vertical_dir
                        }
            except:
                continue
    
    return None


def build_studio_link(course_info, vertical_info):
    """
    Build a Studio link to a vertical.
    """
    if not vertical_info:
        return None
    
    course_key = f"course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
    vertical_block_id = f"block-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}+type@vertical+block@{vertical_info['id']}"
    
    if vertical_info['is_draft']:
        sequential_block_id = f"block-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}+type@sequential+block@{vertical_info['id']}"
        link = f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/container/{vertical_block_id}/{sequential_block_id}"
    else:
        link = f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/container/{vertical_block_id}"
    
    return link


def get_link_context(html_content, link_text, url, words_before=3, words_after=3):
    """
    Extract context around a link in HTML content.
    Returns text with 3 words before and after the link text.
    """
    from bs4 import BeautifulSoup
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        
        # Find the link text in the content
        idx = text.find(link_text)
        if idx == -1:
            idx = text.find(url)
        
        if idx == -1:
            return "Context not found"
        
        # Split into words and find position
        words = text.split()
        current_pos = 0
        word_index = 0
        
        for i, word in enumerate(words):
            current_pos = text.find(word, current_pos)
            if current_pos >= idx:
                word_index = i
                break
            current_pos += len(word)
        
        # Get words before and after
        start_word = max(0, word_index - words_before)
        end_word = min(len(words), word_index + len(link_text.split()) + words_after)
        
        context_words = words[start_word:end_word]
        context = ' '.join(context_words)
        
        return context
    except:
        return "Context extraction failed"