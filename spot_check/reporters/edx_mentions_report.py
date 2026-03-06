def generate_edx_mentions_html(edx_mentions):
    """
    Generate HTML for edX mentions section.
    Shows edX mentions with 'edX' bolded within the context sentence.
    """
    edx_mentions_html = ""
    
    if edx_mentions:
        edx_mentions_html += "<h3>⚠️ edX Mentions</h3>"
        edx_mentions_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        edx_mentions_html += "<thead><tr><th scope='col'>Unit</th><th scope='col'>Context</th></tr></thead>"
        edx_mentions_html += "<tbody>"
        
        for mention in edx_mentions:
            vertical_name = mention['vertical_info']['name'] if mention['vertical_info'] else 'Unknown'
            studio_link = mention['studio_link']
            context = mention['context']
            
            # Create clickable link if we have a studio link
            if studio_link:
                unit_link = f"<a href='{studio_link}' target='_blank'>{vertical_name}</a>"
            else:
                unit_link = vertical_name
            
            # Bold "edX" within the context (case-insensitive replace, first occurrence)
            import re
            context_with_bold = re.sub(r'\bedX\b', '<strong>edX</strong>', context, flags=re.IGNORECASE, count=1)
            
            edx_mentions_html += "<tr>"
            edx_mentions_html += f"<td>{unit_link}</td>"
            edx_mentions_html += f"<td><em style='color: #333;'>{context_with_bold}</em></td>"
            edx_mentions_html += "</tr>"
        
        edx_mentions_html += "</tbody></table>"
    else:
        edx_mentions_html += "<p>✅ No edX mentions found</p>"
    
    return edx_mentions_html