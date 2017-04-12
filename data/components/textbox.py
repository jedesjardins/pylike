from engine.ecs import Component
import pygame

class Textbox(Component):

    def __init__(self, parent, text, max_length=30):
        self.parent = parent
        self.text = text
        self.elapsed_time = 0

        line = 0
        lines = [[]]
        line_length = [0]
        words = text.split(' ')
        for word in words:
        	if line_length[line] + len(lines[line]) + len(word) <= max_length:
        		lines[line].append(word)
        		line_length[line] += len(word)
        	else:
        		line += 1
        		lines.append([word])
        		line_length.append(len(word))

        for i in range(0, len(lines)):
        	lines[i] = ' '.join(lines[i])

        self.lines = lines

        """
        self.total_length = 0
        self.total_past_line_length = 0
        self.last_char = 0
        self.last_line = 0

        self.finished = False
        self.closed = False
        self.flush = False

        self.output_buffer = [[]]
        self.changed = False

		"""