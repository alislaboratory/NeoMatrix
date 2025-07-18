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

@app.route('/api/crypto', methods=['POST'])
def api_crypto():
    data = request.json or {}

    symbols = [s.strip().upper()
               for s in data.get('symbols', [])
               if isinstance(s, str)]
    if not symbols:
        return jsonify(status='error', message='No symbols provided'), 400

    # coin‑line color
    price_hex = data.get('price_color', '#FFFF00').lstrip('#')
    r, g, b = (int(price_hex[i:i+2], 16) for i in (0, 2, 4))

    # refresh interval
    try:
        refresh = int(data.get('refresh_interval', 60))
        if refresh < 1: refresh = 60
    except:
        refresh = 60

    mc.show_crypto_ticker(
        symbols,
        price_color=(r, g, b),
        update_interval=refresh
    )
    return jsonify(status='ok')


@app.route('/api/clear', methods=['POST'])
def api_clear():
    mc.clear()
    return jsonify(status='ok')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
