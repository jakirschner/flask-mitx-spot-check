from datetime import datetime
from spot_check.checkers import (
    check_broken_links,
    find_edx_mentions,
    find_draft_units,
    find_fbe_gating,
    find_staff_only_content,
    check_release_dates,
    find_date_mentions,
    find_ora_dates,
    find_videos,
    find_discussions_issues,
    find_course_updates_issues,
)
from spot_check.reporters import (
    generate_broken_links_html,
    generate_edx_mentions_html,
    generate_draft_units_html,
    generate_fbe_settings_html,
    generate_staff_only_html,
    generate_release_dates_html,
    generate_date_mentions_html,
    generate_ora_dates_html,
    generate_videos_html,
    generate_discussions_html,
    generate_course_updates_html,
    generate_membership_roles_html,
    generate_grading_policy_html,
)


def count_issues(data):
    """Count flagged items in checker results"""
    if isinstance(data, list):
        return len([item for item in data if item.get('flags')])
    elif isinstance(data, dict):
        return len([v for v in data.values() if isinstance(v, list) and v])
    return 0


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
    release_dates_result = check_release_dates(course_dir, course_info)
    date_mentions = find_date_mentions(course_dir, course_info)
    ora_dates = find_ora_dates(course_dir, course_info)
    videos = find_videos(course_dir, course_info)
    discussions_info = find_discussions_issues(course_dir, course_info)
    course_updates = find_course_updates_issues(course_dir, course_info)
    
    # Count issues for tab badges
    content_issues = len(broken_links) + len(edx_mentions) + len(draft_units) + len(staff_only_content)
    dates_issues = len(release_dates_result) + len(date_mentions) + len(ora_dates)
    video_issues = len(videos)
    settings_issues = len(discussions_info['flags']) if isinstance(discussions_info, dict) else 0
    settings_issues += len(course_updates)
    
    # Generate HTML for each section
    broken_links_html = generate_broken_links_html(broken_links)
    edx_mentions_html = generate_edx_mentions_html(edx_mentions)
    draft_units_html = generate_draft_units_html(draft_units)
    fbe_settings_html = generate_fbe_settings_html(fbe_settings, course_info)
    staff_only_html = generate_staff_only_html(staff_only_content)
    release_dates_html = generate_release_dates_html(release_dates_result, course_info)
    date_mentions_html = generate_date_mentions_html(date_mentions)
    ora_dates_html = generate_ora_dates_html(ora_dates, course_info)
    videos_html = generate_videos_html(videos, course_info)
    discussions_html = generate_discussions_html(discussions_info, course_info)
    course_updates_html = generate_course_updates_html(course_updates, course_info)
    membership_roles_html = generate_membership_roles_html(course_info)
    grading_policy_html = generate_grading_policy_html(course_info)
    
    # Build tab badge HTML
    content_badge = f"<span class='tab-badge {'critical' if content_issues > 0 else 'none'}'>{content_issues}</span>" if content_issues > 0 else ""
    dates_badge = f"<span class='tab-badge {'critical' if dates_issues > 0 else 'none'}'>{dates_issues}</span>" if dates_issues > 0 else ""
    video_badge = f"<span class='tab-badge {'critical' if video_issues > 0 else 'none'}'>{video_issues}</span>" if video_issues > 0 else ""
    settings_badge = f"<span class='tab-badge {'critical' if settings_issues > 0 else 'none'}'>{settings_issues}</span>" if settings_issues > 0 else ""
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Spot Check Report - {course_info.get('title', 'Course')}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            html {{
                scroll-behavior: smooth;
            }}
            
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                padding: 20px;
                color: #333;
                line-height: 1.6;
            }}
            
            .header {{
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            
            .header h1 {{
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #333;
            }}
            
            .course-info {{
                font-size: 14px;
                color: #666;
                line-height: 1.5;
            }}
            
            .tabs {{
                display: flex;
                gap: 0;
                margin-bottom: 0;
                border-bottom: 2px solid #ddd;
                background-color: white;
                border-radius: 5px 5px 0 0;
                flex-wrap: wrap;
            }}
            
            .tab-button {{
                padding: 15px 25px;
                border: none;
                background-color: #e0e0e0;
                color: #333;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px 5px 0 0;
                transition: background-color 0.3s;
                margin-right: 5px;
                display: flex;
                align-items: center;
                gap: 10px;
                outline: none;
            }}
            
            .tab-button:hover {{
                background-color: #d0d0d0;
            }}
            
            .tab-button:focus {{
                outline: 3px solid #0066cc;
                outline-offset: -3px;
            }}
            
            .tab-button:focus:not(:focus-visible) {{
                outline: none;
            }}
            
            .tab-button:focus-visible {{
                outline: 3px solid #0066cc;
                outline-offset: -3px;
            }}
            
            .tab-button.active {{
                background-color: white;
                color: #333;
                border-bottom: 3px solid white;
            }}
            
            .tab-badge {{
                background-color: #c41e3a;
                color: white;
                padding: 2px 6px;
                border-radius: 10px;
                font-size: 11px;
                font-weight: bold;
                min-width: 20px;
                text-align: center;
            }}
            
            .tab-badge.none {{
                background-color: #4caf50;
            }}
            
            .tab-content {{
                display: none;
                background-color: white;
                padding: 20px;
                border-radius: 0 5px 5px 5px;
            }}
            
            .tab-content.active {{
                display: block;
            }}
            
            .tab-content h2 {{
                font-size: 20px;
                margin-bottom: 20px;
                color: #333;
            }}
            
            .checker-section {{
                margin-bottom: 30px;
                padding-bottom: 30px;
                border-bottom: 1px solid #e0e0e0;
            }}
            
            .checker-section:last-child {{
                border-bottom: none;
                margin-bottom: 0;
                padding-bottom: 0;
            }}
            
            .checker-section h3 {{
                font-size: 16px;
                margin-bottom: 10px;
                color: #333;
            }}
            
            .checker-section h4 {{
                font-size: 14px;
                margin-bottom: 8px;
                color: #333;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
            }}
            
            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }}
            
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
                color: #333;
            }}
            
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            p {{
                line-height: 1.6;
                margin-bottom: 10px;
                color: #333;
            }}
            
            a {{
                color: #0066cc;
                text-decoration: underline;
                outline: none;
            }}
            
            a:hover {{
                color: #0052a3;
            }}
            
            a:focus {{
                outline: 2px solid #0066cc;
                outline-offset: 2px;
            }}
            
            a:focus:not(:focus-visible) {{
                outline: none;
            }}
            
            a:focus-visible {{
                outline: 2px solid #0066cc;
                outline-offset: 2px;
            }}
            
            details {{
                margin: 10px 0;
            }}
            
            summary {{
                cursor: pointer;
                font-weight: bold;
                padding: 8px;
                background-color: #f9f9f9;
                border-radius: 3px;
                user-select: none;
                outline: none;
            }}
            
            summary:hover {{
                background-color: #f0f0f0;
            }}
            
            summary:focus {{
                outline: 2px solid #0066cc;
                outline-offset: 2px;
            }}
            
            summary:focus:not(:focus-visible) {{
                outline: none;
            }}
            
            summary:focus-visible {{
                outline: 2px solid #0066cc;
                outline-offset: 2px;
            }}
            
            details > div {{
                padding: 10px;
                background-color: #f9f9f9;
                margin-top: 5px;
                border-left: 3px solid #a31f34;
            }}
            
            ul, ol {{
                margin-left: 20px;
                margin-bottom: 10px;
            }}
            
            li {{
                margin-bottom: 5px;
                line-height: 1.6;
            }}
        </style>
        <script>
            function openTab(event, tabName) {{
                // Hide all tab contents
                var tabContents = document.getElementsByClassName('tab-content');
                for (var i = 0; i < tabContents.length; i++) {{
                    tabContents[i].classList.remove('active');
                }}
                
                // Remove active class from all buttons
                var tabButtons = document.getElementsByClassName('tab-button');
                for (var i = 0; i < tabButtons.length; i++) {{
                    tabButtons[i].classList.remove('active');
                }}
                
                // Show the current tab and mark button as active
                document.getElementById(tabName).classList.add('active');
                event.currentTarget.classList.add('active');
                
                // Announce tab change to screen readers
                var tabName_text = event.currentTarget.textContent.trim();
                var announcement = document.createElement('div');
                announcement.setAttribute('role', 'status');
                announcement.setAttribute('aria-live', 'polite');
                announcement.setAttribute('class', 'sr-only');
                announcement.textContent = tabName_text + ' tab opened';
                document.body.appendChild(announcement);
                setTimeout(function() {{ announcement.remove(); }}, 1000);
            }}
            
            // Open first tab by default
            window.onload = function() {{
                document.getElementsByClassName('tab-button')[0].click();
            }};
            
            // Keyboard navigation for tabs
            document.addEventListener('keydown', function(event) {{
                if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {{
                    var tabButtons = document.getElementsByClassName('tab-button');
                    var currentIndex = -1;
                    
                    for (var i = 0; i < tabButtons.length; i++) {{
                        if (tabButtons[i].classList.contains('active')) {{
                            currentIndex = i;
                            break;
                        }}
                    }}
                    
                    if (currentIndex !== -1) {{
                        var nextIndex = event.key === 'ArrowRight' ? currentIndex + 1 : currentIndex - 1;
                        if (nextIndex < 0) nextIndex = tabButtons.length - 1;
                        if (nextIndex >= tabButtons.length) nextIndex = 0;
                        
                        tabButtons[nextIndex].focus();
                        tabButtons[nextIndex].click();
                    }}
                }}
            }});
        </script>
        <style>
            .sr-only {{
                position: absolute;
                width: 1px;
                height: 1px;
                padding: 0;
                margin: -1px;
                overflow: hidden;
                clip: rect(0,0,0,0);
                white-space: nowrap;
                border-width: 0;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{course_info.get('title', 'Unknown Course')}</h1>
            <div class="course-info">
                <strong>Course Number:</strong> {course_info.get('course_number', 'Unknown')}<br/>
                <strong>Course Run:</strong> {course_info.get('course_run', 'Unknown')}<br/>
                <strong>Course Dates:</strong> {start_date} - {end_date}
            </div>
        </div>
        
        <div class="tabs" role="tablist">
            <button class="tab-button" role="tab" aria-selected="false" aria-controls="content" onclick="openTab(event, 'content')">
                Course Content
                {content_badge}
            </button>
            <button class="tab-button" role="tab" aria-selected="false" aria-controls="dates" onclick="openTab(event, 'dates')">
                Dates
                {dates_badge}
            </button>
            <button class="tab-button" role="tab" aria-selected="false" aria-controls="video" onclick="openTab(event, 'video')">
                Video
                {video_badge}
            </button>
            <button class="tab-button" role="tab" aria-selected="false" aria-controls="settings" onclick="openTab(event, 'settings')">
                Course Settings
                {settings_badge}
            </button>
        </div>
        
        <section id="content" class="tab-content" role="tabpanel" aria-labelledby="content-tab">
            <h2>Course Content</h2>
            <div class="checker-section">
                {broken_links_html}
            </div>
            <div class="checker-section">
                {edx_mentions_html}
            </div>
            <div class="checker-section">
                {draft_units_html}
            </div>
            <div class="checker-section">
                {fbe_settings_html}
            </div>
            <div class="checker-section">
                {staff_only_html}
            </div>
        </section>
        
        <section id="dates" class="tab-content" role="tabpanel" aria-labelledby="dates-tab">
            <h2>Dates</h2>
            <div class="checker-section">
                {release_dates_html}
            </div>
            <div class="checker-section">
                {date_mentions_html}
            </div>
            <div class="checker-section">
                {ora_dates_html}
            </div>
        </section>
        
        <section id="video" class="tab-content" role="tabpanel" aria-labelledby="video-tab">
            <h2>Video</h2>
            <div class="checker-section">
                {videos_html}
            </div>
        </section>
        
        <section id="settings" class="tab-content" role="tabpanel" aria-labelledby="settings-tab">
            <h2>Course Settings</h2>
            <div class="checker-section">
                {discussions_html}
            </div>
            <div class="checker-section">
                {course_updates_html}
            </div>
            <div class="checker-section">
                {membership_roles_html}
            </div>
            <div class="checker-section">
                {grading_policy_html}
            </div>
        </section>
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