# psc2

# Installation

To install locally for development the `psc` package, first make
sure to have your conda env activated, then from the root of the repo run
```bash
pip install -e .
```
You do not need to rerun this command when you add files or edit them (`-e` flag).


----
### Dataset librispeech

On peut directement utiliser un url de téléchargement.

----

### Download of youtube audios

```bash
pip install yt-dlp
```
On va vouloir selectionner un format audio seulement, et le convertir en wav 16000Hz 1 channel.

```bash
yt-dlp -F "url" #---> affiche les formats
```

A priori le `139` sera ce que l'on cherche:

```bash
yt-dlp -f 139 "url"
```

On peut automatiser en mettant dans "urls.txt" les urls des videos que l'on veut downloader.
```python
from pathlib import Path
import subprocess as sp

download_path = Path.home() / "Downloads/conferences"
download_path.mkdir(exist_ok=True, parents=True)
urls = open("urls.txt", "r").readlines()
for url in urls:
   url = url.strip() #on enlève les espaces etc
   if not url:
        continue
    sp.run(['yt-dlp', '-f', '139', url], cwd=download_path, check=True)
```

On obtient un m4a compressé. On peut le convertir en wav 16 kHz mono avec par exemple
```bash
Gives a .m4a file, you can either convert it to a wav as a first step, for instance
```bash
ffmpeg -y -i INPUT_M4A_FILE -ac 1 -ar 16000 OUTPUT_WAV_FILE
```

`-y` means that `ffmpeg` can override the `OUTPUT_WAV_FILE`.

On peut automatiser le processus de la meme maniere:
```python
from pathlib import Path
import subprocess as sp

in_folder = Path.home()/"Downloads/conferences"
out_folder = Path.home()/"Downloads/conferences_resamples"
out_folder.mkdir(exist_ok=True, parents=True)

for file in in_folder.iterdir():
    if file.stem != ".m4a":
        continue

    sp.run(["ffmpeg", "-y", "-i", file, "-ar", "16000", "-ac", "1", out_folder/(file.stem + "wav")], check=True)
```

Finalement on peut garder le m4a qui est plus petit (20MB/heures d'audio) pour le stockage. Pour le traitement, on peut lire depuis python en utilisant par exemple `audiocraft`:

```python
# pip install audiocraft
from audiocraft.data.audio import audio_read
from audiocraft.data.audio_utils import convert_audio
wav, sr = audio_read("path_to_file.m4a")
# convert_audio will convert the sample rate and the number of channels to a given target.
# here for instance we convert to 16khz and mono audio, needs to check what
# the model you are using wants as input!!
wav = convert_audio(wav, sr, to_rate=16000, to_channels=1)
wav = wav.numpy()  # for librosa
```
ou alors vous pouvez faire une fonction qui appelle `ffmpeg` avec `subprocess` et extrait vers un fichier `.wav` temporaire que vous pourrez lire avec `torchaudio` ou `librosa` (voir le package `tempfile` par exemple).


