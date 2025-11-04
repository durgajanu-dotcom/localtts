from tts import synthesize
import os

def main():
    text = "This is a smoke test of the local TTS system."
    out = os.path.join('output', 'smoke_test.wav')
    os.makedirs('output', exist_ok=True)
    path = synthesize(text, out)
    print('Wrote file:', path)
    if os.path.exists(path):
        print('Smoke test OK')
    else:
        raise SystemExit('Smoke test failed: file not created')

if __name__ == '__main__':
    main()
