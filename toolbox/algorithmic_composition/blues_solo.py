""" Synthesizes a blues solo algorithmically """

from Nsound import *
import numpy
import random

def add_note(out, instr, key_num, duration, bpm, volume):
    """ Adds a note from the given instrument to the specified stream

        out: the stream to add the note to
        instr: the instrument that should play the note
        key_num: the piano key number (A 440Hzz is 49)
        duration: the duration of the note in beats
        bpm: the tempo of the music
        volume: the volume of the note
	"""
    freq = (2.0**(1/12.0))**(key_num-49)*440.0
    stream = instr.play(duration*(60.0/bpm),freq)
    stream *= volume
    out << stream

# this controls the sample rate for the sound file you will generate
sampling_rate = 44100.0
Wavefile.setDefaults(sampling_rate, 16)

bass = GuitarBass(sampling_rate)	# use a guitar bass as the instrument
solo = AudioStream(sampling_rate, 1)

""" these are the piano key numbers for a 3 octave blues scale in A
	See: http://en.wikipedia.org/wiki/Blues_scale """
blues_scale = [25, 28, 30, 31, 32, 35, 37, 40, 42, 43, 44, 47, 49, 52, 54, 55, 56, 59, 61]
beats_per_minute = 45			# Let's make a slow blues solo

curr_note = 6

possible_licks =    [
                        [ [1, .5], [1, .5], [1, .5], [1, .5] ],
                        [ [-1, .5], [-1, .5], [-1, .5], [-1, .5] ],
                        [ [0, .5/3], [0, .5/3], [0, .5/3], [1, .5], [1, .5], [1, .5] ],
                        [ [0, .5/3], [0, .5/3], [0, .5/3], [-1, .5], [-1, .5], [-1, .5] ]
                    ]


def coerce_to_scale(note):
    """what it says on the tin."""
    if note <= 0:
        note = 0
    elif note >= len(blues_scale):
        note = len(blues_scale) - 1
    return note

def make_it_swing(j, beats_so_far, current_lick, curr_note):
    """
    Makes the notes "swing" length based on index j, making sure to not break measure (e.g., make a lick longer than its measure should be, as determined by comparing "beats_so_far" to 2.0)
    """
    if j%2 == 0:
        if beats_so_far + current_lick[j][1]*1.2 <= 2:
            add_note(solo, bass, blues_scale[curr_note], current_lick[j][1]*1.2, beats_per_minute, 1.0)
            beats_so_far += current_lick[j][1]*1.2
        else:
            if 2.0 - beats_so_far <- 0.0:
                return 2.0
            add_note(solo, bass, blues_scale[curr_note], 2.0-beats_so_far, beats_per_minute, 1.0)
            beats_so_far = 2.0
    else:
        if beats_so_far + current_lick[j][1]*0.8 <= 2:
            add_note(solo, bass, blues_scale[curr_note], current_lick[j][1]*0.8, beats_per_minute, 1.0)
            beats_so_far += current_lick[j][1]*0.8
        else:
            if 2.0 - beats_so_far <= 0.0:
                return 2.0
            add_note(solo, bass, blues_scale[curr_note], 2.0-beats_so_far, beats_per_minute, 1.0)
            beats_so_far = 2.0
    return beats_so_far

def add_lick(current_lick, curr_note, i):
    """
    Adds a full lick, current_lick, from curr_note on at position i.
    """
    beats_so_far = 0.0;
    for j in range(len(current_lick)):
        if j == 0 and i in [2,6]:
            curr_note = 6
        else:
            curr_note = coerce_to_scale(curr_note + current_lick[j][0])
        if beats_so_far >= 2.0:
            break
        else:
            beats_so_far = make_it_swing(j, beats_so_far, current_lick, curr_note)

if __name__ == "__main__":
    for i in range(8):
        current_lick = random.choice(possible_licks)
        add_lick(current_lick, curr_note, i)
    add_note(solo, bass, blues_scale[random.choice([0,6,12])], 4.0, beats_per_minute, 1.0) #sustained final note is apparently good form for blues.
    solo >> "blues_solo.wav"