import os
import gzip
import shutil

#Testing Loading
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# Program that unzips every single gz file in a folder and its subfolders
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
def unzipGz(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".gz"):
                gz_path = os.path.join(dirpath, filename)
                output_path = os.path.join(dirpath, filename[:-3])  # Remove '.gz' extension

                # Skip if file already exists
                if os.path.exists(output_path):
                    print(f"Skipped (already exists): {output_path}")
                    continue

                try:
                    with gzip.open(gz_path, 'rb') as f_in:
                        with open(output_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    print(f"Extracted: {gz_path} -> {output_path}")
                except Exception as e:
                    print(f"Error extracting {gz_path}: {e}")
        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)



if __name__ == "__main__":
    folder_path = input("Enter the path to the folder you want to unzip .gz files in: ").strip()
    if os.path.isdir(folder_path):
        unzipGz(folder_path)
    else:
        print("Invalid folder path. Please check and try again.")
