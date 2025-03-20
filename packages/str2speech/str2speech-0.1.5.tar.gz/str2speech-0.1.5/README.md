# str2speech

## Overview
`str2speech` is a simple command-line tool for converting text to speech using Transformer-based text-to-speech (TTS) models. It supports multiple models and voice presets, allowing users to generate high-quality speech audio from text.

## Latest

Added support for Zyphra Zonos. Just try this out:

```
from str2speech.speaker import Speaker

speaker = Speaker("Zyphra/Zonos-v0.1-transformer")
speaker.text_to_speech("Hello, this is a test!", "output.wav")
```

This expects you to have Zonos installed. If you don't have it yet, run the following:
```
!apt install espeak-ng
!git clone https://github.com/Zyphra/Zonos.git
!cd Zonos && pip install -e .
```

## Features
- Supports multiple TTS models, including `suno/bark-small`, `suno/bark`, and various `facebook/mms-tts` models.
- Allows selection of voice presets.
- Supports text input via command-line arguments or files.
- Outputs speech in `.wav` format.
- Works with both CPU and GPU.

## Installation

To install `str2speech`, first make sure you have `pip` installed, then run:

```sh
pip install str2speech
```

## Usage

### Command Line
Run the script via the command line:

```sh
str2speech --text "Hello, world!" --output hello.wav
```

### Options
- `--text` (`-t`): The text to convert to speech.
- `--file` (`-f`): A file containing text to convert to speech.
- `--voice` (`-v`): The voice preset to use (optional, defaults to a predefined voice).
- `--output` (`-o`): The output `.wav` file name (optional, defaults to `output.wav`).
- `--model` (`-m`): The TTS model to use (optional, defaults to `suno/bark-small`).

Example:
```sh
str2speech --file input.txt --output speech.wav --model suno/bark
```

## API Usage

You can also use `str2speech` as a Python module:

```python
from str2speech.speaker import Speaker

speaker = Speaker()
speaker.text_to_speech("Hello, this is a test.", "test.wav")
```

## Available Models

The following models are supported:
- `suno/bark-small` (default)
- `suno/bark`
- `facebook/mms-tts-eng`
- `facebook/mms-tts-deu`
- `facebook/mms-tts-fra`
- `facebook/mms-tts-spa`
- `Zyphra/Zonos-v0.1-transformer`

## Tested With These Dependencies
- `transformers==4.49.0`
- `torch==2.5.1+cu124`
- `numpy==2.2.3`
- `scipy==1.13.1`

## License
This project is licensed under the GNU General Public License v3 (GPLv3).