def generate_date_mentions_html(date_mentions):
    """
    Generate HTML for date mentions in text section.
    Shows dates found in text with date bolded within the context sentence.
    """
    date_mentions_html = ""
    
    if date_mentions:
        date_mentions_html += "<h3>⚠️ Date Mentions in Text</h3>"
        date_mentions_html += "<p>This report looks for any written mentions of dates in your course and flags them if they fall outside the dates of your course run. This tool is intended to help with mentions of dates which should be updated with each course run, but obviously will also flag dates which are references to historic events. Please review the dates that appear here and make sure there is nothing which needs to be changed.<p>"
        date_mentions_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        date_mentions_html += "<thead><tr><th scope='col'>Unit</th><th scope='col'>Date & Context</th></tr></thead>"
        date_mentions_html += "<tbody>"
        
        for mention in date_mentions:
            vertical_name = mention['vertical_info']['name'] if mention['vertical_info'] else 'Unknown'
            studio_link = mention['studio_link']
            date_text = mention['date']
            context = mention['context']
            
            # Create clickable link if we have a studio link
            if studio_link:
                unit_link = f"<a href='{studio_link}' target='_blank'>{vertical_name}</a>"
            else:
                unit_link = vertical_name
            
            # Bold the date within the context
            context_with_bold = context.replace(date_text, f"<strong>{date_text}</strong>", 1)
            
            date_mentions_html += "<tr>"
            date_mentions_html += f"<td>{unit_link}</td>"
            date_mentions_html += f"<td><em style='color: #333;'>{context_with_bold}</em></td>"
            date_mentions_html += "</tr>"
        
        date_mentions_html += "</tbody></table>"
    else:
        date_mentions_html += "<h3>⚠️ Date Mentions in Text</h3>"
        date_mentions_html += "<p>✅ No out-of-range date mentions found in text</p>"
    
    return date_mentions_html