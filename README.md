# psc2


# Installation

To install locally for development the `psc` package, first make
sure to have your conda env activated, then from the root of the repo run
```
pip install -e .
```

You do not need to rerun this command when you add files or edit them (`-e` flag).


## Notes from Alex

For downloading audio only in compressed format:

```bash
yt-dlp -f 139 URL
```


You can run this from python with `subprocess`:

```python
from pathlib import Path
import subprocess as sp

url = ...
download_path = Path.home() / "Downloads/conferences"
download_path.mkdir(exist_ok=True, parents=True)
sp.run(['yt-dlp'm, '-f', '139', URL], cwd=download_path, check=True)
```

Gives a .m4a file, you can either convert it to a wav as a first step, for instance
```bash
ffmpeg -y -i INPUT_M4A_FILE -ac 1 -ar 16000 OUTPUT_WAV_FILE
```

`-y` means that `ffmpeg` can override the `OUTPUT_WAV_FILE`.

You can run this in a loop using the `subprocess.run` for instance.

You can also load the audio directly from the m4a using `audiocraft.data.audio` (add `audiocraft` to the requirements).
It still uses `ffmpeg` under the hood,

```python
from audiocraft.data.audio import audio_read
from audiocraft.data.audio_utils import convert_audio
wav, sr = audio_read("path_to_file.m4a")
# convert_audio will convert the sample rate and the number of channels to a given target.
# here for instance we convert to 16khz and mono audio, needs to check what
# the model you are using wants as input!!
wav = convert_audio(wav, sr, to_rate=16000, to_channels=1)
wav = wav.numpy()  # for librosa
```
