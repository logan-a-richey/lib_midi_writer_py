#!/usr/bin/python3
"""
Module:   midi_test.py
Author:   Logan Richey
Detail:   Further testing for MidiWriter.
Date:     Feb 3, 2025

This module demonstrates example usage of the MidiWriter library by generating
various MIDI files including simple scales, chords, multiple tracks, and drum patterns.
"""

from midi_writer import MidiWriter

class MidiTest:
    """
    @brief  Some example usage of this custom MidiWriter library.
    """
    
    # Constants
    TICKS_PER_QUARTER: int = 480
    DRUM_CHANNEL: int = 9 # MIDI channel for drums (10th channel, indexed from 0)
    DEFAULT_BPM: int = 120
    DEFAULT_VELOCITY: int = 120
    DEFAULT_DRUM_PITCH: int = 32 # Default pitch for metronome click

    # Drum Kit Definition (MIDI note numbers)
    DRUMS = {
        "kick_drum": 35,
        "snare_drum_rim": 37,
        "snare_drum": 38,
        "cymbal_hihat_closed": 42,
        "cymbal_hihat_open": 46,
        "cymbal_crash1": 49,
        "cymbal_crash2": 57,
        "cymbal_china": 52,
        "cymbal_ride": 51,
        "cymbal_ride_bell": 53,
        "cymbal_splash": 55,
        "tom1": 41,
        "tom2": 43,
        "tom3": 45,
        "tom4": 47,
        "tom5": 50,
        "tambourine": 54,
        "cowbell": 56  # Need more cowbell!
    }
    
    @staticmethod
    def test_twinkle_star() -> None:
        """
        @brief  Creates a simple 'Twinkle Little Star' MIDI file.
        @return None
        """
        # Create a simpler alias for TICKS_PER_QUARTER
        TPQ = MidiTest.TICKS_PER_QUARTER
        
        # Create MIDI object
        myMidi = MidiWriter()

        # Create tempo event
        myMidi.addBPM(start=0, bpm=MidiTest.DEFAULT_BPM)
        
        # Specify track-channel mapping
        myMidi.setChannel(channel=0, program=0)  # Acoustic Grand Piano

        # Create simple song data
        notes: str = "CCGGAAG_FFEEDDC_GGFFEED_GGFFEED_CCGGAAG_FFEEDDC_"
        letter_to_pitch = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71}
        
        # Loop over song data and create notes
        for beat, note in enumerate(notes):
            note_pitch = letter_to_pitch.get(note, None)
            if note_pitch is None:
                continue  # Skip if not a valid note
            myMidi.addNote(
                pitch=note_pitch,
                start=beat * TPQ,
                duration=TPQ
            )
            if beat == 8:
                myMidi.addBPM(start=beat * TPQ, bpm=80)
            if beat == 16:
                myMidi.addBPM(start=beat * TPQ, bpm=180)
        
        # Write out MIDI object
        output_filename: str = "test_twinkle_star.mid"
        myMidi.save(output_filename)
        print(f"Successfully created {output_filename}")

    @staticmethod
    def test_chords() -> None:
        """
        @brief  Tests multiple notes (chords) occurring simultaneously.
        @return None
        """
        
        # Create MIDI object
        myMidi = MidiWriter()

        # Create tempo event
        myMidi.addBPM(start=0, bpm=MidiTest.DEFAULT_BPM)

        # Specify track-channel mapping
        myMidi.setChannel(channel=0, program=0)  # Acoustic Grand Piano

        # Create a simpler alias for TICKS_PER_QUARTER
        TPQ = MidiTest.TICKS_PER_QUARTER
        
        # Song data for chords
        notes = [
            {"start": 0, "duration": 3, "pitch": 60}, 
            {"start": 0, "duration": 3, "pitch": 64}, 
            {"start": 0, "duration": 3, "pitch": 67}, 
            {"start": 0, "duration": 3, "pitch": 71}, 
            {"start": 4, "duration": 4, "pitch": 60}, 
            {"start": 5, "duration": 4, "pitch": 64}, 
            {"start": 6, "duration": 4, "pitch": 67}, 
            {"start": 7, "duration": 4, "pitch": 71}, 
        ]
        
        # Loop over song data and create notes
        for note in notes:
            myMidi.addNote(
                track=0,
                channel=0,
                start=note.get("start", 0) * TPQ,
                duration=note.get("duration", 1) * TPQ,
                pitch=note.get("pitch", 60)
            )
        
        # Write out MIDI object
        output_filename: str = "test_chords.mid"
        myMidi.save(output_filename)
        print(f"Successfully created {output_filename}")

    @staticmethod    
    def test_multiple_tracks() -> None:
        """
        @brief  Tests creating multiple tracks with a single note on each.
        @detail Good practice to alternate channels between tracks to keep each track separate
                in MuseScore. MuseScore tends to combine staves that share the same program index.
        @return None
        """
        # Create MIDI object
        myMidi = MidiWriter()

        # Create tempo event
        myMidi.addBPM(start=0, bpm=MidiTest.DEFAULT_BPM)
        
        # Specify track-channel mapping (alternate channels)
        myMidi.setChannel(channel=0, program=0)  # Acoustic Grand Piano
        myMidi.setChannel(channel=1, program=0)  # Acoustic Grand Piano
        
        # Create a simpler alias for TICKS_PER_QUARTER
        TPQ = MidiTest.TICKS_PER_QUARTER
        
        # Each note goes into a separate track
        myMidi.addNote(track=0, channel=0, start=0 * TPQ, duration=1 * TPQ, pitch=60)
        myMidi.addNote(track=1, channel=1, start=1 * TPQ, duration=1 * TPQ, pitch=62)
        myMidi.addNote(track=2, channel=0, start=2 * TPQ, duration=1 * TPQ, pitch=64)
        myMidi.addNote(track=3, channel=1, start=3 * TPQ, duration=1 * TPQ, pitch=65)
        
        # Write out MIDI object
        output_filename: str = "test_multiple_tracks.mid"
        myMidi.save(output_filename)
        print(f"Successfully created {output_filename}")

    @staticmethod
    def create_drum_midi(filename: str, bpm: int, patterns: dict) -> None:
        """
        @brief  Creates a MIDI file with the given drum patterns.
        @param  filename (str): Output filename.
        @param  bpm (int): Beats per minute.
        @param  patterns (dict): Mapping from pattern string to drum pitch.
        @return None
        """
        
        # Create MIDI object
        myMidi = MidiWriter()

        # Create tempo event
        myMidi.addBPM(start=0, bpm=bpm)
        
        # Create a simpler alias for 16th note tick value
        TICK_PER_16TH: int = MidiTest.TICKS_PER_QUARTER / 4
        
        # Loop over drum patterns and create drum notes
        for pattern, drum_pitch in patterns.items():
            i = 0
            for c in pattern:
                if c == "x":
                    myMidi.addNote(
                        track=0, 
                        channel=MidiTest.DRUM_CHANNEL, 
                        start=int(i * TICK_PER_16TH), 
                        duration=int(TICK_PER_16TH),
                        pitch=drum_pitch, 
                        velocity=MidiTest.DEFAULT_VELOCITY
                    )
                # Do not increment on "|" separators
                i += 1 if c != "|" else 0
        
        # Write out MIDI object
        myMidi.save(filename)
        print(f"Successfully created {filename}")

    @staticmethod
    def test_amen_drums() -> None:
        """
        @brief  Creates an Amen break drum pattern MIDI file.
        @return None
        """
        amen_patterns = {
            "................|................|................|..........x.....|": MidiTest.DRUMS.get("cymbal_crash1", MidiTest.DEFAULT_DRUM_PITCH),
            "x.x.x.x.x.x.x.x.|x.x.x.x.x.x.x.x.|x.x.x.x.x.x.x.x.|x.x.x.x.x...x.x.|": MidiTest.DRUMS.get("cymbal_ride", MidiTest.DEFAULT_DRUM_PITCH),
            "....x.......x...|....x.......x...|....x.........x.|....x.........x.|": MidiTest.DRUMS.get("snare_drum", MidiTest.DEFAULT_DRUM_PITCH),
            ".......x.x.....x|.......x.x.....x|.......x.x......|.x.....x.x......|": MidiTest.DRUMS.get("snare_drum_rim", MidiTest.DEFAULT_DRUM_PITCH),
            "x.........xx....|x.........xx....|x.x.......x.....|..xx......x.....|": MidiTest.DRUMS.get("kick_drum", MidiTest.DEFAULT_DRUM_PITCH)
        }
        SONG_BPM: int = 170
        MidiTest.create_drum_midi("test_drum_amen.mid", SONG_BPM, amen_patterns)

    @staticmethod
    def test_disco_drums() -> None:
        """
        @brief  Demonstrates a simple disco drum beat in a MIDI file.
        @return None
        """
        disco_patterns = {
            "|x...............|................|................|................|x...............|": MidiTest.DRUMS.get("cymbal_crash1", MidiTest.DEFAULT_DRUM_PITCH),
            "|................|................|x...x...x...x...|................|................|": MidiTest.DRUMS.get("cymbal_ride", MidiTest.DEFAULT_DRUM_PITCH),
            "|................|................|..x...x...x...x.|................|................|": MidiTest.DRUMS.get("cymbal_ride_bell", MidiTest.DEFAULT_DRUM_PITCH),
            "|....xx.xxx.xxx.x|xx.xxx.xxx.xxx.x|................|................|................|": MidiTest.DRUMS.get("cymbal_hihat_closed", MidiTest.DEFAULT_DRUM_PITCH),
            "|......x...x...x.|..x...x...x...x.|................|................|................|": MidiTest.DRUMS.get("cymbal_hihat_open", MidiTest.DEFAULT_DRUM_PITCH),
            "|................|................|................|xxx.............|................|": MidiTest.DRUMS.get("tom5", MidiTest.DEFAULT_DRUM_PITCH),
            "|................|................|................|...xxx..........|................|": MidiTest.DRUMS.get("tom4", MidiTest.DEFAULT_DRUM_PITCH),
            "|................|................|................|......xxx.......|................|": MidiTest.DRUMS.get("tom3", MidiTest.DEFAULT_DRUM_PITCH),
            "|................|................|................|.........xxx....|................|": MidiTest.DRUMS.get("tom2", MidiTest.DEFAULT_DRUM_PITCH),
            "|x...x...x...x...|x...x...x...x...|x...x...x...x...|x...x...x...x...|x...............|": MidiTest.DRUMS.get("cowbell", MidiTest.DEFAULT_DRUM_PITCH),
            "|....x.......x..x|....x.......xxxx|...x..x....x..x.|............xxxx|................|": MidiTest.DRUMS.get("snare_drum", MidiTest.DEFAULT_DRUM_PITCH),
            "|x.....x...x..x..|x.....x...x..x..|x.....x...x..x..|x...x...x...x...|x...............|": MidiTest.DRUMS.get("kick_drum", MidiTest.DEFAULT_DRUM_PITCH)
        }
        SONG_BPM: int = 125
        MidiTest.create_drum_midi("test_drums_disco.mid", SONG_BPM, disco_patterns)
    
    @staticmethod
    def main() -> None:
        """
        @brief  Runs tests and demonstrates example usage.
        @return None
        """
        print("*" * 80)
        
        MidiTest.test_twinkle_star()
        MidiTest.test_chords()
        MidiTest.test_multiple_tracks()
        MidiTest.test_amen_drums()
        MidiTest.test_disco_drums()
        
        print("*" * 80)
        print("Successfully ran all tests!")


if __name__ == "__main__":
    MidiTest.main()


