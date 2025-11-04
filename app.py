from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify
import os
import uuid
from tts import synthesize, list_voices
from threading import Timer

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')
OUTPUT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Removed server-side download flow for inline playback; keep compatibility
        text = request.form.get('text', '').strip()
        rate = request.form.get('rate')
        voice = request.form.get('voice')
        if not text:
            flash('Please enter text to synthesize', 'warning')
            return redirect(url_for('index'))
        # fallback: synthesize and return as download if user posts the form
        filename = os.path.join(OUTPUT_DIR, f"tts_{uuid.uuid4().hex}.wav")
        try:
            rate_val = int(rate) if rate else None
        except ValueError:
            rate_val = None
        try:
            path = synthesize(text, filename, rate=rate_val, voice=voice or None)
            return send_file(path, as_attachment=True)
        except Exception as e:
            flash(f'Error during synthesis: {e}', 'danger')
            return redirect(url_for('index'))

    voices = list_voices()
    return render_template('index.html', voices=voices)


def _delete_later(path, delay=30):
    def _del():
        try:
            os.remove(path)
        except Exception:
            pass
    Timer(delay, _del).start()


@app.route('/speak', methods=['POST'])
def speak():
    # Accept form-encoded or JSON
    text = request.form.get('text') if request.form.get('text') is not None else (request.json or {}).get('text')
    rate = request.form.get('rate') if request.form.get('rate') is not None else (request.json or {}).get('rate')
    voice = request.form.get('voice') if request.form.get('voice') is not None else (request.json or {}).get('voice')
    if not text:
        return ('Missing text', 400)
    filename = os.path.join(OUTPUT_DIR, f"tts_{uuid.uuid4().hex}.wav")
    try:
        try:
            rate_val = float(rate) if rate else None
        except Exception:
            rate_val = None
        synthesize(text, filename, rate=rate_val, voice=voice or None)
        # schedule deletion after a short time so disk doesn't fill up
        _delete_later(filename, delay=30)
        return send_file(filename, mimetype='audio/wav', as_attachment=False)
    except Exception as e:
        return (str(e), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
