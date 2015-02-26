"""
Gets the word frequencies of a text file.
In the interests of making this more applicable to other projects (e.g., mini-proj 3), I'm ommitting the part that scans for project Gutenberg-specific markers. If that's really necessary for the deliverable, I can add/show a version with it included.
Matt Ruehle, Feb 2015.
"""

import string

def turn_into_list(book):
	"""
	turns a text file into a list of its words. Ignores case and punctuation; diferentiates words based on white space.
	Make sure the input is a *string*!!!
	"""
	word_list = []
	text = open(book, 'r')
	lines = text.readlines()
	for line in lines:
		working = string.translate(line, None, string.punctuation)
		word_list.extend(working.lower().rsplit())
	return word_list

def get_top_words(word_list, num):
	"""
	Returns the list of the [num] most-used words, and the number of times each of them is used.
	"""
	word_counts = {}
	for word in word_list:
		if word in word_counts:
			word_counts[word] += 1
		else:
			word_counts[word] = 1
	words_in_order = sorted(word_counts, key=word_counts.get, reverse=True)
	if len(words_in_order) >= num:
		return words_in_order[:num]
	else:
		return words_in_order

def wrapper(book, num):
	"""
	neat single commands for a predetermined book. returns a list of the form:
	[[top num words],[corresponding counts]], e.g.:
	[['and','the','a','so'],[5,4,3,2]]
	"""
	specific_list = turn_into_list(book)
	top_n = get_top_words(specific_list, num)
	corresponding_counts = [word_counts[word] for word in top_n]
	result = []
	result.append(top_n)
	result.append(corresponding_counts)
	return result

# if __name__ == "__main__":
# 	flatland_histogram = wrapper('flatland.txt',100)
# 	flatland_words = flatland_histogram[0]
# 	flatland_counts = flatland_histogram[1]
# 	output = open('flatland_word_counts.txt','w')
# 	output.write('Word:               Count:\n')
# 	output.write('-'*25 + '\n')
# 	for i in range(0,100):
# 		output.write(flatland_words[i] + (' '*(20 - len(flatland_words[i]))) + str(flatland_counts[i]) + '\n')

"""
output of the mini-project should be something like,
___ is 98 '%' like ____ (in the same way as humans are 98 percent monkeys, or 80 percent banana).
"""

"""
NEW IDE:
find and compare the top 100 *outside of* the top 100 most-used overall,
so we get rid of the influence of "the," "of", "and", "a", "i", etc!
that should be possible if I can find the top 100 most-used overall, which shouldln't be too difficult!
After that, it's just a simple list comprehension.
"""