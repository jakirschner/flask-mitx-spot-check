from datetime import datetime
from spot_check.checkers import check_broken_links, find_edx_mentions, find_draft_units, find_fbe_gating

def generate_html_report(course_info, course_dir):
    """Generate the HTML report"""
    
    # Format dates
    start_date = format_date(course_info.get('start_date', 'Unknown'))
    end_date = format_date(course_info.get('end_date', 'Unknown'))
    
    # Run checks
    broken_links = check_broken_links(course_dir, course_info)
    edx_mentions = find_edx_mentions(course_dir, course_info)
    draft_units = find_draft_units(course_dir, course_info)
    fbe_settings = find_fbe_gating(course_dir, course_info)

    # Build broken links HTML
    broken_links_html = ""
    if broken_links:
        broken_links_html += "<h3>⚠️ Broken Links</h3>"
        broken_links_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        broken_links_html += "<tr><th>Unit</th><th>Link Text & Context</th><th>Status</th></tr>"
        for link in broken_links:
            context = link.get('context', 'N/A')
            status = link['status']['reason']
            vertical_name = link['vertical_info']['name'] if link['vertical_info'] else 'Unknown'
            studio_link = link['studio_link']
            
            # Create clickable link if we have a studio link
            if studio_link:
                unit_link = f"<a href='{studio_link}' target='_blank'>{vertical_name}</a>"
            else:
                unit_link = vertical_name
            
            broken_links_html += "<tr>"
            broken_links_html += f"<td>{unit_link}</td>"
            broken_links_html += f"<td><strong>{link['link_text']}</strong><br/><em style='color: #666;'>{context}</em></td>"
            broken_links_html += f"<td>{status}</td>"
            broken_links_html += "</tr>"
        broken_links_html += "</table>"
    else:
        broken_links_html += "<p>✅ No broken links found</p>"
    
    # Build edX mentions HTML
    edx_mentions_html = ""
    if edx_mentions:
        edx_mentions_html += "<h3>⚠️ edX Mentions</h3>"
        edx_mentions_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        edx_mentions_html += "<tr><th>Unit</th><th>Context</th></tr>"
        for mention in edx_mentions:
            vertical_name = mention['vertical_info']['name'] if mention['vertical_info'] else 'Unknown'
            studio_link = mention['studio_link']
            
            # Create clickable link if we have a studio link
            if studio_link:
                unit_link = f"<a href='{studio_link}' target='_blank'>{vertical_name}</a>"
            else:
                unit_link = vertical_name
            
            edx_mentions_html += "<tr>"
            edx_mentions_html += f"<td>{unit_link}</td>"
            edx_mentions_html += f"<td><em style='color: #666;'>{mention['context']}</em></td>"
            edx_mentions_html += "</tr>"
        edx_mentions_html += "</table>"
    else:
        edx_mentions_html += "<p>✅ No edX mentions found</p>"
    
    # Build draft units HTML
    draft_units_html = ""
    if draft_units:
        draft_units_html += "<h3>⚠️ Units in Draft</h3>"
        draft_units_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        draft_units_html += "<tr><th>Unit Name</th></tr>"
        for draft in draft_units:
            unit_name = draft['name']
            studio_link = draft['studio_link']
            
            # Create clickable link
            unit_link = f"<a href='{studio_link}' target='_blank'>{unit_name}</a>"
            
            draft_units_html += "<tr>"
            draft_units_html += f"<td>{unit_link}</td>"
            draft_units_html += "</tr>"
        draft_units_html += "</table>"
    else:
        draft_units_html += "<p>✅ No draft units found</p>"

# Build FBE settings HTML
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
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Spot Check Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .header {{
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            .title {{
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .course-info {{
                font-size: 14px;
                color: #666;
            }}
            .content {{
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">{course_info.get('title', 'Unknown Course')}</div>
            <div class="course-info">
                {course_info.get('course_number', 'Unknown')} | 
                {course_info.get('course_run', 'Unknown')} | 
                {start_date} - {end_date}
            </div>
        </div>
        
        <div class="content">
            <h2>Course Content</h2>
            {broken_links_html}
            {edx_mentions_html}
            {draft_units_html}
            {fbe_settings_html}
        </div>
    </body>
    </html>
    """
    
    return html

def format_date(date_string):
    """Format ISO date to readable format"""
    try:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.strftime('%B %d, %Y')
    except:
        return date_string