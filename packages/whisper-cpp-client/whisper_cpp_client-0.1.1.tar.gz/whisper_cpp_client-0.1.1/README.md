# Whisper CPP Client in Python
A small, lightweight python client for the [Whisper.cpp server](https://github.com/ggerganov/whisper.cpp).


## Prerequisites
You need to have the Whisper.cpp server running in your network. You can find the server code in the [Whisper.cpp repository](https://github.com/ggerganov/whisper.cpp/tree/master/examples/server).

## Installation
To install the Whisper CPP client, you can use pip:
```bash
pip install whisper-cpp-client
```

## Usage
To use the Whisper CPP client, you can import the `WhisperClient` class from the `whisper_cpp_client` module:

```python
from whisper_cpp_client import WhisperClient
import json

client = WhisperClient("localhost", 3333)

try:
    response_content = client.transcribe("path/to/audio/file.wav")

    # How you handle the response_content, depends on the response_format
    # parameter which defaults to 'json'.
    data = json.loads(response_content)
    print(data)
except Exception as e:
    print('Handle errors...')
```

The client basically only has two methods: `transcribe` and `set_params`. The `transcribe` method takes an audio file path (only 16-bit WAV files are supported by whisper.cpp) and returns the transcription result, while the `set_params` expects a dictionary of parameters that will be passed to the Whisper.cpp server.


These are the available parameters with the default values based on the Whisper.cpp server configuration (consult the [whisper.cpp documentation](https://github.com/ggerganov/whisper.cpp/tree/master) for more details):

```python
params = {
  'response_format': 'json', # json, text, srt, verbose_json, vtt
  'temperature': 0.0,
  'temperature_inc': 0.2,
  'offset_t': 0,
  'offset_n': 0,
  'duration': 0,
  'progress_step': 5,
  'max_context': -1,
  'max_len': 0,
  'best_of': 2,
  'beam_size': -1,
  'audio_ctx': 0,
  'word_thold': 0.01,
  'entropy_thold': 2.4,
  'logprob_thold': -1.0,
  'no_speech_thold': 0.6,
  'debug_mode': False,
  'translate': False,
  'detect_language': False,
  'diarize': False,
  'tinydiarize': False,
  'split_on_word': False,
  'no_fallback': False,
  'print_special': False,
  'print_colors': False,
  'print_realtime': False,
  'print_progress': False,
  'no_timestamps': False,
  'use_gpu': True,
  'flash_attn': False,
  'suppress_nst':False
}

client = WhisperClient("localhost", 3333)
client.set_params(params)
```


## Development
Create a `venv` install dependencies and run the example:

```bash
python -m venv .
source venv/bin/activate
pip install -r requirements.txt
python examples/test.py
```

## Distribution
To build and upload to pypi, first update version in `__init__.py` and the `pyproject.toml` then run run:

```bash
rm -r dist
python -m build
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*
```