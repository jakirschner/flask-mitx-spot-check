def generate_draft_units_html(draft_units):
    """
    Generate HTML for draft units section.
    Shows all draft units with links to edit them in studio.
    """
    draft_units_html = ""
    
    if draft_units:
        draft_units_html += "<h3>⚠️ Units in Draft</h3>"
        draft_units_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        draft_units_html += "<thead><tr><th scope='col'>Unit Name</th></tr></thead>"
        draft_units_html += "<tbody>"
        
        for draft in draft_units:
            unit_name = draft['name']
            studio_link = draft['studio_link']
            
            # Create clickable link
            unit_link = f"<a href='{studio_link}' target='_blank'>{unit_name}</a>"
            
            draft_units_html += "<tr>"
            draft_units_html += f"<td>{unit_link}</td>"
            draft_units_html += "</tr>"
        
        draft_units_html += "</tbody></table>"
    else:
        draft_units_html += "<p>✅ No draft units found</p>"
    
    return draft_units_html