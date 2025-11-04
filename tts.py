import pyttsx3
import threading
import os

_engine_lock = threading.Lock()
_engine = None

def _init_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
    return _engine

def synthesize(text: str, filename: str, rate: int = None, voice=None) -> str:
    if not text:
        raise ValueError('text must not be empty')
    dirname = os.path.dirname(os.path.abspath(filename))
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)
    with _engine_lock:
        engine = _init_engine()
        # optional rate: allow either an absolute int (words per minute) or a float multiplier
        if rate is not None:
            try:
                # get current/default rate
                try:
                    current = engine.getProperty('rate')
                except Exception:
                    current = None
                # if rate looks like a float, treat as multiplier
                if isinstance(rate, float) or (isinstance(rate, str) and '.' in str(rate)):
                    try:
                        mult = float(rate)
                        if current is not None:
                            engine.setProperty('rate', int(current * mult))
                        else:
                            engine.setProperty('rate', mult)
                    except Exception:
                        pass
                else:
                    # treat as absolute integer
                    try:
                        engine.setProperty('rate', int(rate))
                    except Exception:
                        pass
            except Exception:
                pass
        if voice is not None:
            try:
                engine.setProperty('voice', voice)
            except Exception:
                pass
        engine.save_to_file(text, filename)
        engine.runAndWait()
    return os.path.abspath(filename)

def list_voices():
    with _engine_lock:
        engine = _init_engine()
        voices = engine.getProperty('voices')
        out = []
        for v in voices:
            out.append({
                'id': getattr(v, 'id', None),
                'name': getattr(v, 'name', None),
                'languages': getattr(v, 'languages', None),
            })
        return out
