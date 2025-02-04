#!/usr/bin/python3

"""
Module:   midi_test.py
Author:   Logan Richey
Detail:   Simple MIDI file writing library.
Date:     Feb 3, 2025

This module contains a MidiWriter class with methods to create a MIDI file.
"""

import struct

class MidiWriter:
    """
    @brief  Contains MIDI file writing functions using 480 ticks per quarter note.
    
    All time values (start and duration) are expressed in integer MIDI ticks.
    For example:
      - 480 ticks = quarter note
      - 240 ticks = eighth note
      - 120 ticks = sixteenth note
      - 60 ticks  = thirty-second note, etc.
    
    @publicmethods:
        addTrack() -> int
        setChannel(int channel = 0, int program = 0)
        addBPM(int track = 0, int start = 0, int bpm = 120)
        addNote(int track = 0, int channel = 0, int start = 0, int duration = 480,
                int pitch = 60, int velocity = 120)
        save(str output_filename)
    """
    
    class Track:
        """
        @brief  Represents a single MIDI track.
        
        The Track class stores a list of MIDI events. Each event is a tuple of
        (tick, event_bytes), where 'tick' is the absolute tick time and 'event_bytes'
        is the corresponding MIDI message.
        """
        
        def __init__(self):
            # Each event is a tuple: (tick, event_bytes)
            self.events = []
        
        def add_event(self, tick, event_bytes):
            """
            @brief  Add an event to the track.
            
            @param  tick (int): The absolute tick time at which the event occurs.
            @param  event_bytes (bytes): The MIDI event message.
            """
            self.events.append((tick, event_bytes))
        
        def sort_events(self):
            """
            @brief  Sort events by their tick time.
            
            This method must be called before writing the MIDI file to ensure that events
            are in chronological order.
            """
            self.events.sort(key=lambda ev: ev[0])
    
    def __init__(self):
        """
        @brief  Constructor.
        
        Uses the MIDI standard resolution:
            TICKS_PER_QUARTER = 480.
        """
        self.ticks_per_quarter = 480
        self.tracks = []           # List of Track objects.
        self.channel_program = {}  # Mapping: channel id -> program number.
    
    def encode_var_len(self, value):
        """
        @brief  Encode an integer as a MIDI variable-length quantity.
        
        @param  value (int): The value to encode.
        @return (bytes): The value encoded in MIDI variable-length format.
        
        The MIDI specification requires delta-times to be stored in a variable-length
        format. This function converts an integer into that format.
        """
        buffer = value & 0x7F
        value >>= 7  # shift value right by 7 bits
        while value > 0:
            # Prepend the next 7-bit chunk with the continuation bit set.
            buffer = (buffer << 8) | ((value & 0x7F) | 0x80)
            value >>= 7
        bytes_out = []
        while True:
            # Extract the lowest byte.
            bytes_out.append(buffer & 0xFF)
            if buffer & 0x80:
                buffer >>= 8
            else:
                break
        return bytes(bytes_out)

    def addTrack(self):
        """
        @brief  Append a new track to the MIDI file.
        
        @return (int): The index of the new track.
        """
        track = MidiWriter.Track()
        self.tracks.append(track)
        return len(self.tracks) - 1

    def _get_track(self, track_idx):
        """
        @brief  Retrieve a track by index, auto-adding tracks if necessary.
        
        @param  track_idx (int): The index of the track.
        @return (Track): The Track object.
        """
        while track_idx >= len(self.tracks):
            self.addTrack()
        return self.tracks[track_idx]
    
    def setChannel(self, channel=0, program=0):
        """
        @brief  Set the instrument for a given channel via a program change.
        
        @param  channel (int): MIDI channel number (>= 0).
        @param  program (int): MIDI program number (0 to 127).
        
        @usage
            myMidi.setChannel(channel=0, program=13)  
            # Sets channel 0 to program 13 (e.g., xylophone).
        """
        self.channel_program[channel] = program
        
        # Add a program change event at tick 0 in track 0.
        track0 = self._get_track(0)
        # MIDI program change event: status byte = 0xC0 | channel, then the program number.
        event_bytes = bytes([0xC0 | (channel & 0x0F), program & 0x7F])
        track0.add_event(0, event_bytes)
    
    def addBPM(self, track=0, start=0, bpm=120):
        """
        @brief  Insert a tempo (BPM) change event at the specified tick.
        
        @param  track (int): Track index where the tempo event is placed. (Default = 0)
        @param  start (int): Start time in MIDI ticks.
        @param  bpm (int): Beats per minute (> 0).
        
        @usage
            # Change tempo at 4 quarter notes (4*480 ticks):
            myMidi.addBPM(track=0, start=4 * 480, bpm=180)
        """
        try:
            if track < 0:
                raise ValueError("Track cannot be less than zero.")
            if start < 0:
                raise ValueError("Start cannot be less than zero.")
            if bpm <= 0:
                raise ValueError("BPM must be greater than zero.")
        except Exception as e:
            print("[W] Could not add BPM. Error = {}".format(e))
            print("track={}, start={}, bpm={}".format(track, start, bpm))
            return

        tick = int(start) # start is already in ticks
        # Calculate tempo in microseconds per quarter note (μs/qn).
        # Formula: 60,000,000 / BPM.
        tempo = int(60000000 / bpm)
        # Convert tempo to a 3-byte big-endian value.
        tempo_bytes = tempo.to_bytes(3, byteorder="big")
        # Construct the tempo meta event: FF 51 03 <tempo_bytes>
        meta_event = bytes([0xFF, 0x51, 0x03]) + tempo_bytes
        
        trk = self._get_track(track)
        trk.add_event(tick, meta_event)
    
    def addNote(self, track=0, channel=0, start=0, duration=480, pitch=60, velocity=127):
        """
        @brief  Add a MIDI note event to a track.
        
        @param  track (int)    : Track index (>= 0). Essentially, a musical staff.
        @param  channel (int)  : MIDI channel (0 to 15). (Channel 9 is typically reserved for drums.)
        @param  start (int)    : Start time in MIDI ticks.
        @param  duration (int) : Duration in MIDI ticks (> 0).
        @param  pitch (int)    : MIDI note number (0 to 127). (60 = Middle C)
        @param  velocity (int) : Note velocity (0 to 127); determines volume.
        
        @usage
            # Four quarter notes:
            TPQ = 480  // ticks per quarter note
            myMidi.addNote(track=0, channel=0, start=0 * TPQ, duration=TPQ, pitch=60, velocity=120)
            myMidi.addNote(track=0, channel=0, start=1 * TPQ, duration=TPQ, pitch=62, velocity=120)
            myMidi.addNote(track=0, channel=0, start=2 * TPQ, duration=TPQ, pitch=64, velocity=120)
            myMidi.addNote(track=0, channel=0, start=3 * TPQ, duration=TPQ, pitch=65, velocity=120)
        """
        try:
            if track < 0:
                raise ValueError("[E] Track value '{}' cannot be negative. Expected integer >= 0.".format(track))
            if channel < 0:
                raise ValueError("[E] Channel value '{}' cannot be negative. Expected integer >= 0.".format(channel))
            if start < 0:
                raise ValueError("[E] Start value '{}' cannot be negative. Expected integer >= 0.".format(start))
            if duration <= 0:
                raise ValueError("[E] Duration value '{}' must be > 0.".format(duration))
            if not (0 <= velocity <= 127):
                raise ValueError("[E] Velocity value '{}' must be in range [0, 127].".format(velocity))
        except Exception as e:
            print("[W] Could not add note! Error: {}".format(e))
            print("track={}, channel={}, start={}, duration={}, pitch={}, velocity={}".format(
                track, channel, start, duration, pitch, velocity
            ))
            return
        
        start_tick = int(start)
        end_tick = int(start + duration)
        
        trk = self._get_track(track)
        
        # Note on event: status byte 0x90 + channel, note number, velocity.
        note_on = bytes([0x90 | (channel & 0x0F), pitch & 0x7F, velocity & 0x7F])
        trk.add_event(start_tick, note_on)
        
        # Note off event: status byte 0x80 + channel, note number, velocity 0.
        note_off = bytes([0x80 | (channel & 0x0F), pitch & 0x7F, 0])
        trk.add_event(end_tick, note_off)
    
    def save(self, output_filename):
        """
        @brief  Write the MIDI file to disk.
        
        @param  output_filename (str): The name of the output file (e.g., "output.mid").
        
        This method builds the MIDI header and all track chunks, then writes the
        complete MIDI file to disk.
        """
        # Sort events in each track by tick before writing.
        for trk in self.tracks:
            trk.sort_events()
        
        # Prepare the header chunk.
        num_tracks = len(self.tracks)
        header_chunk_type = b"MThd"
        header_length = 6
        # MIDI format: use 1 if more than one track, else 0.
        midi_format = 1 if num_tracks > 1 else 0
        # The time division is the number of ticks per quarter note.
        header_data = struct.pack(">hhh", midi_format, num_tracks, self.ticks_per_quarter)
        header_chunk = header_chunk_type + struct.pack(">I", header_length) + header_data
        
        # Build track chunks.
        track_chunks = b""
        for trk in self.tracks:
            track_data = bytearray()
            prev_tick = 0
            for tick, event in trk.events:
                delta_ticks = tick - prev_tick
                prev_tick = tick
                track_data += self.encode_var_len(delta_ticks)
                track_data += event
            
            # Append the end-of-track meta event (0xFF 0x2F 0x00)
            track_data += self.encode_var_len(0)
            track_data += bytes([0xFF, 0x2F, 0x00])
            
            # Prepend the track header.
            track_chunk = b"MTrk" + struct.pack(">I", len(track_data)) + track_data
            track_chunks += track_chunk
        
        # Write the complete MIDI file.
        full_data = header_chunk + track_chunks
        with open(output_filename, "wb") as f:
            f.write(full_data)

