def generate_release_dates_html(release_dates_result, course_info):
    """
    Generate HTML for release dates section.
    Shows flagged release dates that are outside the course date range.
    """
    release_dates_html = ""
    
    # Check if self-paced
    if release_dates_result.get('is_self_paced'):
        print("DEBUG: Skipping release dates report for self-paced course")
        return ""
    
    release_dates_html += "<h3>❌ Release Dates</h3>"
    release_dates_html += "<p>This report checks release dates on sections and subsections. It will report if a date falls outside the time of your course run.</p>"
    release_dates_html += "<p>However, it is always good practice for you to go through each of your release dates and be sure that they are set correctly.</p>"
    
    # Link to course outline
    course_outline_link = f"https://studio.courses.learn.mit.edu/authoring/course/course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
    release_dates_html += f"<p><a href='{course_outline_link}' target='_blank'>Link to Course Outline</a></p>"
    
    # Collapsible instructions
    release_dates_html += "<details style='margin-bottom: 20px;'>"
    release_dates_html += "<summary style='cursor: pointer; font-weight: bold;'>How to Update Release Dates</summary>"
    release_dates_html += "<div style='margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-left: 3px solid #a31f34;'>"
    release_dates_html += "<ol>"
    release_dates_html += "<li>Navigate to your course outline</li>"
    release_dates_html += "<li>Find the name of the section or subsection you want to change the release date for</li>"
    release_dates_html += "<li>Click on the three dot menu to the right of the section or subsection name</li>"
    release_dates_html += "<li>Choose 'Configure'</li>"
    release_dates_html += "<li>Find the field labeled 'Release date' and update it</li>"
    release_dates_html += "</ol>"
    release_dates_html += "</div>"
    release_dates_html += "</details>"
    
    # Show flagged dates or message
    flagged_dates = release_dates_result.get('flagged_dates', [])
    
    if flagged_dates:
        release_dates_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        release_dates_html += "<thead><tr><th scope='col'>Section/Subsection Name</th><th scope='col'>Release Date</th><th scope='col'>Issue</th></tr></thead>"
        release_dates_html += "<tbody>"
        
        for date_item in flagged_dates:
            release_dates_html += "<tr>"
            release_dates_html += f"<td>{date_item['name']}</td>"
            release_dates_html += f"<td>{date_item['release_date']}</td>"
            release_dates_html += f"<td>{date_item['reason']}</td>"
            release_dates_html += "</tr>"
        
        release_dates_html += "</tbody></table>"
    else:
        release_dates_html += "<p>✅ Please check all your course release dates for accuracy.</p>"
    
    return release_dates_html