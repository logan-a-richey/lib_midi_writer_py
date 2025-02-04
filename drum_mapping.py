#!/usr/bin/python3

class DrumMapping:
    NAME_TO_NUMBER = {
        # TODO "pretty-fy the key-value spacing
        "laser" : 27,
        "whip": 28,
        "scratch_push": 29,
        "scratch_pull": 30,
        "sticks": 31,
        "metronome_click": 32,
        "metronome_bell": 33,
        "bass_drum": 34,
        "kick_drum": 35,  # COMMON
        "bass_drum_1": 36,
        "snare_cross_stick": 37,  # COMMON
        "snare_drum_1": 38,  # COMMON
        "hand_clap": 39,  # COMMON
        "snare_drum_2": 40,
        "tom_1": 41,  # COMMON
        "cymbal_hi_hat_closed": 42,  # COMMON
        "tom_2": 43,  # COMMON
        "cymbal_hi_hat_pedal": 44,  # COMMON
        "tom_3": 45,  # COMMON
        "cymbal_hi_hat_open": 46,  # COMMON
        "tom_4": 47,  # COMMON
        "tom_5": 48,  # COMMON
        "cymbal_crash_1": 49,  # COMMON
        "tom_6": 50,  # COMMON
        "cymbal_ride_1": 51,  # COMMON
        "cymbal_china": 52,  # COMMON
        "cymbal_ride_bell": 53,  # COMMON
        "tambourine": 54,  # COMMON
        "cymbal_splash": 55,  # COMMON
        "cowbell": 56,  # COMMON
        "cymbal_crash_2": 57,  # COMMON
        "vibraslap": 58,
        "cymbal_ride_2": 59,
        "high_bongo": 60,
        "low_bongo": 61,
        "conga_dead_stroke": 62,
        "conga": 63,
        "high_timbale": 64,
        "low_timbale": 65,
        "high_agogo": 66,
        "low_agogo": 67,
        "cabasa": 68,
        "maracas": 69,
        "whistle_short": 70,
        "whistle_long": 71,
        "guiro_short": 72,
        "guiro_long": 73,
        "claves": 74,
        "high_woodblock": 75,
        "low_woodblock": 76,
        "cuica_high": 77,
        "cuica_low": 78,
        "triangle_mute": 79,  # COMMON
        "triangle_open": 80,  # COMMON
        "shaker": 81,
        "sleigh_bell": 82,
        "bell_tree": 83,
        "castanets": 84,
        "surdu_dead_stroke": 85,
        "surdu": 86,
        "snare_drum_rod": 87,
        "ocean_drum": 88,
        "snare_drum_brush": 89,
    }


if __name__ == "__main__":
    DM = DrumMapping()
    print("PROGRAM MAPPING: NAME TO NUMBER")
    print("*" * 80)
    for k,v in DM.NAME_TO_NUMBER.items():
        print("{}: {}".format(
            f"\"{k}\"".ljust(30),
            str(v)
        ))
    print("*" * 80)

