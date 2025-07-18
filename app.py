from flask import Flask, render_template, request, jsonify
from matrix_controller import MatrixController

app = Flask(__name__, static_folder='static', template_folder='templates')
mc = MatrixController()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/text', methods=['POST'])
def api_text():
    text = request.form.get('text', '')
    mc.show_text(text)
    return jsonify(status='ok')

@app.route('/api/program', methods=['POST'])
def api_program():
    prog = request.json.get('program', '')
    mc.run_program(prog)
    return jsonify(status='ok')

@app.route('/api/pixel', methods=['POST'])
def api_pixel():
    data = request.json
    x = int(data.get('x', 0))
    y = int(data.get('y', 0))
    r = int(data.get('r', 0))
    g = int(data.get('g', 0))
    b = int(data.get('b', 0))
    on = data.get('on', True)
    color = (r, g, b) if on else (0, 0, 0)
    mc.set_pixel(x, y, color)
    return jsonify(status='ok')

@app.route('/api/clear', methods=['POST'])
def api_clear():
    mc.clear()
    return jsonify(status='ok')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
