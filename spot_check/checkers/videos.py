import os
import xml.etree.ElementTree as ET


def find_vertical_for_video(course_dir, video_id):
    """
    Find which vertical contains this video.
    Returns the vertical info dict, or None if not found.
    """
    # Search in both draft and non-draft verticals
    for vertical_dir in [
        os.path.join(course_dir, 'course', 'vertical'),
        os.path.join(course_dir, 'course', 'drafts', 'vertical')
    ]:
        if not os.path.exists(vertical_dir):
            continue
        
        for vertical_file in os.listdir(vertical_dir):
            if not vertical_file.endswith('.xml'):
                continue
            
            vertical_path = os.path.join(vertical_dir, vertical_file)
            try:
                tree = ET.parse(vertical_path)
                root = tree.getroot()
                
                # Look for video elements with matching url_name
                for video_elem in root.findall('.//video'):
                    if video_elem.get('url_name') == video_id:
                        # Found it! Return vertical info
                        vertical_name = root.get('display_name', 'Unknown')
                        vertical_id = vertical_file.replace('.xml', '')
                        is_draft = 'drafts' in vertical_dir
                        
                        vertical_info = {
                            'name': vertical_name,
                            'id': vertical_id,
                            'is_draft': is_draft
                        }
                        
                        # If draft, also capture parent_url
                        if is_draft:
                            parent_url = root.get('parent_url', '')
                            if parent_url:
                                vertical_info['parent_url'] = parent_url
                        
                        return vertical_info
            except:
                continue
    
    return None

def find_videos(course_dir, course_info):
    """
    Find all video components and check their properties.
    Returns a list of dicts with video info and flags.
    """
    videos = []
    video_dir = os.path.join(course_dir, 'course', 'video')
    
    if not os.path.exists(video_dir):
        print("DEBUG: No video directory found")
        return videos
    
    print(f"DEBUG: Searching for videos in {video_dir}")
    
    for video_file in os.listdir(video_dir):
        if not video_file.endswith('.xml'):
            continue
        
        video_path = os.path.join(video_dir, video_file)
        try:
            tree = ET.parse(video_path)
            root = tree.getroot()
            
            # Get video info
            display_name = root.get('display_name', 'Unknown Video')
            video_id = video_file.replace('.xml', '')
            
            video_info = {
                'display_name': display_name,
                'video_id': video_id,
                'flags': [],
                'properties': {},
                'vertical_info': None
            }
            
            # Find the vertical that contains this video
            vertical_info = find_vertical_for_video(course_dir, video_id)
            video_info['vertical_info'] = vertical_info
            
            # Check download_video attribute
            download_video = root.get('download_video', 'false')
            video_info['properties']['download_video'] = download_video
            if download_video != 'true':
                video_info['flags'].append(('Not Downloadable', '❌'))
            
            # Check for YouTube
            youtube_id = root.get('youtube_id_1_0', '')
            video_info['properties']['youtube_id'] = youtube_id
            if youtube_id:  # If populated, it's a YouTube video
                video_info['flags'].append(('YouTube Link', '⚠️'))
            
            # Check for transcripts
            transcripts_elem = root.find('.//transcripts')
            has_transcripts = transcripts_elem is not None and len(transcripts_elem) > 0
            video_info['properties']['has_transcripts'] = has_transcripts
            
            if not has_transcripts:
                video_info['flags'].append(('No Transcripts', '❌'))
            else:
                # Check if transcript is downloadable
                download_track = root.get('download_track', 'true')
                video_info['properties']['download_track'] = download_track
                if download_track == 'false':
                    video_info['flags'].append(('No Downloadable Transcripts', '❌'))
            
            # Check for edX video links
            has_edx_link = False
            
            # Check html5_sources attribute
            html5_sources = root.get('html5_sources', '[]')
            if 'edx-video.net' in html5_sources:
                has_edx_link = True
            
            # Check source elements
            for source_elem in root.findall('.//source'):
                src = source_elem.get('src', '')
                if 'edx-video.net' in src:
                    has_edx_link = True
                    break
            
            video_info['properties']['has_edx_link'] = has_edx_link
            if has_edx_link:
                video_info['flags'].append(('edX Link', '❌'))
            
            # Only include videos with flags
            if video_info['flags']:
                videos.append(video_info)
                print(f"DEBUG: Found video with issues: {display_name}")
        
        except Exception as e:
            print(f"DEBUG: Error parsing {video_file}: {str(e)}")
    
    print(f"DEBUG: Found {len(videos)} videos with issues total")
    return videos