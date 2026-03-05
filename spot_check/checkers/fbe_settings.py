import os
import xml.etree.ElementTree as ET
import json
from .utils import build_studio_link


def find_fbe_gating(course_dir, course_info):
    """
    Find all units with group access (FBE) restrictions.
    Returns a list of dicts with gating info.
    """
    gated_units = []
    has_verified_restriction = False
    
    # Search in both draft and non-draft verticals
    for vertical_dir in [
        os.path.join(course_dir, 'course', 'vertical'),
        os.path.join(course_dir, 'course', 'drafts', 'vertical')
    ]:
        if not os.path.exists(vertical_dir):
            continue
        
        print(f"DEBUG: Searching for FBE gating in {vertical_dir}")
        
        for vertical_file in os.listdir(vertical_dir):
            if not vertical_file.endswith('.xml'):
                continue
            
            vertical_path = os.path.join(vertical_dir, vertical_file)
            try:
                tree = ET.parse(vertical_path)
                root = tree.getroot()
                
                # Check for group_access attribute
                group_access_str = root.get('group_access', '')
                
                if not group_access_str:
                    continue
                
                # Parse the group_access JSON
                try:
                    # Replace HTML entities
                    group_access_str = group_access_str.replace('&quot;', '"')
                    group_access = json.loads(group_access_str)
                except:
                    print(f"DEBUG: Could not parse group_access in {vertical_file}")
                    continue
                
                # Extract restriction type
                unit_name = root.get('display_name', 'Unknown')
                vertical_id = vertical_file.replace('.xml', '')
                is_draft = 'drafts' in vertical_dir
                
                # group_access format: {"50": [1]} or {"50": [2]}
                # 1 = Auditors only, 2 = Verified learners only
                for group_id, restriction_list in group_access.items():
                    if isinstance(restriction_list, list) and len(restriction_list) > 0:
                        restriction_type = restriction_list[0]
                        
                        if restriction_type == 2:
                            restriction_name = "Verified Learners Only"
                            has_verified_restriction = True
                        elif restriction_type == 1:
                            restriction_name = "Auditors Only"
                        else:
                            restriction_name = f"Unknown Restriction ({restriction_type})"
                        
                        # Build studio link
                        vertical_info = {
                            'name': unit_name,
                            'id': vertical_id,
                            'is_draft': is_draft
                        }
                        studio_link = build_studio_link(course_info, vertical_info)
                        
                        gated_units.append({
                            'name': unit_name,
                            'id': vertical_id,
                            'restriction_type': restriction_name,
                            'studio_link': studio_link
                        })
                        
                        print(f"DEBUG: Found gated unit: {unit_name} - {restriction_name}")
            
            except Exception as e:
                print(f"DEBUG: Error reading {vertical_file}: {str(e)}")
    
    print(f"DEBUG: Found {len(gated_units)} gated units total")
    
    return {
        'gated_units': gated_units,
        'has_verified_restriction': has_verified_restriction
    }