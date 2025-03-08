# lib_midi_writer-py
Lightweight Python module to create MIDI files.
=======
# README: MidiWriter (Python)

## Overview
- `MidiWriter` is a lightweight Python class designed to generate and save MIDI files.
- It provides an easy-to-use interface for adding tracks, setting channels, specifying tempo, and inserting MIDI note events.

## Features
- Supports multiple tracks
- Customizable tempo (BPM)
- Ability to specify MIDI channels and programs
- Adds note events with configurable pitch, velocity, and duration
- Saves MIDI data to a file
- Uses standard 480 ticks per quarter note (modifiable)

## Installation
Simply import the `MidiWriter` class with your Python project:
`from midi_writer import MidiWriter`

## Usage"
### 1. Creating a MIDI file:
```python
# Simple test to write 4 quarter notes across 4 staves:

from midi_writer import MidiWriter

def main():
    ''' MidiWriter public methods, params, and returns:
    @publicmethod addTrack() -> int
    @publicmethod setChannel(int channel = 0, int program = 0) -> None
    @publicmethod addBPM(int track = 0, int start = 0, int bpm = 120) -> None
    @publicmethod addNote(
        int track = 0,
        int channel = 0, 
        int start = 0,
        int duration = 480,
        int pitch = 60,
        int velocity = 120
      ) -> None
    @publicmethod save(str output_filename) -> None
    '''

    # Create instance of MidiWriter class
    myMidi = MidiWriter()

    # Create tempo event
    myMidi.addBPM(start=0, bpm=120)

    # Specify track-channel mapping (alternate channels)
    myMidi.setChannel(channel=0, program=0)  # Acoustic Grand Piano
    myMidi.setChannel(channel=1, program=0)  # Acoustic Grand Piano

    # Define TICKS_PER_QUARTER
    TPQ = 480

    # Each note goes into a separate track
    # addNote params: track, channel, start, duration, pitch, velocity
    # alternate channels so Musescore will not combine staves:
    myMidi.addNote(track=0, channel=0, start=0 * TPQ, duration=1 * TPQ, pitch=60, velocity=120)
    myMidi.addNote(track=1, channel=1, start=1 * TPQ, duration=1 * TPQ, pitch=62, velocity=120)
    myMidi.addNote(track=2, channel=0, start=2 * TPQ, duration=1 * TPQ, pitch=64, velocity=120)
    myMidi.addNote(track=3, channel=1, start=3 * TPQ, duration=1 * TPQ, pitch=65, velocity=120)

    # Write out MIDI object
    output_filename: str = "test_multiple_tracks.mid"
    myMidi.save(output_filename)
    print(f"Successfully created {output_filename}")

if __name__ == "__main__":
    main()

```

## API Reference

### `addTrack()`
Adds a new track to the MIDI file.
- **Returns**: The index of the newly created track.

### `setChannel(int channel = 0, int program = 0)`
Assigns a program (instrument) to a specific MIDI channel.
- **Parameters**:
  - `channel`: MIDI channel number (0-15).
  - `program`: Program number (0-127) representing an instrument.

### `addBPM(int track = 0, int start = 0, int bpm = 120)`
Adds a tempo change event to a track.
- **Parameters**:
  - `track`: Track index.
  - `start`: Tick position where the tempo change should be inserted.
  - `bpm`: Beats per minute.

### `addNote(int track, int channel, int start, int duration, int pitch, int velocity)`
Inserts a note into a specified track.
- **Parameters**:
  - `track`: Track index.
  - `channel`: MIDI channel (0-15).
  - `start`: Start time in ticks.
  - `duration`: Note duration in ticks.
  - `pitch`: MIDI note number (0-127, where 60 is Middle C).
  - `velocity`: Note volume (0-127).

### `save(const std::string &output_filename)`
Writes the MIDI data to a file.
- **Parameters**:
  - `output_filename`: Name of the output MIDI file.

## Notes
1. Create an instance of the MidiWriter class: `myMidi = MidiWriter()`
- MIDI events are defined in terms of an integer number of ticks per quarter note. Default is 480 ticks per quarter.
- You can change the default ticks per quarter upon instantiating the MidiWriter class.

2. Define channel-to-program mapping (where program index refers to MIDI instrument).

3. Add tempo events to the MidiWriter class using `myMidi.addBPM()`.

4. Add notes to the MidiWriter class using `myMidi.addNote(int track, int channel, int start, int duration, int pitch, int velocity)`.
- Tracks are automatically created if they do not exist. For example, adding a note to Track 4 will automatically create tracks up to track 4 to accommodate.

5. Save and write your MIDI object using `myMidi.save()`.
- All tracks and events must be added before calling `save()`.
- The default `TICKS_PER_QUARTER` is 480, aligning with standard MIDI resolution.

6. An output/ directory will automatically be created if it doesn't exist. Output files will be created there.

## License
This project is open-source and available under the MIT License.

## Contributing
- I designed this MidiWriter to be more lightweight than other APIs. There are many features I wish to add going forward.
- Feel free to offer suggestions and feedback!
- If you wish to contribute, please fork the repo and submit a pull request, and I can consider any changes.
