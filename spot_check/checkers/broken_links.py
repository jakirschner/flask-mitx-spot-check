import os
import requests
from bs4 import BeautifulSoup
from .utils import find_vertical_for_html, build_studio_link, get_link_context


def find_external_links(course_dir):
    """
    Find all external links in HTML files.
    Returns a list of dicts with link info and the HTML file it came from.
    """
    links = []
    html_dir = os.path.join(course_dir, 'course', 'html')
    
    if not os.path.exists(html_dir):
        print("DEBUG: No html directory found")
        return links
    
    print(f"DEBUG: HTML directory: {html_dir}")
    
    # Loop through all HTML files (both .xml and .html)
    for filename in os.listdir(html_dir):
        if not (filename.endswith('.xml') or filename.endswith('.html')):
            continue
        
        filepath = os.path.join(html_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse HTML content
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find all <a> tags
            for a_tag in soup.find_all('a', href=True):
                href = a_tag.get('href', '').strip()
                link_text = a_tag.get_text(strip=True)
                
                # Skip anchor links
                if href.startswith('#'):
                    continue
                
                # Skip internal MITx links (start with /)
                if href.startswith('/'):
                    continue
                
                # Skip empty links
                if not href or href == '':
                    continue
                
                # Check if it's an external link
                if href.startswith('http'):
                    links.append({
                        'url': href,
                        'link_text': link_text if link_text else href,
                        'html_file': filename,
                        'filepath': filepath,
                        'content': content
                    })
            
            # Find all iframes (except Qualtrics)
            for iframe in soup.find_all('iframe', src=True):
                src = iframe.get('src', '').strip()
                
                # Skip Qualtrics iframes
                if 'qualtrics.com' in src.lower():
                    continue
                
                # Skip internal links
                if src.startswith('/'):
                    continue
                
                if src.startswith('http'):
                    links.append({
                        'url': src,
                        'link_text': '[iframe]',
                        'html_file': filename,
                        'filepath': filepath,
                        'content': content,
                        'type': 'iframe'
                    })
        
        except Exception as e:
            print(f"DEBUG: Error reading {filename}: {str(e)}")
    
    print(f"DEBUG: Found {len(links)} external links total")
    return links


def check_link_status(url, timeout=5):
    """
    Check if a link is valid.
    Returns a dict with status, code, and reason.
    """
    try:
        response = requests.head(url, allow_redirects=False, timeout=timeout)
        
        # Determine if broken
        if response.status_code == 404:
            return {'valid': False, 'code': 404, 'reason': 'Not Found'}
        elif response.status_code == 410:
            return {'valid': False, 'code': 410, 'reason': 'Gone'}
        elif response.status_code in [301, 302, 307, 308]:
            return {'valid': False, 'code': response.status_code, 'reason': 'Redirect'}
        elif response.status_code in [401, 403]:
            return {'valid': False, 'code': response.status_code, 'reason': 'Access Denied'}
        elif response.status_code >= 500:
            return {'valid': False, 'code': response.status_code, 'reason': 'Server Error'}
        elif 200 <= response.status_code < 300:
            return {'valid': True, 'code': response.status_code, 'reason': 'OK'}
        else:
            return {'valid': False, 'code': response.status_code, 'reason': 'Unknown'}
    
    except requests.Timeout:
        return {'valid': False, 'code': 'TIMEOUT', 'reason': 'Timeout'}
    except requests.ConnectionError:
        return {'valid': False, 'code': 'CONNECTION_ERROR', 'reason': 'Connection Error'}
    except Exception as e:
        return {'valid': False, 'code': 'ERROR', 'reason': 'Error'}


def check_broken_links(course_dir, course_info):
    """
    Main function to check all broken links.
    """
    print("DEBUG: Starting broken links check...")
    
    # Collect all links
    links = find_external_links(course_dir)
    
    # Check each link
    broken_links = []
    for link_info in links:
        url = link_info['url']
        status = check_link_status(url)
        
        if not status['valid']:
            # Find the vertical that contains this HTML file
            vertical_info = find_vertical_for_html(course_dir, link_info['html_file'])
            studio_link = build_studio_link(course_info, vertical_info) if vertical_info else None
            
            # Get context
            context = get_link_context(
                link_info['content'],
                link_info['link_text'],
                url
            )
            
            link_info['status'] = status
            link_info['vertical_info'] = vertical_info
            link_info['studio_link'] = studio_link
            link_info['context'] = context
            broken_links.append(link_info)
            print(f"DEBUG: Broken link found: {url} ({status['reason']})")
    
    print(f"DEBUG: Found {len(broken_links)} broken links")
    return broken_links