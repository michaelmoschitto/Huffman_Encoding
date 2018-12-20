import unittest
import filecmp
import subprocess
from huffman import *

class TestList(unittest.TestCase):
    def test_cnt_freq(self):
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)
        # freqlist = cnt_freq('blank.txt')
        # self.assertListEqual(freqlist, [])
        with self.assertRaises(FileNotFoundError):
          cnt_freq('myfakefile.txt')
        freqlist = cnt_freq("blank.txt")
        anslist = [0,0,0,0,0,0]
        self.assertListEqual(freqlist[97:103], anslist)
    
    def test_comes_before(self):
        a = HuffmanNode('a', 10)
        b = HuffmanNode('b', 11)
        self.assertTrue(comes_before(a,b))
        a = None
        b = HuffmanNode('b', 11)
        self.assertFalse(comes_before(a,b))
        a = HuffmanNode('c', 11)
        b = HuffmanNode('b', 11)
        self.assertFalse(comes_before(a,b))
        a = HuffmanNode('c', 11)
        b = HuffmanNode('b', 10)
        self.assertFalse(comes_before(a,b))
    
    def test_create_huff_tree_for_file2(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
    
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
    
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)
    
    def test_create_huff_tree_for_file1(self):
        freqlist = cnt_freq("file1.txt")
    
        hufftree = create_huff_tree(freqlist)
    
        self.assertEqual(hufftree.freq, 13)
        self.assertEqual(hufftree.char, 32)
        left = hufftree.left
        self.assertEqual(left.freq, 6)
        self.assertEqual(left.char, 32)
        right = hufftree.right
        self.assertEqual(right.freq, 7)
        self.assertEqual(right.char, 97) #comes back as 100
    
        self.assertEqual(right.left.freq, 3) #this should be 3b
        self.assertEqual(right.left.char, 99) #returns 100
    
        self.assertEqual(right.right.freq, 4)
        self.assertEqual(right.right.char, 97)
    
        self.assertEqual(right.left.right.char, 99) #this should be c
        self.assertEqual(right.left.right.freq, 2) #this should be 2
    
        self.assertEqual(right.left.left.freq, 1)  #1,b
        self.assertEqual(right.left.left.char, 100)
    
    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
    
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")
        freqlist = cnt_freq('blank.txt')
        self.assertEqual(create_header(freqlist), "")
        freqlist = cnt_freq('only_b.txt')
        self.assertEqual(create_header(freqlist), "98 15")
        freqlist = cnt_freq('declaration.txt')
        self.assertEqual(create_header(freqlist), "10 166 32 1225 38 1 39 1 44 109 45 3 46 36 49 1 52 1 54 1 55 2 58 10 59 10 65 22 66 7 67 19 68 5 69 3 70 17 71 15 72 24 73 8 74 5 75 1 76 15 77 3 78 8 79 6 80 23 82 9 83 23 84 15 85 3 87 13 97 466 98 88 99 171 100 253 101 875 102 169 103 116 104 331 105 451 106 12 107 13 108 216 109 144 110 487 111 518 112 116 113 6 114 420 115 460 116 640 117 211 118 74 119 84 120 9 121 82 122 4")
    
    
    def test_create_code(self):
        freqlist = cnt_freq("file1.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
    
        self.assertEqual(codes[ord(' ')], '00')
        self.assertEqual(codes[ord('a')], '11')
        self.assertEqual(codes[ord('b')], '01')
        self.assertEqual(codes[ord('d')], '100')
        self.assertEqual(codes[ord('c')], '101')
    
        freqlist = cnt_freq("blank.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        for i in range(len(codes)):
            self.assertEqual(codes[i], "")
    
    def test_01_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell = True)
        self.assertEqual(err, 0)
    
        huffman_encode("file2.txt", "file2_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file2_out.txt file2_soln.txt", shell = True)
        self.assertEqual(err, 0)
    
        huffman_encode("declaration.txt", "declaration_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb declaration_out.txt declaration_soln.txt", shell = True)
        self.assertEqual(err, 0)
    
    
        huffman_encode("blank.txt", "blank_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb blank_out.txt blank_soln.txt", shell = True)
        self.assertEqual(err, 0)
    
        huffman_encode("only_b.txt", "only_b_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb only_b_out.txt only_b_soln.txt", shell = True)
        self.assertEqual(err, 0)
    
        huffman_encode("only_one_letter.txt", "one_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb one_out.txt only_one_soln.txt", shell = True)
        self.assertEqual(err, 0)
    
        with self.assertRaises(FileNotFoundError):
            huffman_encode("myfakefile.txt", "blank_out.txt")
    
        # huffman_encode("AliceInWonderLand.txt", "blank_out.txt")
        # # capture errors by running 'diff' on your encoded file with a *known* solution file
        # err = subprocess.call("diff -wb blank_out.txt alice_soln.txt", shell = True)
        # self.assertEqual(err, 0)
        # 
        # huffman_encode("AliceInWonderLand.txt", "blank_out.txt")
        # # capture errors by running 'diff' on your encoded file with a *known* solution file
        # err = subprocess.call("diff -wb blank_out.txt alice_soln.txt", shell = True)
        # self.assertEqual(err, 0)
        
    def test_parse_header(self):
        infile = open('file2_soln.txt')
        freqlist = cnt_freq('file2.txt')
        header_string = infile.readline().strip()
        self.assertListEqual(freqlist, parse_header(header_string))
        infile.close()
    
    def test_decode(self):
        
        with self.assertRaises(FileNotFoundError):
            huffman_decode('myfakefile.txt', 'decoded.txt')
            
        huffman_decode('multiline_soln.txt', 'decoded.txt')
        err = subprocess.call("diff -wb decoded.txt multiline.txt", shell = True)
        self.assertEqual(err, 0)
        
        huffman_decode('file1_soln.txt', 'decoded.txt')
        err = subprocess.call("diff -wb decoded.txt file1.txt", shell = True)
        self.assertEqual(err, 0)
        
        huffman_decode('file2_soln.txt', 'decoded.txt')
        err = subprocess.call("diff -wb decoded.txt file2.txt", shell = True)
        self.assertEqual(err, 0)
        
        huffman_decode('blank_soln.txt', 'decoded.txt')
        err = subprocess.call("diff -wb decoded.txt blank.txt", shell = True)
        self.assertEqual(err, 0)
        
        huffman_decode('only_b_soln.txt', 'decoded.txt')
        err = subprocess.call("diff -wb decoded.txt only_b.txt", shell = True)
        self.assertEqual(err, 0)

        huffman_decode('only_one_soln.txt', 'decoded.txt')
        err = subprocess.call("diff -wb decoded.txt only_one_letter.txt", shell = True)
        self.assertEqual(err, 0)
        
        huffman_decode('declaration_soln.txt', 'decoded.txt')
        err = subprocess.call("diff -wb decoded.txt declaration.txt", shell = True)
        self.assertEqual(err, 0)
        
    
    
    # def test_war_and_peace(self):
    #     huffman_encode('war_and_peace.txt', 'war_and_peace_out.txt')
    #     huffman_decode('war_and_peace_out.txt', 'decoded.txt')
    #     err = subprocess.call("diff -wb decoded.txt war_and_peace.txt", shell = True)
    #     self.assertEqual(err, 0)
        
        
        
        
        
        
        
if __name__ == '__main__':
   unittest.main()
