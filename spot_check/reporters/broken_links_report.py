def generate_broken_links_html(broken_links):
    """
    Generate HTML for broken links section.
    """
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
    
    return broken_links_html