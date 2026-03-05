def generate_edx_mentions_html(edx_mentions):
    """
    Generate HTML for edX mentions section.
    """
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
    
    return edx_mentions_html