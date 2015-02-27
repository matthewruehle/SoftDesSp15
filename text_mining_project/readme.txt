This folder contains several moving parts.

text_file_extractor.py:
	The file text_file_extractor.py contains two functions--one which grabs a text file from the web and then stores it offline, and another which does the same thing but also removes "Project Gutenberg" headers and footers. It's chiefly used to gather text files for the main project.

text_mining_project.py:
	The main project is text_mining_project.py, which contains a "wrapper" function (and various sub-functions) which compares the similarity of two different text files, based on words shared/word similarity as a percentage. If this file is run as __main__, it also prints out examples.

text_mining_project_writeup.txt, text_mining_project_writeup.pdf:
	text_mining_project_writeup.txt and .pdf are writeups of the project response.

miscellaneous .txt files:
	The other files (e.g., 'Alice_in_Wonderland.txt', 'Metamorphosis.txt', 'To_Kill_a_Mockingbird.txt', etc.) are text files extracted from the internet - some from Project Gutenberg, and one (Mockingbird) from elsewhere. There's nothing special about them specifically--they're just examples of text files which can be tried out. Also, "Alice," "Metamorphosis," and the Twain books are necessary to run the "demo" built into the main project.