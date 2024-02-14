import resampy
import numpy as np 
import scipy
import pandas as pd 
import matplotlib.pyplot as plt
from pydub import AudioSegment
import librosa

def resample(audio_file, target_sr):
    x, sr_orig = librosa.load(audio_file, sr=None, mono=False)
    audio_data = resampy.resample(audio_data, sr_orig, target_sr)


def extract_feature(file_name, **kwargs):
    """
    Extract feature from audio file `file_name`
        Features supported:
            - MFCC (mfcc)
            - Chroma (chroma)
            - MEL Spectrogram Frequency (mel)
            - Contrast (contrast)
            - Tonnetz (tonnetz)
    """
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")

    # Load the audio file with pydub
    audio = AudioSegment.from_file(file_name)
    sample_rate = audio.frame_rate

    # Convert to NumPy array
    audio_data = np.array(audio.get_array_of_samples())
    if audio.channels == 2:  # Check if stereo and convert to mono
        audio_data = audio_data.reshape((-1, 2))
        audio_data = audio_data.mean(axis=1)
    audio_data = audio_data.astype(np.float32) / np.iinfo(audio_data.dtype).max  # Normalize

    # Feature extraction
    result = np.array([])
    if chroma or contrast or tonnetz:
        stft = np.abs(librosa.stft(audio_data))
    
    if mfcc:
        mfccs = np.mean(librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13).T, axis=0)
        result = np.hstack((result, mfccs))

    if chroma:
        chroma_feature = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        result = np.hstack((result, chroma_feature))

    if mel:
        mel_feature = np.mean(librosa.feature.melspectrogram(y=audio_data, sr=sample_rate).T, axis=0)
        result = np.hstack((result, mel_feature))

    if contrast:
        contrast_feature = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
        result = np.hstack((result, contrast_feature))

    if tonnetz:
        tonnetz_feature = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(audio_data), sr=sample_rate).T, axis=0)
        result = np.hstack((result, tonnetz_feature))

    return result


def preprocess_audio(speaker,audio_file):
    # Extract the same features as we did for training
    #audio = AudioSegment.from_mp3("/kaggle/working/" + audio_file[-4] + speaker + ".mp3")
    file_path = "/kaggle/working/" + audio_file[:-4] + speaker + ".mp3"
    features = extract_feature(file_path, mel=True)
    return features

def predict_gender(speaker,audio_file , model):
    # Preprocess the file
    features = preprocess_audio(speaker,audio_file)
    # Reshape features to match the input shape of the model
    features = np.reshape(features, (1, -1))
    # Make a prediction
    prediction = model.predict(features)[0]
    # Interpret the result
    if prediction <= 0.5:
        return "Female",prediction
    else:
        return "Male",prediction
