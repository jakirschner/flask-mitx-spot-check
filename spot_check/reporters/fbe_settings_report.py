def generate_fbe_settings_html(fbe_settings, course_info):
    """
    Generate HTML for FBE settings (course gating) section.
    """
    fbe_settings_html = ""
    gated_units = fbe_settings.get('gated_units', [])
    has_verified = fbe_settings.get('has_verified_restriction', False)
    
    if gated_units:
        fbe_settings_html += "<h3>FBE Settings (Course Gating)</h3>"
        fbe_settings_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        fbe_settings_html += "<tr><th>Unit Name</th><th>Restriction Type</th><th>Studio Link</th></tr>"
        for unit in gated_units:
            unit_name = unit['name']
            restriction_type = unit['restriction_type']
            studio_link = unit['studio_link']
            
            # Create clickable link
            unit_link = f"<a href='{studio_link}' target='_blank'>{unit_name}</a>"
            
            fbe_settings_html += "<tr>"
            fbe_settings_html += f"<td>{unit_name}</td>"
            fbe_settings_html += f"<td>{restriction_type}</td>"
            fbe_settings_html += f"<td>{unit_link}</td>"
            fbe_settings_html += "</tr>"
        fbe_settings_html += "</table>"
    else:
        fbe_settings_html += "<h3>FBE Settings (Course Gating)</h3>"
        fbe_settings_html += "<p>⚠️ None of your content is restricted to verified learners. Please double check that you are following your Featured Based Enrollment (FBE) requirements. (Contact your PA for more information).</p>"
    
    # Add collapsible instructions
    course_outline_link = f"https://studio.courses.learn.mit.edu/authoring/course/course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
    fbe_settings_html += f"<p><a href='{course_outline_link}' target='_blank'>Link to Course Outline</a></p>"
    fbe_settings_html += "<details style='margin-top: 10px;'>"
    fbe_settings_html += "<summary style='cursor: pointer; font-weight: bold;'>How to Edit FBE Settings</summary>"
    fbe_settings_html += "<div style='margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-left: 3px solid #a31f34;'>"
    fbe_settings_html += "<ol>"
    fbe_settings_html += "<li>Go to your course outline</li>"
    fbe_settings_html += "<li>Find the section or subsection you want to restrict</li>"
    fbe_settings_html += "<li>Click on the three dot menu to the right of the section or subsection name</li>"
    fbe_settings_html += "<li>Choose 'Configure'</li>"
    fbe_settings_html += "<li>Look for 'Restrict Access By' or 'Group Access' settings</li>"
    fbe_settings_html += "<li>Select the appropriate restriction (Verified Learners or Auditors)</li>"
    fbe_settings_html += "<li>Save your changes</li>"
    fbe_settings_html += "</ol>"
    fbe_settings_html += "</div>"
    fbe_settings_html += "</details>"
    
    return fbe_settings_html