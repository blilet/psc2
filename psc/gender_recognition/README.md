---

## Data Overview

### Source
Our project utilizes the [Mozilla Common Voice dataset](https://www.kaggle.com/datasets/mozillaorg/common-voice), a comprehensive corpus of speech data. This dataset is collected through the [Common Voice website](http://voice.mozilla.org/) and comprises a variety of sources, including user-submitted blog posts, historical books, movies, and other public speech corpora. Its primary aim is to facilitate the development and evaluation of Automatic Speech Recognition (ASR) systems.

### Dataset Version
For this project, we are working with a specific 13GB version of the dataset, which can be downloaded [here](https://www.kaggle.com/datasets/mozillaorg/common-voice).

## Data Preparation and Balancing

### Subset Selection
We focus on the “cv-train-other” subset, accompanied by the “cv-train-other.csv” file. This CSV file includes details for each audio recording, such as filename, text, up_votes, down_votes, age, gender, and accent. Our analysis primarily targets audio files with specified gender information.

### Data Cleaning and Balancing Steps
To ensure data quality and balance, we perform the following steps:
- Exclude audio files lacking gender information or labeled with 'other' as gender.
- Remove any silent audio files.
- Achieve an equal representation of male and female voices.
- Store the refined dataset in a new CSV file, “Balanced-data.csv,” which will list the paths of the remaining audio files along with their corresponding gender.

### Processing Notebook
All the above modifications are executed in the “Balancing.ipynb” notebook. This notebook also includes all necessary installation steps.

### Temporary Note
**Important:** For the proper execution of the “Balancing.ipynb” notebook, ensure that the dataset is downloaded as a folder named "archive" and placed on the desktop. Future updates to the code will aim to enhance its flexibility regarding data location.

---

