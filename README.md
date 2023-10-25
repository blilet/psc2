# psc2

# Installation

To install locally for development the `psc` package, first make
sure to have your conda env activated, then from the root of the repo run
```
pip install -e .
```

You do not need to rerun this command when you add files or edit them (`-e` flag).µM

----
### Dataset librispeech

On peut directement utiliser un url de téléchargement.

----

### Download of youtube audios

```
pip install yt-dlp
```
On va vouloir selectionner un format audio seulement, et le convertir en wav 16000Hz 1 channel. 

```
yt-dlp -F "url" #---> affiche les formats 
```

A priori le `139` sera ce que l'on cherche:

```
yt-dlp -f 139 -x --audio-format wav "url" 
```

On obtient un wav 44100 Hz 2 channels, qu'il faut convertir en 16000Hz 1 channel. 

```
mkdir resampled
file="--"
ffmpeg -i "$file$" -ar 16000 -ac 1 "resampled/$file$"
```

Even better, on peut utiliser un script python pour automatiser

```
from pathlib import Path
import subprocess as sp

in_folder = Path.home()/"--"
out_folder = Path.home()/"--"
outfolder.mkdir(exist_ok=True, parents=True)

for file in in_folder.iterdir():
    if file.stem != ".wav"
        continue

    sp.run(["ffmpeg","-","-i", file, "-ar", "16000", "-ac", "1", out_folder/file_name], check=True)
```

Ensuite on met dans "urls.txt" les urls des videos que l'on veut downloader. 

```
urls = open("urls.txt", "r").readlines()
for url in urls:
   url = url.strip() #on enlève les espaces etc
   if not url:
        continue
    yt-dlp -f 139 -x (--audio-format wav) "https://url"
```

Finalement on peut garder le m4a qui est plus petit (20MB/heures d'audio) pour le stockage. Pour le traitement, on peut convertir en wav en utilisant par exemple `audiocraft`:

```
pip install audiocraft
from audiocraft.data.audio import audio_read
wav, .. = audio_read("file.m4a")
wav.numpy()

``
