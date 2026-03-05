import os
import xml.etree.ElementTree as ET


def find_draft_units(course_dir, course_info):
    """
    Find all units that are in draft status.
    Returns a list of dicts with draft unit info.
    """
    drafts = []
    drafts_vertical_dir = os.path.join(course_dir, 'course', 'drafts', 'vertical')
    
    if not os.path.exists(drafts_vertical_dir):
        print("DEBUG: No drafts/vertical directory found")
        return drafts
    
    print(f"DEBUG: Searching for draft units in {drafts_vertical_dir}")
    
    # Loop through all vertical files in drafts
    for vertical_file in os.listdir(drafts_vertical_dir):
        if not vertical_file.endswith('.xml'):
            continue
        
        vertical_path = os.path.join(drafts_vertical_dir, vertical_file)
        try:
            tree = ET.parse(vertical_path)
            root = tree.getroot()
            
            unit_name = root.get('display_name', 'Unknown')
            vertical_id = vertical_file.replace('.xml', '')
            
            # Build studio link for draft unit
            course_key = f"course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
            vertical_block_id = f"block-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}+type@vertical+block@{vertical_id}"
            
            # For draft units, we need the parent sequential ID from the parent_url attribute
            parent_url = root.get('parent_url', '')
            if parent_url:
                # Extract the block ID from parent_url
                parent_block_id = parent_url.split('@')[-1] if '@' in parent_url else parent_url
                sequential_block_id = f"block-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}+type@sequential+block@{parent_block_id}"
                studio_link = f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/container/{vertical_block_id}/{sequential_block_id}"
            else:
                studio_link = f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/container/{vertical_block_id}"
            
            drafts.append({
                'name': unit_name,
                'id': vertical_id,
                'studio_link': studio_link
            })
            
            print(f"DEBUG: Found draft unit: {unit_name}")
        
        except Exception as e:
            print(f"DEBUG: Error reading {vertical_file}: {str(e)}")
    
    print(f"DEBUG: Found {len(drafts)} draft units total")
    return drafts