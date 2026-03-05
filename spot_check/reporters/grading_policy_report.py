def generate_grading_policy_html(course_info):
    """
    Generate HTML for grading policy section.
    Always shows link to grading policy and instructions for review.
    """
    grading_html = ""
    
    grading_html += "<h3>Grading Policy</h3>"
    
    # Build grading policy link
    course_key = f"course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
    grading_link = f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/settings/grading"
    
    grading_html += f"<p><a href='{grading_link}' target='_blank'>Link to Grading Policy</a></p>"
    
    grading_html += "<p>Please review your grading policies and look for any warnings. See the information below for an example of a warning.</p>"
    
    grading_html += "<p><strong>In particular, check to make sure that all your assignment weights add up to 100% for the course.</strong></p>"
    
    # Collapsible instructions
    grading_html += "<details style='margin-bottom: 20px;'>"
    grading_html += "<summary style='cursor: pointer; font-weight: bold;'>How to Check Grading Policy</summary>"
    grading_html += "<div style='margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-left: 3px solid #a31f34;'>"
    
    grading_html += "<ol>"
    grading_html += "<li>Go to your grading policy (link above)</li>"
    grading_html += "<li>Review each grading component and its weight</li>"
    grading_html += "<li>Verify that the total of all component weights equals 100%</li>"
    grading_html += "<li>Check for any warning messages displayed by the system</li>"
    grading_html += "<li>Ensure each assignment type (homework, exams, projects, etc.) has the correct weight</li>"
    grading_html += "</ol>"
    
    grading_html += "</div></details>"
    
    return grading_html