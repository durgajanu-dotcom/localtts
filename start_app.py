import webbrowser
import threading
import time

# Import Flask app from app.py
from app import app

def run_server():
    # running in a thread so we can open the browser
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    # give server a moment to start
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')
    try:
        # keep main thread alive while server runs
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Shutting down')
