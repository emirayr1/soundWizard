# add music cent stuff and mathematical calculations for music theory
# different systems, scales, modes, contourpoıint, intervals, chords, chord progressions, voice leading, harmonic analysis, form analysis, rhythmic analysis, timbral analysis

class NOTE:
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, name, octave=4):
        self.name = name
        self.octave = octave
        # Find the index (0-11) for calculations
        if name not in self.NOTES:
            raise ValueError(f"Invalid note name: {name}")
        self.index = self.NOTES.index(name)

    def add_semitones(self, semitones):
        total_semitones = self.index + semitones
        new_index = total_semitones % 12
        octave_shift = total_semitones // 12
        new_octave = self.octave + octave_shift
        return NOTE(self.NOTES[new_index], new_octave)
    
class MODE:
    # Define standard interval patterns (semitones)
    PATTERNS = {
        'ionian':     [2, 2, 1, 2, 2, 2, 1], # Major
        'dorian':     [2, 1, 2, 2, 2, 1, 2],
        'phrygian':   [1, 2, 2, 2, 1, 2, 2],
        'lydian':     [2, 2, 2, 1, 2, 2, 1],
        'mixolydian': [2, 2, 1, 2, 2, 1, 2],
        'aeolian':    [2, 1, 2, 2, 1, 2, 2], # Minor
        'locrian':    [1, 2, 2, 1, 2, 2, 2]
    }

    def __init__(self, root_name, mode_type):
        self.root = NOTE(root_name)
        self.mode_type = mode_type.lower()
        if self.mode_type not in self.PATTERNS:
             raise ValueError(f"Unknown mode: {mode_type}")
        self.intervals = self.PATTERNS[self.mode_type]
        
    def generate_scale(self, showName:bool = True):
        scale = [self.root.name] if showName else [self.root]
        current_note = self.root
        for interval in self.intervals:
            next_note = current_note.add_semitones(interval)
            scale.append(next_note.name if showName else next_note)
            current_note = next_note
            
        return scale
        
ionian = MODE('D', 'dorian')
print(ionian.generate_scale())