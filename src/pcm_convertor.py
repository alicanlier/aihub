'''from scipy.io import wavfile

# Load PCM file
sample_rate, data = wavfile.read('f1_1_26_210929_0005230.pcm')

# Resample to 16kHz
new_sample_rate = 16000
resampled_data = scipy.signal.resample(data, int(len(data) * new_sample_rate / sample_rate))

# Write WAV file
wavfile.write('f1_1_26_210929_0005230.wav', new_sample_rate, resampled_data)'''

'''
import librosa

filename = 'data/f1_1_26_210929_0005230.pcm'
data, sample_rate = librosa.load(filename, sr=16000, mono=True, dtype='float32')

output_filename = 'wavoutput/f1_1_26_210929_0005230.wav'
librosa.output.write_wav(output_filename, data, sample_rate)
'''

import subprocess

# Specify the paths to the input and output files
input_file = 'f1_1_26_210929_0005230.pcm'
output_file = 'f1_1_26_210929_0005230.wav'

# Specify the ffmpeg command and arguments
command = ['ffmpeg', '-f', 's16le', '-ar', '16k', '-ac', '1', '-i', input_file, '-y', output_file]

# Run the command using subprocess
# subprocess.run(command, check=True)

try:
    subprocess.run(command, check=True)
    subprocess.check_output(command, stderr=subprocess.STDOUT)
    print('Conversion completed successfully.')
except subprocess.CalledProcessError as e:
    print('Error during conversion:', e.output.decode())


