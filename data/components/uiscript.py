
from engine.ecs import Component

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
                    else:
                        print('error')

                    #blocks[curr_block].append(l)
            return blocks

    def AutoScript(script_file):
        #blocks['enter'] = [('text', 'yo, waddup')]
        blocks = UIScript.parse_script(script_file)
        return UIScript(blocks)
    
    def __init__(self, actions):
        self.running = False
        self.blocks = actions
        self.curr_block = 'enter'
        self.curr_line = 0
        self.target = None
        self.lock = None

        self.info = {
            'output_buffer': [[]],
            'finished': False,
            'speedup': False
            'stop': False,
            'elapsed_time': 0
            'last_char': 0
        }