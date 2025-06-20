import numpy as np
import os
import soundfile

def set_snr(speech_split,noise_split,params,output_dir="tmp"):
    
    speech, sr = sf.read(speech_split)
    assert sr == 16000, "Obtained Speech has unexpected Sampling rate"
    
    noise, sr = sf.read(noise_split)
    assert sr == 16000, "Obtained Noise has unexpected Sampling rate"
    
    snr = np.random.uniform(params["snr_range"][0], params["snr_range"][1])
    
    noise_power = (noise ** 2).mean()
    speech_power = (speech ** 2).mean()
    
    noise_power_target = speech_power * 10 ** (-snr / 10)
    
    noise_scaling = (noise_power_target / noise_power) ** 0.5
    
    modified_noise = noise*noise_scaling
    
    modified_speech = speech + modified_noise
    
    modified_speech = modified_speech / np.max(np.abs(modified_speech))
	
	mixed_wav_path = os.path.join(output_dir,f"clean_noise_{snr}.wav")
	
	sf.write(mixed_wav_path, mixed, 16000)
	
	print("Done saving ", mixed_wav_path)

clean_file = "clean.wav"
noise_file = "noise.wav"

params = {"snr_range":[-10,10]}
output_dir = os.makedirs("snr_outputs",exist_ok=True)

set_snr(clean_file,noise_file,output_dir)