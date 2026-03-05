from datetime import datetime

def generate_html_report(course_info):
    """Generate the HTML report"""
    
    # Format dates
    start_date = format_date(course_info.get('start_date', 'Unknown'))
    end_date = format_date(course_info.get('end_date', 'Unknown'))
    
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
            .tabs {{
                display: flex;
                gap: 10px;
                margin: 20px 0;
                border-bottom: 2px solid #ddd;
            }}
            .tab {{
                padding: 10px 20px;
                cursor: pointer;
                background-color: #f0f0f0;
                border: none;
                border-radius: 5px 5px 0 0;
            }}
            .tab.active {{
                background-color: white;
                border-bottom: 3px solid #a31f34;
            }}
            .content {{
                background-color: white;
                padding: 20px;
                border-radius: 5px;
            }}
            .error {{
                color: red;
                background-color: #ffcccc;
                padding: 10px;
                border-radius: 5px;
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
            <h2>Report Generation Status</h2>
            {'<p>✅ Course info parsed successfully!</p>' if not course_info.get('errors') else '<p>⚠️ Warnings:</p>'}
            {''.join([f'<div class="error">{error}</div>' for error in course_info.get('errors', [])])}
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