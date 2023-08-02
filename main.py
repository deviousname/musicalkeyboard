import mido  # For handling MIDI (Musical Instrument Digital Interface) messages
import keyboard  # For detecting key presses and releases
import threading  # For executing functions concurrently

class MidiKeyMapper:
    """Map keyboard keys to MIDI notes."""
    
    def __init__(self):
        """
        Initialize the MIDI output port, define key-note mapping and initialize current notes.
        """
        
        self.outport = mido.open_output()  # Opens a MIDI output port

        # Define mapping of keyboard keys to MIDI note numbers
        self.key_to_note = {
            'a': 60, 's': 62, 'd': 64, 'f': 65, 'g': 67,
            'h': 69, 'j': 71, 'k': 72, 'l': 74,
            'z': 48, 'x': 50, 'c': 52, 'v': 53, 'b': 55,
            'n': 57, 'm': 59, 'q': 72, 'w': 74, 'e': 76,
            'r': 77, 't': 79, 'y': 81, 'u': 83, 'i': 84,
            'o': 86, 'p': 88
        }

        self.current_notes = {}  # Store currently playing notes

    def note_on(self, note):
        """
        Send a MIDI 'note_on' message for the specified note if it's not currently playing.
        """
        if note not in self.current_notes:
            note_on = mido.Message('note_on', note=note)
            self.outport.send(note_on)
            self.current_notes[note] = True

    def note_off(self, note):
        """
        Send a MIDI 'note_off' message for the specified note if it's currently playing.
        """
        if note in self.current_notes:
            note_off = mido.Message('note_off', note=note)
            self.outport.send(note_off)
            del self.current_notes[note]

    def run(self):
        """
        Listen for key presses and releases, starting note_on and note_off in separate threads respectively.
        """
        for key, note in self.key_to_note.items():
            keyboard.on_press_key(key, lambda e, note=note: threading.Thread(target=self.note_on, args=(note,)).start())
            keyboard.on_release_key(key, lambda e, note=note: threading.Thread(target=self.note_off, args=(note,)).start())

        keyboard.wait()  # Block program execution until a keyboard event occurs

if __name__ == '__main__':
    midi_key_mapper = MidiKeyMapper()  # Instantiate the MidiKeyMapper
    midi_key_mapper.run()  # Start listening for keyboard events
