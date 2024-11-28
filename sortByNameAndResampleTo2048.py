import os
import wave
import numpy as np
from scipy import signal
from shutil import copy2
import subprocess
from datetime import datetime
import subprocess

def resample_with_sox(input_file, output_file, target_samples=2048):
    sample_rate = 44100  # Sample rate in Hz
    target_duration_seconds = target_samples / sample_rate  # Calculate target duration in seconds

    try:
        # Get the original duration of the audio file
        result = subprocess.run(['soxi', '-D', input_file], capture_output=True, text=True, check=True)
        original_duration_seconds = float(result.stdout.strip())

        # Calculate the speed factor needed to achieve the target duration
        speed_factor = original_duration_seconds / target_duration_seconds

        subprocess.run([
            'sox',
            input_file,
            '-b', '16',       # 16-bit depth
            output_file,
            'remix', '1',     # Force mono
            'rate', str(sample_rate),  # Ensure sample rate is 44100 Hz
            'speed', str(speed_factor)  # Adjust speed to achieve target duration
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error resampling {input_file}: {str(e)}")
        
def sort_wav_files_by_filename(wav_files):
    def sort_key(file_tuple):
        filename = file_tuple[0]
        prefix = filename.split('_')[0]
        if prefix.isdigit() and len(prefix) == 1:
            prefix = '0' + prefix
        return int(prefix)
    
    return sorted(wav_files, key=sort_key)

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Retrieve all .wav files with their creation times
    wav_files = []
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.wav'):
            file_path = os.path.join(input_folder, filename)
            creation_time = os.path.getctime(file_path)
            wav_files.append((filename, creation_time))

    # Sort files by filename
    sorted_files = sort_wav_files_by_filename(wav_files)

    # Sort files by creation time ascending
    # sorted_files = sorted(wav_files, key=lambda x: x[1])

    # # Log the sorted order
    # log_file = os.path.join(os.path.dirname(output_folder), 'sorted_order.log')
    # with open(log_file, 'w') as log:
    #     log.write("Files sorted by creation date (ascending):\n")
    #     for filename, ctime in sorted_files:
    #         readable_time = datetime.fromtimestamp(ctime).strftime('%H:%M:%S:%f')
    #         log.write(f"{readable_time} - {filename}\n")

    # print(f"Sorted file order logged to {log_file}")

    # Process each file in sorted order
    for i, (filename, _) in enumerate(sorted_files, start=1):
        input_path = os.path.join(input_folder, filename)
        try:

            temp_filename = f"temp_{filename}"
            temp_path = os.path.join(output_folder, temp_filename)
            final_filename = f"{i}_{filename}"
            final_path = os.path.join(output_folder, final_filename)

            # Copy to temp file
            copy2(input_path, temp_path)

            # Resample and trim
            resample_with_sox(temp_path, final_path)

            # Remove temp file
            os.remove(temp_path)

            print(f"Processed and resampled {filename} -> {final_filename}")

        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    # Define input and output folders
    input_folder = "incoming/Sliced"  # Change this to your input folder path
    output_folder = "incoming/RN"      # Change this to your desired output folder path

    process_folder(input_folder, output_folder)