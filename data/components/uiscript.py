
from engine.ecs import Component
from copy import deepcopy

class UIScript(Component):

    """ A script wraps a list of actions. Each action is completed before the
        next starts.
        Scripts need to know when an action ends.
        Scripts need to support branching based on menu's 
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
            if word[0] == '>' and i != 0:
                options_index = i
                break
            text_array.append(word)

        text = ' '.join(text_array[1:])

        index = options_index
        options = []
        while index < len(all_array):
            options.append((all_array[index][1:], all_array[index+1][1:]))
            index += 2

        
        return ('menu', text, options)

    def set_flag(line):
        all_array = line.split()
        flags = []

        for i in range(1, len(all_array)):
            flags.append(all_array[i][1:])

        return ('setflag', flags)

    def unset_flag(line):
        all_array = line.split()
        flags = []

        for i in range(1, len(all_array)):
            flags.append(all_array[i][1:])

        return ('unsetflag', flags)

    def check_flag(line):
        all_array = line.split()
        flag = all_array[1][1:]
        true_block = all_array[2][1:]
        false_block = all_array[3][1:]

        return ('checkflag', flag, true_block, false_block)

    def parse_script(file):
        with open('data/scripts/' + file, 'r') as script:
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
                        blocks[curr_block].append(UIScript.say(l))
                    elif '#menu' in l:
                        blocks[curr_block].append(UIScript.menu(l))
                    elif '#setflag' in l:
                        blocks[curr_block].append(UIScript.set_flag(l))
                    elif '#unsetflag' in l:
                        blocks[curr_block].append(UIScript.unset_flag(l))
                    elif '#checkflag' in l:
                        blocks[curr_block].append(UIScript.check_flag(l))

                    else:
                        print('error')

                    #blocks[curr_block].append(l)
            return blocks

    def AutoScript(script_file):
        #blocks['enter'] = [('text', 'yo, waddup')]
        blocks = UIScript.parse_script(script_file)
        return UIScript(blocks)

    info = {
            'output_buffer': [[]],
            'finished': False,
            'speedup': False,
            'stop': False,
            'elapsed_time': 0,
            'last_char': 0,
            'selection': 0,
            'selected': False,
            'next_block': None
        }
    
    def __init__(self, actions):
        self.running = False
        self.blocks = actions
        self.curr_block = 'enter'
        self.curr_line = 0
        self.target = None
        self.lock = None
        self.text_image = None

        self.info = deepcopy(UIScript.info)