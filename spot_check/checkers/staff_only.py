import os
import xml.etree.ElementTree as ET
from .utils import build_studio_link


def find_staff_only_content(course_dir, course_info):
    """
    Find all content (chapters, sequentials, verticals) marked as visible_to_staff_only.
    Returns a list of dicts with staff-only content info.
    """
    staff_only_items = []
    
    # Search chapters, sequentials, and verticals in both draft and non-draft
    search_dirs = [
        ('chapter', os.path.join(course_dir, 'course', 'chapter')),
        ('sequential', os.path.join(course_dir, 'course', 'sequential')),
        ('vertical', os.path.join(course_dir, 'course', 'vertical')),
        ('chapter_draft', os.path.join(course_dir, 'course', 'drafts', 'chapter')),
        ('sequential_draft', os.path.join(course_dir, 'course', 'drafts', 'sequential')),
        ('vertical_draft', os.path.join(course_dir, 'course', 'drafts', 'vertical')),
    ]
    
    for item_type, search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
        
        print(f"DEBUG: Searching for staff-only content in {search_dir}")
        
        for filename in os.listdir(search_dir):
            if not filename.endswith('.xml'):
                continue
            
            filepath = os.path.join(search_dir, filename)
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()
                
                # Check for visible_to_staff_only attribute
                visible_to_staff_only = root.get('visible_to_staff_only', 'false').lower() == 'true'
                
                if not visible_to_staff_only:
                    continue
                
                item_name = root.get('display_name', 'Unknown')
                item_id = filename.replace('.xml', '')
                is_draft = 'drafts' in search_dir
                
                # Get the base item type (chapter, sequential, or vertical)
                base_type = item_type.replace('_draft', '')
                
                # Build studio link based on type
                if base_type in ['chapter', 'sequential']:
                    # Link to course outline
                    studio_link = f"https://studio.courses.learn.mit.edu/authoring/course/course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
                    link_text = "View in Course Outline"
                else:  # vertical
                    # Link to the vertical
                    vertical_info = {
                        'name': item_name,
                        'id': item_id,
                        'is_draft': is_draft
                    }
                    studio_link = build_studio_link(course_info, vertical_info)
                    link_text = "View in Studio"
                
                staff_only_items.append({
                    'name': item_name,
                    'id': item_id,
                    'type': base_type,
                    'studio_link': studio_link,
                    'link_text': link_text
                })
                
                print(f"DEBUG: Found staff-only {base_type}: {item_name}")
            
            except Exception as e:
                print(f"DEBUG: Error reading {filename}: {str(e)}")
    
    print(f"DEBUG: Found {len(staff_only_items)} staff-only items total")
    return staff_only_items