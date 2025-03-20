# SeaVAD

SeaVAD is a Python package for Voice Activity Detection (VAD) using a state machine version of SileroVAD os you can control the performance.

## Installation

You can install SeaVAD using pip:

```bash
pip install SeaVAD
```

## Usage

Here is a simple example of how to use SeaVAD:

```python
from seavad.main import SeaVAD

# Load your audio file
audio_path = 'path/to/your/audio/file.wav'
with open(test_audio, "r") as f:
    f.seek(44)
    audio_data = f.read()

# Local VAD onnx model path
model_file_path = 'path/to/vad/onnx/model'

# Create a SeaVAD object with the sample rate and sample width of your audio.
# Only 16000 and 8000 sample_rate supported
vad = SeaVAD(model_file_path=model_file_path, sample_rate=16000, sample_width=2)

# Detect voice activity
segments = vad.get_vad_segments(audio_data)

# Print the detected segments
for (start, end) in segments:
    print(f"Start: {start}, End: {end}")
```

## License

See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact us at info@seasalt.ai
