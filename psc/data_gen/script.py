from datasets import load_dataset
dataset = load_dataset('librispeech_asr', split='validation.clean') ## à changer validation.clean -> train.clean
import multiprocessing as mp
import numpy as np
import numpy.random as rnd
import os
import random as rand
import soundfile as sf
import time
from pathlib import Path
import subprocess as sp
bande_organise = {}
for x in dataset:
    if x['speaker_id'] not in bande_organise.keys():
        bande_organise[x['speaker_id']] = [x['audio']]
    else:
        bande_organise[x['speaker_id']].append(x['audio'])
L = list(bande_organise.keys())
m = min([len(bande_organise[key]) for key in bande_organise.keys()]) ## à changer
l = len(L)
N = 10000
n_coeurs = mp.cpu_count()
processes = N/n_coeurs
max_interruptions = 5
def mergerAux():
    speaker_1 = int(rnd.uniform(0,l))
    speaker_2 = int(rnd.uniform(0,l))
    if (speaker_1 == speaker_2):
        if speaker_1 == 0: speaker_2 = int(rnd.uniform(1,l))
        else: speaker_2 = int(rnd.uniform(0,speaker_1))
    N_interruptions = int(rnd.uniform(1,max_interruptions))
    interruptions = rand.sample(range(m), N_interruptions)
    L_aud = []
    path = str(speaker_1) +"-"+ str(speaker_2) + "_"
    for k in range(m):
        if k not in interruptions:
            piste = bande_organise[L[speaker_1]][k]
            audio_data= piste['array']
            if (int(piste['sampling_rate']) != 16000):
                audio_data =  sf.resample(audio_data, 16000)
            L_aud.append(audio_data)
            path = path + "0"
        else:
            piste = bande_organise[L[speaker_2]][k]
            audio_data= piste['array']
            if (int(piste['sampling_rate']) != 16000):
                audio_data =  sf.resample(audio_data, 16000)
            L_aud.append(audio_data)
            path = path +"1"
    merged_audio = np.concatenate(L_aud, axis=0)
    sf.write(path + ".wav", merged_audio, 16000)
    return 0
def merger(arbs):
    for k in range(int(processes)):
        mergerAux()
    return 0
if __name__ == "__main__":
    processes = []
    start_time= time.time()
    for i in range(n_coeurs):
        process = mp.Process(target=merger, args=(i,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    end_time= time.time()
    print(end_time-start_time)
    print("All merging processes have finished")
    
#from concurrent.features
#import ProcessPoolExecutor
#def process_file():
#with ProcessPoolExecutor(multiprocessing.cpu_count()) as pool
#pendings =[]
#for file in files:
#    pending = pool.submit(proces_file, file "args")
#    pendings.append(pending)
#result = [p.result for p in pendings]
#pickle
