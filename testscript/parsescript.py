#!/usr/bin/python3
"""
"""

def say(line):
	text_array = line.split()
	text = ' '.join(text_array[1:])
	return ('text', text)

def menu(line):
	all_array = line.split()
	text_array = []
	options_to_blocks = []

	options_index = 0

	for i in range(0, len(all_array)):
		word = all_array[i]
		if word[0] == '#' and i != 0:
			options_index = i
			break
		text_array.append(word)

	text = ' '.join(text_array)

	index = options_index
	options = []
	while index < len(all_array):
		options.append((all_array[index][1:], all_array[index+1][1:]))
		index += 2

	
	return ('menu', text, options)

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
				blocks[curr_block].append(say(l))
			if '#menu' in l:
				blocks[curr_block].append(menu(l))

			#blocks[curr_block].append(l)

