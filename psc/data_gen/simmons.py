#pip install yt-dlp
#pip install ffmpeg
#pip install ffmpeg-python
#pip install gender-guesser
#pip install gender
import gender_guesser.detector as gender_guesser
import ffmpeg
import json
import os
from pathlib import Path
import numpy as np
import subprocess as sp
keywords = ["what", "why", "when", "where", "name", "is", "how", "do", "does", "which", "are", "could", "would",  "should", "has", "have", "whom", "whose", "?"]
def get_gender(name): #don't @ me with no heteronormative bullshit
    
    d = gender_guesser.Detector(case_sensitive=False)
    gender_prediction = d.get_gender(name)
    
    if gender_prediction == "unknown":
        return "U"
    elif gender_prediction == 'male':
        return "M"
    else:
        return "F"
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
def strToTime(str):
    st =  str.split(':')
    return int(st[0])*3600 + int(st[1])*60 + int(float(st[2]))
def lenTirade(L):
    try:
        start = strToTime(L[0])
        end = strToTime(L[2])
        return end - start
    except:
        return 0
def lenSpeaker(L):
    s = 0
    for x in L:
        s+= lenTirade(x)
    return s
def mainSpeaker(d):
    speaker= 'None'
    s = 0
    for key in d.keys():
        len = lenSpeaker(d[key])
        if len >s:
            s= len
            speaker = key
    return speaker
def isQuestion(str):
    str = str.lower()
    for x in keywords:
        if x in str: return True
    return False
def mixte(str):
    if str == '0': return []
    else: return 0
def vttToDict(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    current_speaker = 'None'
    previous_speaker = 'None'
    lines = lines[4:]
    timestamps=[]
    tirades = {}
    for line in lines:
        split = line.split()
        line = line.strip()
        if '-->' in line:
            timestamps.append(line)
        elif ':' in line:
            if split[0] == split[0].upper() and not has_numbers(split[0]):
                current_speaker = split[0].replace(':','')
                begin = timestamps[-1].split('-->')[0]
                try:
                    tirades[current_speaker].append([begin, line])
                except:
                    tirades[current_speaker]= [[begin, line]]
                if previous_speaker != 'None':
                        tirades[previous_speaker][-1].append(begin)
                previous_speaker = current_speaker
        else:
            try:
                tirades[current_speaker][-1][1] =  tirades[current_speaker][-1][1] + " - " + line
            except:
                pass
    try:
        tirades[current_speaker][-1].append(timestamps[-1].split('-->')[1].strip())
        tirades['END_STAMP'] = timestamps[-1].split('-->')[1].strip()
    except:
        pass
    return tirades
def endOfSpeech(L,prox):
    R = []
    for x in L:
        if 'APPLAUSE' in x[1]:
            R.append(x)
    try:
        end = strToTime(R[-1][2])
    except:
        end = prox
    try:
        if prox - end <10:
            end = strToTime(R[-2][2])
    except:
        pass
    return end
def interruptions_list(L,end):
    R = []
    for x in L:
        try:
                if strToTime(x[2])< end: R.append([strToTime(x[0]), strToTime(x[2]), "U", "N"])
        except:
            pass
    return R
download_path = Path.home() / "Downloads/cache_simmons"
download_path.mkdir(exist_ok=True, parents=True)
urls = open("urls_SIMMONS.txt", "r").readlines()
for url in urls:
    url = url.strip() #on enlève les espaces etc
    if not url:
        continue
    try:
        sp.run(['yt-dlp', '-f', '139', '--output' ,"%(id)s.m4a", url], cwd=download_path, check=True)
    except:
        pass
    try:
        sp.run(['yt-dlp', '--skip-download', '--write-description', '--output' ,"%(id)s", url], cwd=download_path, check=True)
    except:
        pass
    try:
        sp.run(['yt-dlp', '--write-sub' ,'--skip-download', '--output' ,"%(id)s",url], cwd=download_path, check=True)
    except:
        pass
in_folder = Path.home()/"Downloads/cache_simmons"
out_folder= Path.home()/"Downloads/wav_simmons"
out_folder.mkdir(exist_ok=True, parents=True)
for file in in_folder.iterdir():
    if file.suffix != ".m4a":
        continue
    sp.run(["ffmpeg", "-y", "-i", file, "-ar", "16000", "-ac", "1", out_folder/(file.stem + ".wav")], check=True)
out_J = out_json = in_folder/"json"
out_J.mkdir(exist_ok=True, parents=True)
for file in in_folder.iterdir():
    if file.suffix != ".vtt":
        continue
    uuid = file.stem.split('.')[0]
    path = str(out_folder) + '/'+uuid + '.wav'
    dict = vttToDict(file)
    speaker = mainSpeaker(dict)
    start = strToTime(dict[speaker][0][0])
    end = endOfSpeech(dict[speaker],strToTime(dict['END_STAMP']))
    path_description = str(in_folder)  + '/'+uuid + '.description'
    uuid_json = uuid+ '.json'
    out_json = in_folder/"json"/uuid_json
    try:
        with open(path_description, 'r', encoding='utf-8') as file:
            line = file.readline()
    except FileNotFoundError:
        continue
    if 'Auth' in line:
        line = line.split(' ')[1]
    else:
        line = line.split(' ')[0]
    genderS = get_gender(line)
    if 'AUDIENCE' in dict.keys():
        interruptions = interruptions_list(dict['AUDIENCE'],end)
    else:
        try:
            interruptions = interruptions_list(dict['STUDENT'],end)
        except:
            continue
    to_JSON = {'path': (path, uuid), 'gender':genderS, 'start':int(start), 'end':end, 'num_interruptions':len(interruptions), 'interruptions':interruptions}
    json_d = json.dumps(to_JSON, indent = 2)
    with open(out_json, 'w') as f:
            f.write(json_d)
python_objects = []
for json_file in out_J.iterdir():
        try:
            with open(json_file, "r") as f:
                python_objects.append(json.load(f))
            # Dump all the Python objects into a single JSON file.
        except:
            pass
with open('database_SIMMONS.json', "w") as f:
    json.dump(python_objects, f, indent=4)
print('Stored in where ipynb file is.')
