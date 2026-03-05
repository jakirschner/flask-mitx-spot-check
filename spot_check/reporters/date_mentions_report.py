def generate_date_mentions_html(date_mentions):
    """
    Generate HTML for date mentions in text section.
    """
    date_mentions_html = ""
    
    if date_mentions:
        date_mentions_html += "<h3>⚠️ Date Mentions in Text</h3>"
        date_mentions_html += "<table border='1' style='width:100%; border-collapse:collapse;'>"
        date_mentions_html += "<tr><th>Unit</th><th>Date & Context</th></tr>"
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
            
            date_mentions_html += "<tr>"
            date_mentions_html += f"<td>{unit_link}</td>"
            date_mentions_html += f"<td><strong>{date_text}</strong><br/><em style='color: #666;'>{context}</em></td>"
            date_mentions_html += "</tr>"
        date_mentions_html += "</table>"
    else:
        date_mentions_html += "<h3>⚠️ Date Mentions in Text</h3>"
        date_mentions_html += "<p>✅ No out-of-range date mentions found in text</p>"
    
    return date_mentions_html