def build_video_studio_link(course_info, video_info):
    """
    Build a Studio link to a video's containing vertical.
    Videos are components inside verticals, so we link to the vertical.
    """
    if not video_info or not video_info['vertical_info']:
        return None
    
    vertical = video_info['vertical_info']
    
    course_key = f"course-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}"
    vertical_block_id = f"block-v1:{course_info['org']}+{course_info['course_number']}+{course_info['course_run']}+type@vertical+block@{vertical['id']}"
    
    if vertical['is_draft'] and vertical.get('parent_url'):
        # Draft link includes sequential parent
        return f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/container/{vertical_block_id}/{vertical['parent_url']}"
    else:
        # Non-draft link
        return f"https://studio.courses.learn.mit.edu/authoring/course/{course_key}/container/{vertical_block_id}"


def generate_videos_html(videos, course_info):
    """
    Generate HTML for videos section.
    Shows flagged videos in a table with columns for each issue type.
    """
    videos_html = ""
    
    if videos:
        # Determine if any are critical (❌ flags)
        has_critical = any(any(flag[1] == '❌' for flag in video['flags']) for video in videos)
        icon = "❌" if has_critical else "⚠️"
        
        videos_html += f"<h3>{icon} Videos</h3>"
        
        # Create table with columns for each issue type
        videos_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        videos_html += "<tr><th>Video Name</th><th>Not Downloadable</th><th>No Transcripts</th><th>No Downloadable Transcripts</th><th>YouTube Link</th><th>edX Link</th></tr>"
        
        for video in videos:
            studio_link = build_video_studio_link(course_info, video)
            
            # Create video name link
            if studio_link:
                video_link = f"<a href='{studio_link}' target='_blank'>{video['display_name']}</a>"
            else:
                video_link = video['display_name']
            
            # Check which flags apply
            not_downloadable = ""
            no_transcripts = ""
            no_downloadable_transcripts = ""
            youtube_link = ""
            edx_link = ""
            
            for flag_name, flag_icon in video['flags']:
                if flag_name == 'Not Downloadable':
                    not_downloadable = flag_icon
                elif flag_name == 'No Transcripts':
                    no_transcripts = flag_icon
                elif flag_name == 'No Downloadable Transcripts':
                    no_downloadable_transcripts = flag_icon
                elif flag_name == 'YouTube Link':
                    youtube_link = flag_icon
                elif flag_name == 'edX Link':
                    edx_link = flag_icon
            
            videos_html += f"<tr>"
            videos_html += f"<td>{video_link}</td>"
            videos_html += f"<td>{not_downloadable}</td>"
            videos_html += f"<td>{no_transcripts}</td>"
            videos_html += f"<td>{no_downloadable_transcripts}</td>"
            videos_html += f"<td>{youtube_link}</td>"
            videos_html += f"<td>{edx_link}</td>"
            videos_html += f"</tr>"
        
        videos_html += "</table>"
    else:
        videos_html += "<h3>Videos</h3>"
        videos_html += "<p>✅ No video issues found</p>"
    
    return videos_html