from flask import Flask, render_template, request, send_file, Response
import os
import tempfile
import queue
from datetime import datetime, timezone
from spot_check.extractor import extract_tarball, delete_static_folder
from spot_check.parsers import parse_course_info
from spot_check.reporter import generate_html_report

app = Flask(__name__)

# Global progress queue for SSE
progress_queue = queue.Queue()

def progress_update(message):
    """Send a progress update to connected clients"""
    progress_queue.put(message)
    print(f"DEBUG: Progress - {message}")

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/progress')
def progress():
    """Server-Sent Events endpoint for real-time progress updates"""
    def generate():
        try:
            while True:
                try:
                    message = progress_queue.get(timeout=5)
                    yield f"data: {message}\n\n"
                except queue.Empty:
                    # Keep-alive message every 5 seconds
                    yield f"data: Processing...\n\n"
        except GeneratorExit:
            pass
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

@app.route('/check', methods=['POST'])
def check_course():
    try:
        # Get uploaded file
        if 'tarball' not in request.files:
            progress_update("Error: No file uploaded")
            return "No file uploaded", 400
        
        file = request.files['tarball']
        
        if file.filename == '':
            progress_update("Error: No file selected")
            return "No file selected", 400
        
        # Create temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Save uploaded file
                progress_update("Saving uploaded file...")
                tarball_path = os.path.join(temp_dir, file.filename)
                file.save(tarball_path)
                
                # Extract tarball
                progress_update("Extracting course files...")
                extract_dir = temp_dir
                extract_tarball(tarball_path, extract_dir)
                
                # Delete static folder
                progress_update("Cleaning up temporary files...")
                delete_static_folder(extract_dir)
                
                # Parse course info
                progress_update("Parsing course structure...")
                course_info = parse_course_info(extract_dir)
                
                # Generate HTML report
                progress_update("Generating spot check report...")
                html_content = generate_html_report(course_info, extract_dir)
                
                # Generate filename: [course_number]+[course_run]_spotcheck_YYYYMMDD_HHMMSS.html
                course_number = course_info.get('course_number', 'unknown')
                course_run = course_info.get('course_run', 'unknown')
                timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
                filename = f"{course_number}+{course_run}_spotcheck_{timestamp}.html"
                
                # Save to temporary file for download
                progress_update("Finalizing report...")
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
                
                progress_update("Complete")
                return response
            
            except Exception as e:
                progress_update(f"Error: {str(e)}")
                print(f"Error: {str(e)}")
                return f"Error processing course: {str(e)}", 500
    
    except Exception as e:
        progress_update(f"Error: {str(e)}")
        print(f"Error: {str(e)}")
        return f"Error processing course: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)