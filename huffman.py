import os


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def __lt__(self, other):
        return comes_before(self, other)


def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file"""

    try:
        txt_file = open(filename)
        text_string = txt_file.read()  # have to check for file not found and empty file
    except:
        raise FileNotFoundError('cannot read from empty file')
        
    txt_file.close()
    if text_string == '':
        return [0] * 256
    freq_list = [0] * 256

    for char in text_string:
        if ord(char) >= 0 or ord(char) <= 255:
            freq_list[ord(char)] += 1

    return freq_list

    # front = 0
    # back = 254
    # trimmed_list = []
    # for frontIndex in range(len(freq_list)):
    #     if freq_list[frontIndex] != 0:
    #         front = frontIndex
    #         break
    #
    # for backIndex in range(len(freq_list), 0, -1):
    #     if freq_list[backIndex] != 0:
    #         back = backIndex + 1
    #         break


def comes_before(a, b):
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a is None or b is None:
        return False
    elif a.freq < b.freq:
        return True
    elif b.freq < a.freq:
        return False
    else:
        return a.char < b.char


def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""
    if comes_before(a, b):
        # I dont think its right that child1.char just goes in when it says minimum
        parent = HuffmanNode(a.char, a.freq + b.freq)
        parent.set_left(a)
        parent.set_right(b)
    # else:
    #     parent = HuffmanNode(b.char, a.freq + b.freq)
    #     parent.set_left(a)
    #     parent.set_right(b)
    if a.char < b.char:
        parent.char = a.char
    else:
        parent.char = b.char
    return parent


def create_huff_tree(char_freq):
    """Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree"""
    node_list = []
    if char_freq == 256 * [0]:
        return HuffmanNode(0, 0)
    for index in range(len(char_freq)):
        if char_freq[index] != 0:
            node_list.append(HuffmanNode(index, char_freq[index]))
    node_list.sort()  # want to use my comes before method to check for ascii too

    index = 0
    while len(node_list) > 1:
        child1 = node_list.pop(0)
        child2 = node_list.pop(0)
        parent = combine(child1, child2)

        # add the node to the sorted list using the
        index2 = 0
        if len(node_list) != 0:
            while not comes_before(parent, node_list[index2]):
                index2 += 1
                if index2 == len(node_list):
                    break
        node_list.insert(index2, parent)
    return node_list[0]


def create_code(node):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the arrary, with the resulting Huffman code for that character stored at that location"""
    code_list = 256 * ['']
    string_path = ''
    return create_code_helper(node, code_list, string_path)


def create_code_helper(node, code_list, string_path):
    if node.left is None and node.right is None:
        code_list[node.char] = string_path

    if node.left:
        create_code_helper(node.left, code_list, string_path + '0')

    if node.right:
        create_code_helper(node.right, code_list, string_path + '1')
    return code_list


def create_header(freqs):
    """Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2" """
    header = ""
    freq = 0
    char = ''
    for i in range(len(freqs)):
        char = i
        freq = freqs[i]
        if not freq == 0:
            header += str(char) + ' ' + str(freq) + ' '
    return header[:-1]


def huffman_encode(in_file, out_file):
    """Takes input file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take note of special cases - empty file and file with only one unique character"""
    infile = open(in_file)
    outfile = open(out_file, 'w+')
    text_string = infile.read()
    # infile.close()
    code_list = create_code(create_huff_tree(cnt_freq(in_file)))
    if text_string != "":
        out_string = create_header(cnt_freq(in_file)) + '\n'
    else:
        out_string = ""
    for char in text_string:
        out_string += code_list[ord(char)]
    outfile.write(out_string)
    outfile.close()
    infile.close()


def parse_header(header_string): #recreates the frequency list from the header of the encoded file
    freq_list = [0] * 256
    head_list = header_string.split()

    for i in range(len(head_list)):
        if i % 2 == 0:
            index = head_list[i]
        else:
            freq_list[int(index)] = int(head_list[i])
    return freq_list
    
def huffman_decode(encoded_file, decode_file): #decoding file
    infile = open(encoded_file)
    freq_list = infile.readline().strip()
    code_string = infile.readline()
    outfile = open(decode_file, 'w') 
    # code_string = code_string[0:]
    
    infile.close()
    
    output_string = ''
    
    if freq_list == '': #case for an empty file 
        outfile.write('')
        outfile.close()
        return
        
    parent = create_huff_tree(parse_header(freq_list))
    node = create_huff_tree(parse_header(freq_list))
    
    if node.left == None and node.right == None: #case for a file with only one letter and no subsequent children from the parent node
        output_string = str(chr(node.char) * node.freq)
        outfile.write(output_string)
        outfile.close()
        return
    
    
    for char in code_string: #loop that traverses through the tree until it gets tot he leaf and then adds that to the output string
        if node.left == None and node.right == None:
            output_string += chr(node.char)
            node = parent
        if char == '1':
            node = node.right
        if char == '0':
            node = node.left
    output_string += chr(node.char)
            
    outfile.write(output_string)
    outfile.close()
    
    
    
    
    
    
    
