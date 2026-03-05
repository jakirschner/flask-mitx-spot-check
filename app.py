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
            
            # Generate HTML report (pass extract_dir so it can run checks)
            html_content = generate_html_report(course_info, extract_dir)
            
            # Save to temporary file for download
            output_path = os.path.join(temp_dir, 'report.html')
            with open(output_path, 'w') as f:
                f.write(html_content)
            
            # Send file
            return send_file(output_path, as_attachment=True, download_name='spot_check_report.html')
    
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)