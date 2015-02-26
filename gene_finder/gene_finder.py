# -*- coding: utf-8 -*-
"""
@author: Matt Ruehle
Gene Finder program.
"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq, load_salmonella_genome

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###
nucleotide_dict = {'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C'}

def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide

        A couple extra get_complement tests here, because there's few enough cases and it's important enough to check both ways:

    >>> get_complement('C')
    'G'
    >>> get_complement('T')
    'A'
    >>> get_complement('A')
    'T'
    >>> get_complement('G')
    'C'
    """
    return nucleotide_dict[nucleotide]

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    reverse = list(dna[::-1]) #creates reverse, a list of the characters in dna in reverse order.
    for i in range(len(reverse)):
        reverse[i] = get_complement(reverse[i])
    reverse_complement = "".join(reverse)
    return reverse_complement

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string

        Added one test, for an input sequence with no stop codon, and one test for an input sequence with no stop and where the last 2 and first 1 are a stop.
        Other tests seem sufficient: makes sure out-of-frame stops don't get picked up, but in-frame stops do.
    >>> rest_of_ORF("ATGCGATG")
    'ATGCGATG'
    >>> rest_of_ORF("ATGCGACTC")
    'ATGCGACTC'
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    """
    ORF = []
    for i in range(0,len(dna),3):
        if dna[i:i+3] in ['TAG','TAA','TGA']:
            return "".join(ORF)
        else:
            ORF.append(dna[i:i+3])
    return "".join(ORF)

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

        This test looks sufficient: tests for multiple ones, but also avoids nested ORFs and out-of-frame ORFs.

    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    """
    ORF_list = []
    i = 0
    while i < len(dna)-2:
        if dna[i:i+3] == 'ATG':
            new_ORF = rest_of_ORF(dna[i:])
            ORF_list.append(new_ORF)
            i += len(new_ORF)
        else:
            i += 3
    return ORF_list

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    ORFs = []
    for i in range(0,3):
        ORFs.extend(find_all_ORFs_oneframe(dna[i:]))
    return ORFs

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
        This test looks like enough - it checks for an ORF from both directions, and if the earlier functions work there hopefully wouldn't be any other new sources of error.

    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    both_all_ORFs = []
    both_all_ORFs.extend(find_all_ORFs(dna))
    both_all_ORFs.extend(find_all_ORFs(get_reverse_complement(dna)))
    return both_all_ORFs


def longest_ORF(dna):
    """ 
    Finds the longest ORF on both strands of the specified DNA and returns it as a string

    ...what if there are more than one ORFs of equal length? Based on the rest of the functions, I feel like I might just want to return one--but I'm not positive :|. I'll go with that for now.

    This unit test looks sufficient: anything which it wouldn't catch, earlier tests should.

    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    ORF_list = find_all_ORFs_both_strands(dna)
    longest_ORF = ['']
    longest_length = 0
    for entry in ORF_list:
        if len(entry) > longest_length:
            longest_ORF[0] = entry
            longest_length = len(entry)
    return longest_ORF[0]


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF 

        Note: I would contend that we would want to run, say, 30-40 trials - enough to assume a normal distribution - and then go with the 95th percentile. Too few trials is bad, but if we just go with the flat maximum we leave ourselves prone to outliers.

        Random, so no way to do unit testing--though we could conceivably just run it a couple times to see if results seem "gut-check" reasonable.
        """
    lengths = []
    for i in range(0, num_trials):
        lengths.append(len(longest_ORF(shuffle_string(dna))))
    return max(lengths)

# print(longest_ORF_noncoding('ATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAA',100))
# print(len('ATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAAATGCGAATGTAGCATCAAA'))
# #these statements just test longest_ORF_noncoding to see if the results seem reasonable. They do.


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
<<<<<<< HEAD
    aminos = []
    i = 0
    while (len(dna) - i) > 2:
        aminos.append(aa_table[dna[i:i+3]])
        i += 3
    return "".join(aminos)

def gene_finder(dna):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
=======
    # TODO: implement this
    pass

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
>>>>>>> 922a6e32441860ab0413630f74531e6e47a16a7c
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    threshold = longest_ORF_noncoding(dna, 1500) # 1500 is just a fiat; no particular reason on my part.
    all_orfs = find_all_ORFs_both_strands(dna)
    filtered_orfs = [orf for orf in all_orfs if len(orf) >= threshold]
    aa_sequences = [coding_strand_to_AA(orf) for orf in filtered_orfs]
    return aa_sequences

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    dna = load_seq("./data/X73525.fa")
    results = gene_finder(dna)
    print(results)
