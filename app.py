from flask import Flask, render_template, request, jsonify
import io
import contextlib
import base64
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.json.get('code', '')
    output = ''
    image_data = None
    try:
        with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec_globals = {'plt': plt}
            exec(code, exec_globals)
            output = buf.getvalue()

            # Check if a plot was created
            if plt.get_fignums():
                image_path = 'static/plot.png'
                plt.savefig(image_path)
                plt.close()
                with open(image_path, 'rb') as img_file:
                    image_data = base64.b64encode(img_file.read()).decode('utf-8')
                os.remove(image_path)
    except Exception as e:
        output = str(e)

    return jsonify({'output': output, 'image': image_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)

