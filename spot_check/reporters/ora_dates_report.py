def build_ora_studio_link(course_info, ora_info):
    """Build a Studio link to an ORA unit (vertical)"""
    if not ora_info:
        return None
    
    course_key = f"course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
    vertical_block_id = f"block-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}+type@vertical+block@{ora_info['vertical_id']}"
    
    if ora_info['is_draft']:
        # Draft link (we'd need sequential info, for now just link to vertical)
        return f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/container/{vertical_block_id}"
    else:
        return f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/container/{vertical_block_id}"


def generate_ora_dates_html(oras, course_info):
    """
    Generate HTML for ORA step dates section.
    """
    ora_html = ""
    
    if oras:
        # Determine if any are critical (❌ flags)
        has_critical = any(any(flag[1] == '❌' for flag in ora['flags']) for ora in oras)
        icon = "❌" if has_critical else "⚠️"
        
        ora_html += f"<h3>{icon} ORA Step Dates</h3>"
        
        # Link to ORA section + toggle instructions
        ora_html += "<p><a href='https://studio.courses.learn.mit.edu/authoring/course/course-v1:" + course_info['org'] + "+" + course_info['course_number'] + "+" + course_info['course_run'] + "' target='_blank'>Link to ORA Units</a></p>"
        
        ora_html += "<details style='margin-bottom: 20px;'><summary style='cursor: pointer; font-weight: bold;'>How to Update ORA Dates</summary>"
        ora_html += "<div style='margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-left: 3px solid #a31f34;'>"
        ora_html += "<ul>"
        ora_html += "<li>Go to the unit containing your ORA</li>"
        ora_html += "<li>Find the ORA component</li>"
        ora_html += "<li>Click on the edit button (a pencil next to the ORA name)</li>"
        ora_html += "<li>Click on the \"Schedule\" tab and set the dates</li>"
        ora_html += "</ul>"
        ora_html += "<p><strong>A note about the settings \"Match deadlines to the subsection due date\" and \"Match deadlines to the course end date\":</strong></p>"
        ora_html += "<p>These can be useful settings, but bear in mind that they leave no room between when a learner may make a submission and when other learners must review them. If you have learners who submit a response close to the subsection due date or to the end of the course, there might not be an opportunity for the correct number of learners to review their submission. This may lead to situations where you will have to staff grade learners in order for them to receive credit for their ORA submissions.</p>"
        ora_html += "</div></details>"
        
        # Table for each ORA
        for ora in oras:
            studio_link = build_ora_studio_link(course_info, ora)
            
            # ORA header with link
            if studio_link:
                ora_link = f"<a href='{studio_link}' target='_blank'>{ora['display_name']}</a>"
            else:
                ora_link = ora['display_name']
            
            ora_html += f"<h4>{ora_link}</h4>"
            
            # Flags if any
            if ora['flags']:
                ora_html += "<p style='color: #c41e3a; font-weight: bold;'>"
                for flag_name, flag_icon in ora['flags']:
                    flag_reason = get_flag_reason(flag_name)
                    ora_html += f"{flag_icon} {flag_name}: {flag_reason}<br/>"
                ora_html += "</p>"
            
            # Dates table
            if ora['dates']:
                ora_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
                ora_html += "<tr><th>Step</th><th>Date</th></tr>"
                
                step_order = ['Response Start', 'Response End', 'Peer Start', 'Peer End']
                for step in step_order:
                    if step in ora['dates']:
                        date_value = ora['dates'][step]
                        flag_icon = ""
                        for flag_name, flag_sym in ora['flags']:
                            if flag_name == step:
                                flag_icon = f" {flag_sym}"
                                break
                        ora_html += f"<tr><td>{step}{flag_icon}</td><td>{date_value}</td></tr>"
                
                ora_html += "</table><br/>"
        
        # Grading config note if any issues
        for ora in oras:
            for flag_name, _ in ora['flags']:
                if flag_name == 'Grading Config':
                    must_grade = ora['grading_config'].get('must_grade', 0)
                    must_be_graded = ora['grading_config'].get('must_be_graded_by', 0)
                    ora_html += f"<p style='color: #c41e3a;'><strong>⚠️ Grading Config Issue:</strong> must_grade ({must_grade}) should be greater than must_be_graded_by ({must_be_graded})</p>"
                    break
    else:
        ora_html += "<h3>ORA Step Dates</h3>"
        ora_html += "<p>✅ No ORAs found in course</p>"
    
    return ora_html


def get_flag_reason(flag_name):
    """Get human-readable reason for a flag"""
    reasons = {
        'Response Start': 'Response start date is outside course date range',
        'Response End': 'Response end date is outside course date range',
        'Peer Start': 'Peer assessment start date is outside course date range',
        'Peer End': 'Peer assessment end date is outside course date range',
        'Grading Config': 'must_grade should be greater than must_be_graded_by',
        'Date Overlap': 'Response end date should be before peer assessment start date'
    }
    return reasons.get(flag_name, flag_name)