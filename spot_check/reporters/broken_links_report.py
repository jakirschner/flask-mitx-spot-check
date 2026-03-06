def generate_broken_links_html(broken_links):
    """
    Generate HTML for broken links section.
    Shows links in context with link text bolded within the sentence.
    """
    broken_links_html = ""
    
    if broken_links:
        broken_links_html += "<h3>⚠️ Broken Links</h3>"
        broken_links_html += "<p>This report pulls any links that appear to be broken in your course. Note that it may flag links that are actually working but timed out on load. It may also highlight links that are behind login screens or are redirecting to other places.</p>"
        broken_links_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        broken_links_html += "<thead><tr><th scope='col'>Unit</th><th scope='col'>Link Text in Context</th><th scope='col'>Status</th></tr></thead>"
        broken_links_html += "<tbody>"
        
        for link in broken_links:
            context = link.get('context', 'N/A')
            status = link['status']['reason']
            vertical_name = link['vertical_info']['name'] if link['vertical_info'] else 'Unknown'
            studio_link = link['studio_link']
            link_text = link['link_text']
            
            # Create clickable link if we have a studio link
            if studio_link:
                unit_link = f"<a href='{studio_link}' target='_blank'>{vertical_name}</a>"
            else:
                unit_link = vertical_name
            
            # Bold the link text within the context
            context_with_bold = context.replace(link_text, f"<strong>{link_text}</strong>", 1)
            
            broken_links_html += "<tr>"
            broken_links_html += f"<td>{unit_link}</td>"
            broken_links_html += f"<td><em style='color: #333;'>{context_with_bold}</em></td>"
            broken_links_html += f"<td>{status}</td>"
            broken_links_html += "</tr>"
        
        broken_links_html += "</tbody></table>"
    else:
        broken_links_html += "<p>✅ No broken links found</p>"
    
    return broken_links_html