"""
Text mining project.
Compares two texts (e.g., two books), and returns how similar they are, percent-wise, as calculated solely from looking at shared words.
I was planning on making this a bit more ambitious, by using Pattern's sentiment analysis features as well--but I've had a nasty bug these last couple days.
-Matt, February
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


def percentify(word_list, num):
	"""
	takes in a word list; returns a list of the [num] most-used words, in order, and the corresponding percentage of the work it composes.
	"""
	word_counts = {}
	for word in word_list:
		if word in word_counts:
			word_counts[word] += 1.0
		else:
			word_counts[word] = 1.0
	words_in_order = sorted(word_counts, key=word_counts.get, reverse=True)
	if len(words_in_order) >= num:
		return [words_in_order[:num], [word_counts[word]/len(word_list) for word in words_in_order[:num]]]
	else:
		return [words_in_order, [word_counts[word]/len(word_list)for word in words_in_order]]


def comparator(list1, list2):
	"""
	Takes in two lists of two lists; compares percentages and then returns the overlap fraction.
	"""
	similarity = 0.0
	words1 = list1[0]
	percents1 = list1[1]
	words2 = list2[0]
	percents2 = list2[1]
	list1_percent_dictionary = {words1[i]: percents1[i] for i in range(0,len(words1))}
	list2_percent_dictionary = {words2[i]: percents2[i] for i in range(0, len(words2))}
	for word in words1:
		if word in words2:
			similarity += min(list1_percent_dictionary[word], list2_percent_dictionary[word])		
	return similarity


def book_comparer(book1, book2):
	"""
	wrapper for the rest! put in two book files as strings, and then it does the rest. Since computation speed hasn't proven to be an issue yet, it does it for all words in book 1; if speed bogs down, num can be set to a different value (e.g. 500).
	"""
	word_list_1 = turn_into_list(book1)
	word_list_2 = turn_into_list(book2)
	num = len(word_list_1)
	similarity = comparator(percentify(word_list_1, num), percentify(word_list_2, num))
	return similarity

if __name__ == "__main__":
	first_book = 'Alice_in_Wonderland.txt'
	second_book = 'Metamorphosis.txt'
	print(first_book[:-4] + ' is ' + str(int(round(book_comparer(first_book, second_book) * 100.0))) + ' percent equivalent to ' + second_book[:-4] + ' (in a conceptually similar way to how humans are 80 percent genetically identical to cows).')
	first_book = 'The_Adventures_of_Huckleberry_Finn.txt'
	second_book = 'The_Adventures_of_Tom_Sawyer.txt'
	print(first_book[:-4] + ' is ' + str(int(round(book_comparer(first_book, second_book) * 100.0))) + ' percent equivalent to ' + second_book[:-4] + ' (in a conceptually similar way to how humans are 80 percent genetically equivalent to cows).')