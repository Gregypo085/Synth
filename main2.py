import numpy as np  # Math library for array operations
import sounddevice as sd  # Audio library for playing and recording audio
from pynput.keyboard import Key, Listener  # Keyboard library for listening to keyboard events

# Install and import Pyo for more advanced audio processing if needed. 
# Pyo is designed for real-time synths or DAW style projects. Not something I need right now.
# https://github.com/Pyo/pyo

sample_rate = 44100 # Sample rate in Hz
amplitude = 0.3 # Amplitude of the sound


def main(): # Main function

    # Generate and play a sound
    mysound = sine_wave()
    sd.play(mysound, sample_rate)
    sd.wait()

# OLD Sine wave generator
def sine_wave(
        frequency: int = 440,
        duration: float = 1.0,
        amplitude: float = 0.3,
        sample_rate: int = 44100
        ) -> np.ndarray:
    
    # Calculate the number of samples
    n_samples = int(sample_rate * duration)

    # Create an array of time points
    time_points = np.linspace(0, duration, n_samples, False) # numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0, *, device=None). https://numpy.org/doc/stable/reference/generated/numpy.linspace.html#numpy-linspace

    # Create the sine wave
    sine = np.sin(2 * np.pi * frequency * time_points)

    # Apply the amplitude and return the tone
    sine *= amplitude
    return sine



# White noise generator
def white_noise(
        duration: float = 1.0, # Duration of the noise in seconds
        amplitude: float = 0.1, # Amplitude of the noise
        sample_rate: int = 44100 # Sample rate in Hz
        ) -> np.ndarray: 

    # Calculate the number of samples
    n_samples = int(duration * sample_rate)

    # Generate white noise
    noise = np.random.uniform(-1, 1, n_samples)

    # Scale the noise to the desired amplitude
    noise *= amplitude

    return noise



# Sine wave generator
def sine_wave_generator(frequency = 440, amplitude = 0.3, sample_rate = 44100):
    time_index = 0 # Current time index. Keeps track of how far along the wave is so it can continue smoothly from where it left off.
    omega = 2 * np.pi * frequency / sample_rate # Angular frequency

    def generator(chunk_size): # Generator function that generates a chunk of samples
        nonlocal time_index # Nonlocal keyword is used to modify a variable that is defined in the outer scope of the generator function.
        samples = amplitude * np.sin(
            omega * (np.arange(chunk_size) + time_index)) # Computes angular frequency normalization for sine progression in sine_wave_generator. Generates chunk of samples. 
        time_index += chunk_size # Update time index to keep track of where we are in the wave.
        return samples.astype(np.float32) # Returns the chunk of samples
    
    return generator
        
class NotePlayer: # Class to play a note for the active notes dictionary
    def __init__(self, frequency: float, amplitude: float = 0.3, sample_rate: int = 44100): # Initialize the note player
        self.generator_func = sine_wave_generator(frequency, amplitude, sample_rate) # Initialize the generator function
        
        self.sample_rate = sample_rate # Sample rate in Hz
        self.fade_samples = int(0.01 * sample_rate) # Fade samples in samples
        self.fade_index = 0 # Fade index
        self.releasing = False # Releasing flag
        
        self.stream = sd.OutputStream( # Initialize the stream
            samplerate=sample_rate, # Sample rate in Hz
            channels=1, # Number of channels
            dtype='float32', # Data type
            callback=self.audio_callback # Callback function
        )

    def audio_callback(self, outdata, frames, time, status): # Audio callback function
        chunk = self.generator_func(frames) # Generate chunk of samples

        if self.releasing: # If the note is releasing
            n = min(self.fade_samples - self.fade_index, frames) # Number of samples to fade
            fade = np.linspace(1, 0, n, endpoint=False) # Fade array defined by numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0, *, device=None). https://numpy.org/doc/stable/reference/generated/numpy.linspace.html#numpy-linspace
            chunk[:n] *= fade # Apply fade to the first n samples
            self.fade_index += n # Update fade index to keep track of where we are in the fade.
            if self.fade_index >= self.fade_samples: # If fade is complete
                chunk[n:] = 0 # Set remaining samples to 0
        outdata[:] = chunk.reshape(-1, 1) # Reshape the chunk of samples. [:] means [0:len(sequence):1], which selects every element from the start (index 0) to the end of the sequence. 

    def start(self): # Start the stream
        self.stream.start()

    def stop(self): # Stop the stream
        self.releasing = True # Set releasing flag to True
        self.fade_index = 0 # Reset fade index
        sd.sleep(int(1000 * (self.fade_samples / self.sample_rate)))
        self.stream.stop() # Stop the stream
        self.stream.close() # Close the stream
      
    

if __name__ == "__main__":
    main()
