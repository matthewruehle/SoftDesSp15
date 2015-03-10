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

curr_note = 0

possible_licks =    [
                        [ [1, .5], [1, .5], [1, .5], [1, .5] ],
                        [ [-1, .5], [-1, .5], [-1, .5], [-1, .5] ],
                        [ [0, .5/3], [0, .5/3], [0, .5/3], [1, .5], [1, .5], [1, .5] ],
                        [ [0, .5/3], [0, .5/3], [0, .5/3], [-1, .5], [-1, .5], [-1, .5] ]
                    ]


"""
the following is a *ton* of if/elif/else statements. This is made to give it good "swing" without breaking the measure structure, and to have the solo & sub-solo 4-measure sections "conclude" nicely.
The if-s are for music-y, rather than code-y, purposes. That said, something to make it cleaner/more efficient would be A-OK.
"""

for i in range(8):
    current_lick = random.choice(possible_licks)
    if i == 2 or i == 6:
        beats_so_far = 0.0
        for j in range(len(current_lick)):
            curr_note += current_lick[j][0]
            if curr_note < 0:
                curr_note = 0
            elif curr_note >= len(blues_scale):
                curr_note = len(blues_scale)-1
            if j == 0:
                curr_note = random.choice([6])
            if j%2 == 0:
                if beats_so_far + current_lick[j][1]*1.2 <= 2:
                    add_note(solo, bass, blues_scale[curr_note], current_lick[j][1]*1.2, beats_per_minute, 1.0)
                else:
                    add_note(solo, bass, blues_scale[curr_note], 2.0-beats_so_far, beats_per_minute, 1.0)
            else:
                if beats_so_far +  current_lick[j][1]*.8 <= 2:
                    add_note(solo, bass, blues_scale[curr_note], current_lick[j][1]*.8, beats_per_minute, 1.0)
                else:
                    add_note(solo, bass, blues_scale[curr_note], 2.0-beats_so_far, beats_per_minute, 1.0)
    elif i == 7:
        for j in range(len(current_lick)-1):
            curr_note += current_lick[j][0]
            if curr_note < 0:
                curr_note = 0
            elif curr_note >= len(blues_scale):
                curr_note = len(blues_scale)-1
            if j == len(current_lick) - 2:
                add_note(solo, bass, blues_scale[curr_note], 2.0-beats_so_far, beats_per_minute, 1.0)
            elif j%2 == 0:
                if beats_so_far + current_lick[j][1]*1.2 <= 2:
                    add_note(solo, bass, blues_scale[curr_note], current_lick[j][1]*1.2, beats_per_minute, 1.0)
                else:
                    add_note(solo, bass, blues_scale[curr_note], 2.0-beats_so_far, beats_per_minute, 1.0)
            else:
                if beats_so_far +  current_lick[j][1]*.8 <= 2:
                    add_note(solo, bass, blues_scale[curr_note], current_lick[j][1]*.8, beats_per_minute, 1.0)
                else:
                    add_note(solo, bass, blues_scale[curr_note], 2.0-beats_so_far, beats_per_minute, 1.0)
    else:
        beats_so_far = 0.0
        for j in range(len(current_lick)):
            curr_note += current_lick[j][0]
            if curr_note < 0:
                curr_note = 0
            elif curr_note >= len(blues_scale):
                curr_note = len(blues_scale)-1
            if j%2 == 0:
                if beats_so_far + current_lick[j][1]*1.2 <= 2:
                    add_note(solo, bass, blues_scale[curr_note], current_lick[j][1]*1.2, beats_per_minute, 1.0)
                else:
                    add_note(solo, bass, blues_scale[curr_note], 2.0-beats_so_far, beats_per_minute, 1.0)
            else:
                if beats_so_far +  current_lick[j][1]*.8 <= 2:
                    add_note(solo, bass, blues_scale[curr_note], current_lick[j][1]*.8, beats_per_minute, 1.0)
                else:
                    add_note(solo, bass, blues_scale[curr_note], 2.0-beats_so_far, beats_per_minute, 1.0)

solo >> "blues_solo.wav"