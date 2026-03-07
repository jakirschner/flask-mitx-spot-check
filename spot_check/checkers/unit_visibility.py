import os
import xml.etree.ElementTree as ET
from .utils import find_vertical_for_html, build_studio_link


def find_unit_visibility_issues(course_dir, course_info):
    """
    Find units that are either staff-only or in draft status.
    Staff-only takes precedence - if a unit is both staff-only and draft,
    it will only be listed as staff-only.
    Returns a list of dicts with unit info and status.
    """
    units_with_issues = {}  # Use dict to track by unit ID to avoid duplicates
    
    # First, find all staff-only content
    staff_only_units = set()
    
    for root_dir in [
        os.path.join(course_dir, 'course'),
        os.path.join(course_dir, 'course', 'drafts')
    ]:
        for item_type in ['chapter', 'sequential', 'vertical']:
            item_dir = os.path.join(root_dir, item_type)
            
            if not os.path.exists(item_dir):
                continue
            
            for filename in os.listdir(item_dir):
                if not filename.endswith('.xml'):
                    continue
                
                filepath = os.path.join(item_dir, filename)
                try:
                    tree = ET.parse(filepath)
                    root = tree.getroot()
                    
                    # Check if it's staff-only
                    if root.get('visible_to_staff_only') == 'true':
                        unit_id = filename.replace('.xml', '')
                        display_name = root.get('display_name', 'Unknown')
                        staff_only_units.add(unit_id)
                        
                        units_with_issues[unit_id] = {
                            'name': display_name,
                            'id': unit_id,
                            'status': 'Staff-Only',
                            'type': item_type.capitalize(),
                            'is_draft': 'drafts' in filepath,
                            'studio_link': build_studio_link(course_info, {'id': unit_id}) if item_type == 'vertical' else None
                        }
                
                except Exception as e:
                    print(f"DEBUG: Error reading {filename}: {str(e)}")
    
    # Then, find draft units (but skip if already marked as staff-only)
    draft_dir = os.path.join(course_dir, 'course', 'drafts', 'vertical')
    
    if os.path.exists(draft_dir):
        for filename in os.listdir(draft_dir):
            if not filename.endswith('.xml'):
                continue
            
            unit_id = filename.replace('.xml', '')
            
            # Skip if already marked as staff-only
            if unit_id in staff_only_units:
                continue
            
            filepath = os.path.join(draft_dir, filename)
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()
                
                display_name = root.get('display_name', 'Unknown')
                
                units_with_issues[unit_id] = {
                    'name': display_name,
                    'id': unit_id,
                    'status': 'Draft',
                    'type': 'Vertical',
                    'is_draft': True,
                    'parent_url': root.get('parent_url', ''),
                    'studio_link': build_studio_link(course_info, {'id': unit_id})
                }
            
            except Exception as e:
                print(f"DEBUG: Error reading {filename}: {str(e)}")
    
    print(f"DEBUG: Found {len(units_with_issues)} units with visibility issues")
    return list(units_with_issues.values())