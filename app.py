from flask import Flask, render_template, request, send_file
import os
import tempfile
from spot_check.extractor import extract_tarball, delete_static_folder
from spot_check.parsers import parse_course_info
from spot_check.reporter import generate_html_report

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/check', methods=['POST'])
def check_course():
    try:
        # Get uploaded file
        if 'tarball' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['tarball']
        
        if file.filename == '':
            return "No file selected", 400
        
        # Create temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            tarball_path = os.path.join(temp_dir, file.filename)
            file.save(tarball_path)
            
            # Extract tarball
            extract_dir = temp_dir
            extract_tarball(tarball_path, extract_dir)
            
            # Delete static folder
            delete_static_folder(extract_dir)
            
            # Parse course info
            course_info = parse_course_info(extract_dir)
            
            # Generate HTML report
            html_content = generate_html_report(course_info, extract_dir)
            
            # Generate filename: [course_number]+[course_run]_spotcheck_YYYYMMDD_HHMMSS.html
            from datetime import datetime, timezone
            course_number = course_info.get('course_number', 'unknown')
            course_run = course_info.get('course_run', 'unknown')
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            filename = f"{course_number}+{course_run}_spotcheck_{timestamp}.html"
            
            # Save to temporary file for download
            output_path = os.path.join(temp_dir, 'report.html')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Send file with proper filename and custom header
            response = send_file(
                output_path,
                mimetype='text/html',
                as_attachment=True,
                download_name=filename
            )
            
            # Add custom header for JavaScript to read
            response.headers['X-Filename'] = filename
            
            return response
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error processing course: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)