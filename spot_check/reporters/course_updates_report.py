def generate_course_updates_html(updates_issues, course_info):
    """
    Generate HTML for course updates section.
    Shows flagged updates from previous runs or with dates outside course range.
    """
    updates_html = ""
    
    if updates_issues:
        updates_html += "<h3>⚠️ Course Updates</h3>"
        
        # Build course updates link
        course_key = f"course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
        updates_link = f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/course_info"
        
        updates_html += f"<p><a href='{updates_link}' target='_blank'>Link to Course Updates</a></p>"
        
        # Show message about updates from previous run
        updates_html += "<p style='color: #c41e3a; font-weight: bold;'>"
        updates_html += "Course updates appear to be from a previous run."
        updates_html += "</p>"
        
        # Show which updates have issues
        updates_html += "<ul>"
        for update in updates_issues:
            updates_html += f"<li><strong>Update ID {update['id']}</strong> (Date: {update['date']})"
            for flag_name, flag_icon in update['flags']:
                updates_html += f"<br/>{flag_icon} {flag_name}"
            updates_html += "</li>"
        updates_html += "</ul>"
    else:
        updates_html += "<h3>Course Updates</h3>"
        
        # Build course updates link
        course_key = f"course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
        updates_link = f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/course_info"
        
        updates_html += f"<p><a href='{updates_link}' target='_blank'>Link to Course Updates</a></p>"
        updates_html += "<p>✅ All course updates appear to be from the current run.</p>"
    
    return updates_html