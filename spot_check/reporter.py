from datetime import datetime
from spot_check.checkers import check_broken_links, find_edx_mentions, find_draft_units

def generate_html_report(course_info, course_dir):
    """Generate the HTML report"""
    
    # Format dates
    start_date = format_date(course_info.get('start_date', 'Unknown'))
    end_date = format_date(course_info.get('end_date', 'Unknown'))
    
    # Run checks
    broken_links = check_broken_links(course_dir, course_info)
    edx_mentions = find_edx_mentions(course_dir, course_info)
    
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