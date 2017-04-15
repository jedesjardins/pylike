#!/usr/bin/python3
"""
"""

def say(line):
	text_array = line.split()
	text = ' '.join(text_array[1:])
	print(text)

def menu(line):
	all_array = line.split()
	text_array = []
	options_to_blocks = []

	for word in all_array[1:]:
		if word[0] == '#':
			break
		text_array.append(word)

	text = ' '.join(text_array)
	
	print('menu:', text)

with open('script', 'r') as script:
	blocks = {}
	curr_block = None

	for line in script.readlines():
		l = line.strip()
		if not l:
			continue
		if l[0] == '$':
			curr_block = l[1:]
			blocks[curr_block] = []

		else:
			if '#say' in l:
				say(l)
			if '#menu' in l:
				menu(l)

			blocks[curr_block].append(l)

