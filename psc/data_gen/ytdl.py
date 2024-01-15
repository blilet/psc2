import multiprocessing as mp
from pathlib import Path
import time
import subprocess as sp
n_coeurs = mp.cpu_count()
def split_text_file(input_file, number_files):
    with open(input_file, 'r') as file:
        content = file.readlines()

    total_lines = len(content)
    ind = total_lines // number_files
    if ind ==0: num_files = total_lines%number_files
    else: num_files = number_files
    for i in range(num_files):
        output_file_name = f"urls_{i + 1}.txt"

        with open(output_file_name, 'w') as output_file:
            output_file.writelines([content[min(ind * k + i,total_lines-1)] for k in range(number_files)])
        print(f"Created {output_file_name}")
    return num_files
thr = split_text_file('urls.txt', n_coeurs)
def down(i):
    download_path = Path.home() / "Downloads/conferences"
    download_path.mkdir(exist_ok=True, parents=True)
    urls = open("urls_"+str(i)+".txt", "r").readlines()
    for url in urls:
       url = url.strip() #on enlève les espaces etc
       if not url:
            continue
       sp.run(['yt-dlp', '-f', '139', url], cwd=download_path, check=True)
    return 0
if __name__ == "__main__":
    processes = []
    start_time= time.time()
    for i in range(1,thr+1):
        process = mp.Process(target=down, args=(i,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    end_time= time.time()
    print(end_time-start_time)
    print("All downloading processes have finished")
