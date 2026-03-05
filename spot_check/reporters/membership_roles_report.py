def generate_membership_roles_html(course_info):
    """
    Generate HTML for membership roles section.
    Always shows link to instructor dashboard and instructions for adding roles.
    """
    membership_html = ""
    
    membership_html += "<h3>Verify Membership Roles</h3>"
    
    # Build membership link
    course_key = f"course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
    membership_link = f"https://courses.learn.mit.edu/courses/{course_key}/instructor#view-membership"
    
    membership_html += f"<p><a href='{membership_link}' target='_blank'>Link to Membership Tab</a></p>"
    
    # Collapsible instructions
    membership_html += "<details style='margin-bottom: 20px;'>"
    membership_html += "<summary style='cursor: pointer; font-weight: bold;'>How to Verify and Update Membership Roles</summary>"
    membership_html += "<div style='margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-left: 3px solid #a31f34;'>"
    
    membership_html += "<p>Please verify that you have correctly assigned roles in the course.</p>"
    
    membership_html += "<p>You can do this from the <a href='" + membership_link + "' target='_blank'>Membership tab of your Instructor Dashboard</a>.</p>"
    
    membership_html += "<p>If that link does not work, find your membership tab by viewing your live course, clicking on the \"Instructor\" tab, then on \"Membership\".</p>"
    
    membership_html += "<ol>"
    membership_html += "<li>Scroll to the bottom of the Membership tab and find the section labeled \"Course Team Management\"</li>"
    membership_html += "<li>In the drop down list under \"Select a course team role,\" choose \"Discussion Admins\"</li>"
    membership_html += "<li>Add the emails of whichever individuals will be responsible for monitoring the discussion forums during the run of the course</li>"
    membership_html += "<li>Click \"Add Discussion Admin\"</li>"
    membership_html += "<li>Once you have completed adding your Discussion Admins, select the role \"Course Data Researcher\"</li>"
    membership_html += "<li>Course data researchers are given access to a number of useful reports about your course. They will have access to a new link on the instructor dashboard \"Data Download\" where they will be able to view and generate reports.</li>"
    membership_html += "<li><strong>Note:</strong> These reports contain sensitive learner information and should not be shared beyond the course team or downloaded and transmitted via email or other insecure channel.</li>"
    membership_html += "<li>As above, add the emails of whichever individuals you want to give access to this course information</li>"
    membership_html += "</ol>"
    
    membership_html += "<p>Please note that those you wish to add to these course roles must first have accounts on <a href='https://learn.mit.edu/' target='_blank'>MIT Learn</a>.</p>"
    
    membership_html += "</div></details>"
    
    return membership_html