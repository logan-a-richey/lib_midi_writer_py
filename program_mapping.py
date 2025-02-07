#!/usr/bin/python3

class ProgramMapping:
    """ 
    @brief     Helpful encapsulated mappings for program to instrument.
    @detail    While using MidiWriter.setChannel(int channel, int program)
    
    @usage
    ```
    from midi_writer import MidiWriter
    myMidi = MidiWriter(
    inst_id = ProgramMapping.NAME_TO_NUMBER.get("rock_organ", 0) # should return 18 from "rock_organ"
    myMidi.setChannel(channel=0, inst_id)
    ```
    """
    
    '''
    # possible class lookup for numbers
    class Piano: 
        # class variables to easy lookup in an IDE:
        acoustic_grand_piano    = 0, 
        bright_acoustic_piano   = 1, 
        electric_grand_piano    = 2, 
        honky-tonk_piano        = 3, 
        rhodes_piano            = 4, 
        chorused_piano          = 5, 
        harpsichord             = 6, 
        clavinet                = 7, 
    '''

    NAME_TO_NUMBER = {
        # Category: Piano
        "acoustic_grand_piano"    : 0, 
        "bright_acoustic_piano"   : 1, 
        "electric_grand_piano"    : 2, 
        "honky-tonk_piano"        : 3, 
        "rhodes_piano"            : 4, 
        "chorused_piano"          : 5, 
        "harpsichord"             : 6, 
        "clavinet"                : 7, 

        # Category: Chromatic Percussion
        "celesta"                 : 8, 
        "glockenspiel"            : 9, 
        "music_box"               : 10, 
        "vibraphone"              : 11, 
        "marimba"                 : 12, 
        "xylophone"               : 13, 
        "tubular_bells"           : 14, 
        "dulcimer"                : 15,

        # Category: Organ
        "hammond_organ"           : 16, 
        "percussive_organ"        : 17, 
        "rock_organ"              : 18, 
        "church_organ"            : 19, 
        "reed_organ"              : 20, 
        "accordion"               : 21, 
        "harmonica"               : 22, 
        "tango_accordion"         : 23,

        # Category: Guitar
        "acoustic_guitar_(nylon)" : 24, 
        "acoustic_guitar_(steel)" : 25, 
        "electric_guitar_(jazz)"  : 26, 
        "electric_guitar_(clean)" : 27, 
        "electric_guitar_(muted)" : 28, 
        "overdriven_guitar"       : 29, 
        "distortion_guitar"       : 30, 
        "guitar_harmonics"        : 31,

        # Category: Bass
        "acoustic_bass"           : 32, 
        "electric_bass_(finger)"  : 33, 
        "electric_bass_(pick)"    : 34, 
        "fretless_bass"           : 35, 
        "slap_bass_1"             : 36, 
        "slap_bass_2"             : 37, 
        "synth_bass_1"            : 38, 
        "synth_bass_2"            : 39,

        # Category: String
        "violin"                  : 40, 
        "viola"                   : 41, 
        "cello"                   : 42, 
        "contrabass"              : 43, 
        "tremolo_strings"         : 44, 
        "pizzicato_strings"       : 45, 
        "orchestral_harp"         : 46, 
        "timpani"                 : 47,

        # Category: Ensemble
        "string_ensemble_1"       : 48, 
        "string_ensemble_2"       : 49, 
        "synth_strings_1"         : 50, 
        "synth_strings_2"         : 51, 
        "choir_aahs"              : 52, 
        "voice_oohs"              : 53, 
        "synth_voice"             : 54, 
        "orchestra_hit"           : 55,

        # Category: Brass
        "trumpet"                 : 56, 
        "trombone"                : 57, 
        "tuba"                    : 58, 
        "muted_trumpet"           : 59, 
        "french_horn"             : 60, 
        "brass_section"           : 61, 
        "synth_brass_1"           : 62, 
        "synth_brass_2"           : 63,

        # Category: Reed
        "soprano_sax"             : 64, 
        "alto_sax"                : 65, 
        "tenor_sax"               : 66, 
        "baritone_sax"            : 67, 
        "oboe"                    : 68, 
        "english_horn"            : 69, 
        "bassoon"                 : 70, 
        "clarinet"                : 71,

        # Category: Woodwind
        "piccolo"                 : 72, 
        "flute"                   : 73, 
        "recorder"                : 74, 
        "pan_flute"               : 75, 
        "bottle_blow"             : 76, 
        "shakuhachi"              : 77, 
        "whistle"                 : 78, 
        "ocarina"                 : 79,

        # Category: Synth Lead
        "lead_1_(square)"         : 80,
        "lead_2_(sawtooth)"       : 81,
        "lead_3_(calliope_lead)"  : 82,
        "lead_4_(chiffer_lead)"   : 83,
        "lead_5_(charang)"        : 84,
        "lead_6_(voice)"          : 85,
        "lead_7_(fifths)"         : 86,
        "lead_8_(brass_+_lead)"   : 87,

        # Category: Synth Pad
        "pad_1_(new_age)"         : 88, 
        "pad_2_(warm)"            : 89, 
        "pad_3_(polysynth)"       : 90, 
        "pad_4_(choir)"           : 91, 
        "pad_5_(bowed)"           : 92, 
        "pad_6_(metallic)"        : 93, 
        "pad_7_(halo)"            : 94, 
        "pad_8_(sweep)"           : 95,

        # Category: Synth Effect
        "fx_1_(rain)"             : 96, 
        "fx_2_(soundtrack)"       : 97, 
        "fx_3_(crystal)"          : 98, 
        "fx_4_(atmosphere)"       : 99, 
        "fx_5_(brightness)"       : 100, 
        "fx_6_(goblins)"          : 101, 
        "fx_7_(echoes)"           : 102, 
        "fx_8_(sci-fi)"           : 103,

        # Category: Ethnic
        "sitar"                   : 104, 
        "banjo"                   : 105, 
        "shamisen"                : 106, 
        "koto"                    : 107, 
        "kalimba"                 : 108, 
        "bagpipe"                 : 109, 
        "fiddle"                  : 110, 
        "shana"                   : 111,

        # Category: Aux Percussion
        "tinkle_bell"             : 112, 
        "agogo"                   : 113, 
        "steel_drums"             : 114, 
        "woodblock"               : 115, 
        "taiko_drum"              : 116, 
        "melodic_tom"             : 117, 
        "synth_drum"              : 118, 
        "cymbal_reverse"          : 119,

        # Category: SFX
        "guitar_fret_noise"       : 120, 
        "breath_noise"            : 121, 
        "seashore"                : 122, 
        "bird_tweet"              : 123, 
        "telephone_ring"          : 124, 
        "helicopter"              : 125, 
        "applause"                : 126, 
        "gunshot"                 : 127, 
    }


if __name__ == "__main__":
    PM = ProgramMapping()
    print("PROGRAM MAPPING: NAME TO NUMBER")
    print("*" * 80)
    for k,v in PM.NAME_TO_NUMBER.items():
        print("{}: {}".format(
            f"\"{k}\"".ljust(30),
            str(v)
        ))
    print("*" * 80)

