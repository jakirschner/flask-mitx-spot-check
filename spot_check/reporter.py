from datetime import datetime
from spot_check.checkers import check_broken_links, find_edx_mentions, find_draft_units, find_fbe_gating, find_staff_only_content
from spot_check.reporters import (
    generate_broken_links_html,
    generate_edx_mentions_html,
    generate_draft_units_html,
    generate_fbe_settings_html,
    generate_staff_only_html,
)


def generate_html_report(course_info, course_dir):
    """Generate the HTML report"""
    
    # Format dates
    start_date = format_date(course_info.get('start_date', 'Unknown'))
    end_date = format_date(course_info.get('end_date', 'Unknown'))
    
    # Run all checks
    broken_links = check_broken_links(course_dir, course_info)
    edx_mentions = find_edx_mentions(course_dir, course_info)
    draft_units = find_draft_units(course_dir, course_info)
    fbe_settings = find_fbe_gating(course_dir, course_info)
    staff_only_content = find_staff_only_content(course_dir, course_info)
    
    # Generate HTML for each section
    broken_links_html = generate_broken_links_html(broken_links)
    edx_mentions_html = generate_edx_mentions_html(edx_mentions)
    draft_units_html = generate_draft_units_html(draft_units)
    fbe_settings_html = generate_fbe_settings_html(fbe_settings, course_info)
    staff_only_html = generate_staff_only_html(staff_only_content)
    
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
            {staff_only_html}
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