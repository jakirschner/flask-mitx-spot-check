from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Spot Check Tool</h1>
    <form action="/check" method="post">
        <input type="file" name="tarball" accept=".tar.gz">
        <button type="submit">Upload</button>
    </form>
    '''

@app.route('/check', methods=['POST'])
def check_course():
    file = request.files['tarball']
    return f'Received file: {file.filename}'

if __name__ == '__main__':
    app.run(debug=True)