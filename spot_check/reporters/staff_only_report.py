def generate_staff_only_html(staff_only_content):
    """
    Generate HTML for staff-only content section.
    Shows content that is hidden from students.
    """
    staff_only_html = ""
    
    if staff_only_content:
        staff_only_html += "<h3>Staff-Only Content</h3>"
        staff_only_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        staff_only_html += "<thead><tr><th scope='col'>Content Name</th><th scope='col'>Type</th><th scope='col'>Studio Link</th></tr></thead>"
        staff_only_html += "<tbody>"
        
        for item in staff_only_content:
            item_name = item['name']
            item_type = item['type'].capitalize()
            studio_link = item['studio_link']
            link_text = item['link_text']
            
            # Create clickable link for item name
            item_link = f"<a href='{studio_link}' target='_blank'>{item_name}</a>"
            
            staff_only_html += "<tr>"
            staff_only_html += f"<td>{item_link}</td>"
            staff_only_html += f"<td>{item_type}</td>"
            staff_only_html += f"<td><a href='{studio_link}' target='_blank'>{link_text}</a></td>"
            staff_only_html += "</tr>"
        
        staff_only_html += "</tbody></table>"
    else:
        staff_only_html += "<h3>Staff-Only Content</h3>"
        staff_only_html += "<p>✅ No staff-only content found</p>"
    
    return staff_only_html