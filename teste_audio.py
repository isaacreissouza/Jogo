# teste_audio.py
import audio
import inspect
print("audio.__file__:", getattr(audio, '__file__', 'NÃO ENCONTRADO'))
Sound = getattr(audio, 'Sound', None)
print("Sound repr:", Sound)
try:
    print("inspect.signature(Sound):", inspect.signature(Sound))
except Exception as e:
    print("inspect.signature erro:", e)
