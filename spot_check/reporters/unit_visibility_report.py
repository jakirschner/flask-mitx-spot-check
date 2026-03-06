def generate_unit_visibility_html(units_with_issues, course_info):
    """
    Generate HTML for unit visibility section.
    Shows units that are either Staff-Only or in Draft status.
    Staff-Only takes precedence over Draft.
    """
    visibility_html = ""
    
    if units_with_issues:
        # Determine if any are critical
        has_draft = any(unit['status'] == 'Draft' for unit in units_with_issues)
        icon = "⚠️"
        
        visibility_html += f"<h3>{icon} Unit Visibility</h3>"
        visibility_html += "<p>Staff-only units are hidden from learners. Draft units contain unpublished changes that learners won't see until published. Review each unit below to ensure its visibility status is intentional.</p>"
        
        # Create accessible table
        visibility_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        visibility_html += "<thead><tr><th scope='col'>Unit Name</th><th scope='col'>Status</th></tr></thead>"
        visibility_html += "<tbody>"
        
        for unit in units_with_issues:
            unit_name = unit['name']
            status = unit['status']
            
            # Create studio link if available
            if unit['studio_link']:
                unit_link = f"<a href='{unit['studio_link']}' target='_blank'>{unit_name}</a>"
            else:
                unit_link = unit_name
            
            # Status styling
            if status == 'Staff-Only':
                status_display = f"<strong>Staff-Only</strong>"
            else:  # Draft
                status_display = f"<strong>Draft</strong>"
            
            visibility_html += "<tr>"
            visibility_html += f"<td>{unit_link}</td>"
            visibility_html += f"<td>{status_display}</td>"
            visibility_html += "</tr>"
        
        visibility_html += "</tbody></table>"
    else:
        visibility_html += "<h3>Unit Visibility</h3>"
        visibility_html += "<p>✅ All units have appropriate visibility settings (no staff-only or draft units found)</p>"
    
    return visibility_html