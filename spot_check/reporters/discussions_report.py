def generate_discussions_html(discussions_info, course_info):
    """
    Generate HTML for discussions section.
    Shows status (open/closed) and any issues with instructions.
    """
    discussions_html = ""
    
    # Determine icon based on status
    if discussions_info['status'] == 'open':
        icon = "✅"
        status_text = "Open"
        status_color = "green"
    else:
        icon = "⚠️"
        status_text = "Closed"
        status_color = "orange"
    
    discussions_html += f"<h3>{icon} Discussions: {status_text}</h3>"
    discussions_html += "<p></p>"
    
    # If there are issues, show them with instructions
    if discussions_info['flags']:
        discussions_html += "<p style='color: #c41e3a; font-weight: bold;'>"
        for flag_name, flag_icon in discussions_info['flags']:
            discussions_html += f"{flag_icon} {flag_name}<br/>"
        discussions_html += "</p>"
        
        # Build discussion settings link
        course_key = f"course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
        settings_link = f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/pages-and-resources/discussion/configure/openedx"
        
        discussions_html += f"<p><a href='{settings_link}' target='_blank'>Link to Discussion Settings</a></p>"
        
        # Show appropriate instructions based on issue
        discussions_html += "<details style='margin-bottom: 20px;'>"
        discussions_html += "<summary style='cursor: pointer; font-weight: bold;'>How to Fix Discussion Issues</summary>"
        discussions_html += "<div style='margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-left: 3px solid #a31f34;'>"
        
        # Check which issue to show instructions for
        has_blackout_overlap = any('Blackout' in flag[0] for flag in discussions_info['flags'])
        has_closed = any('Closed' in flag[0] for flag in discussions_info['flags'])
        
        if has_blackout_overlap:
            discussions_html += "<h4>To Clear Blackout Dates and Open Discussions:</h4>"
            discussions_html += "<ul>"
            discussions_html += "<li>Go to your discussion settings (link above)</li>"
            discussions_html += "<li>If that link does not work, you can access your discussion settings by going to Content → Pages & Resources, then click on the gear icon on the Discussion card. Click next to get to the Setting.</li>"
            discussions_html += "<li>Scroll to the bottom of the settings and find \"Discussion restrictions\"</li>"
            discussions_html += "<li>Select \"Scheduled\" and delete any date ranges that are there</li>"
            discussions_html += "<li>Confirm your choice by clicking \"Delete\"</li>"
            discussions_html += "<li>Select \"Off\"</li>"
            discussions_html += "<li>Save your changes</li>"
            discussions_html += "</ul>"
        elif has_closed:
            discussions_html += "<h4>To Open Your Discussions:</h4>"
            discussions_html += "<ul>"
            discussions_html += "<li>Go to your discussion settings (link above)</li>"
            discussions_html += "<li>If that link does not work, you can access your discussion settings by going to Content → Pages & Resources, then click on the gear icon on the Discussion card. Click next to get to the Setting.</li>"
            discussions_html += "<li>Scroll to the bottom of the settings and find \"Discussion restrictions\"</li>"
            discussions_html += "<li>Select \"Off\" and save</li>"
            discussions_html += "</ul>"
        
        discussions_html += "</div></details>"
    else:
        discussions_html += "<p>No discussion issues detected.</p>"
    
    return discussions_html