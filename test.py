import numpy as np  
import sounddevice as sd
from pynput.keyboard import Key, Listener
#from main import sine_wave_generator
from main import NotePlayer
import threading


# Install and import Pyo for more advanced audio processing. 
# Pyo is designed for real-time synths or DAW style projects. Not something I need right now.
# https://github.com/Pyo/pyo

# Need to implement Equal Temperament Formula

# Equal Temperament Formula
# f(n) = f(0) * 2^(n/12)

A4_POS = 49
A4_FREQ = 440.0
KEYS = 88

for key in range(1, KEYS + 1): # Generate a list of frequencies for each key
    n = key - A4_POS # Calculate the number of semitones from A4
    freq = A4_FREQ * (2 ** (n / 12)) # Calculate the frequency of the note
    note = round(freq, 2) # Round the frequency to 2 decimal places
    #print(f"Key {key} - {note}") # Print the note frequency

note_frequencies = {
    "a": 261.63, #C3
    "w": 277.18, #C#3
    "s": 293.66, #D3
    "e": 311.13, #D#3
    "d": 329.63, #E3
    "f": 349.23, #F3
    "t": 369.99, #F#3
    "g": 392.00, #G3
    "y": 415.30, #G#3
    "h": 440.00, #A3
    "u": 466.16, #A#3
    "j": 493.88, #B3
    "k": 523.25, #C4
    "o": 554.37, #C#4
    "l": 587.33, #D4
    "p": 622.25, #D#4
    ";": 659.25, #E4
    "'": 698.46, #F4
}

active_notes = {} # Dictionary to store active notes

def on_press(key): # Function to handle key press events
    try: # Try to get the character of the key pressed
        k = key.char # Get the character of the key pressed
        if k in note_frequencies and k not in active_notes: # If the key is in the dictionary and not already active
            print(f"Key {k} pressed") # Print the key pressed
            player = NotePlayer(note_frequencies[k]) # Create a new NotePlayer object
            player.start() # Start the player
            active_notes[k] = player # Add the player to the dictionary
    except AttributeError:
        pass # Non-character keys

def on_release(key): # Function to handle key release events
    try: # Try to get the character of the key released
        k = key.char # Get the character of the key released
        if k in active_notes: # If the key is in the dictionary
            print(f"Key {k} released") # Print the key released
            threading.Thread(target=active_notes[k].stop).start() # Stop the player in a separate thread https://docs.python.org/3/library/threading.html
            del active_notes[k] # Remove the player from the dictionary
    except AttributeError: # Non-character keys
        pass

with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
    