################################################################################
# Test functions and main() for demonstration purposes.
################################################################################

def main():
    TPQ = 480  # TICKS_PER_QUARTER
    
    def test_simple():
        """
        @brief  Generate a simple quarter-note scale MIDI file.
        """
        
        myMidi = MidiWriter() # Create a new MIDI object.
        myMidi.addBPM(track=0, start=0, bpm=120) # Set initial tempo.
        myMidi.setChannel(channel=0, program=0) # Set channel 0 to Acoustic Grand Piano.
        
        # Define a scale (C major scale)
        notes = [60, 62, 64, 65, 67, 69, 71, 72]
        for beat, note in enumerate(notes):
            myMidi.addNote(
                track=0,
                channel=0,
                start=beat * TPQ,
                duration=TPQ,
                pitch=note,
                velocity=120
            )
        
        output = "test_scale.mid"
        myMidi.save(output)
        print("Successfully created \"{}\".".format(output))
    
    def test_6lets():
        """
        @brief  Generate a MIDI file with sextuplet (6-tuplet) notes.
        
        Note: Some programs (e.g. MuseScore) may have difficulty automatically 
        quantizing tuplets. The MIDI data is correct, but you may need to adjust 
        the quantization and tuplet settings in your score editor.
        """
        myMidi = MidiWriter() # Create a new MIDI object.
        myMidi.addBPM(track=0, start=0, bpm=120) # Set initial tempo.
        myMidi.setChannel(channel=0, program=0) # Set channel 0 to Acoustic Grand Piano.
        
        # SIXLET_TICKS: Duration of one sextuplet note within a quarter note.
        SIXLET_TICKS = TPQ / 6  
        for beat in range(24):
            myMidi.addNote(
                track=0,
                channel=0,
                start=int(beat * SIXLET_TICKS),
                duration=int(SIXLET_TICKS),
                pitch=60 + beat,
                velocity=100
            )
        
        output = "test_midi_writer_sextuplets.mid"
        myMidi.save(output)
        print("Successfully created \"{}\".".format(output))
    
    print("*" * 80)
    test_simple()
    test_6lets()
    print("*" * 80)
    print("Successfully ran all tests in this file!")

if __name__ == "__main__":
    main()

