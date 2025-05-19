import kaldi
import pyaudio

# Load the model and feature extraction pipeline (same as before)
model_dir = "C:/Users/systran/Downloads/0013_librispeech_v1_chain/exp/chain_cleaned/tdnn_1d_sp"
# C:\Users\systran\Downloads\0013_librispeech_v1_chain\exp\chain_cleaned\tdnn_1d_sp
model = kaldi.chain.SupervisedChainModel.read(model_dir)
feat_pipeline = kaldi.chain.FeatureExtractor(model.dir + "/lda.mat") #'final.mdl' or 'lda.mat'

# Create the decoder (same as before)
decoder_opts = kaldi.chain.DecodableOptions()
decoder_opts.acoustic_scale = 1.0
decoder_opts.frame_subsampling_factor = model.info().frame_subsampling_factor
decodable_opts = kaldi.chain.ChainTrainingOptions()
decodable_opts.apply(model.chain_opts)
decodable_opts.frame_subsampling_factor = model.info().frame_subsampling_factor
decoder = kaldi.chain.ChainDecoder(model.am_nnet, model.den_fst, decoder_opts)

# Set up the microphone input
audio_interface = pyaudio.PyAudio()
audio_stream = audio_interface.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=4096
)

# Process the microphone input
while True:
    audio_data = audio_stream.read(4096) # read a chunk of audio data from the microphone
    if len(audio_data) == 0: break # stop if there is no more audio data
    audio_vector = kaldi.matrix.Vector(kaldi.subprocess([f"echo '{audio_data}' | sox -t wav - -t raw - rate 16000 |"].encode(), stdout=kaldi.subprocess.PIPE).communicate()[0])
    features = kaldi.matrix.Matrix()
    feat_pipeline.accept_waveform(16000, audio_vector)
    feat_pipeline.input_finished()
    feat_pipeline.get_feats(features)
    decoder.decode(features)
    best_path = decoder.get_best_path()
    transcription = kaldi.chain.ChainSupervision.get_linear_symbol_sequence(best_path)
    print(transcription)
