import numpy as np
import base64
import sys
import argparse
 

class Rotor():
    perms = []
    def __init__(self, alphabet, perms, turnover_position = 'R', position = 'A'):
        self.alphabet = alphabet
        self.perms = [c for c in perms]
        self.position = position
        self.turnover_position = turnover_position
        
    def step(self): 
        self.position = self.alphabet[(self.alphabet.index(self.position) + 1) % len(self.alphabet)]
        return self.turnover_position == self.position
    
    def encrypt_forward(self, c):
        return self.perms[self.alphabet.index(c)]
    
    def encrypt_backward(self, c):
        return self.alphabet[self.perms.index(c)]
    
class Reflector():
    def __init__(self, pairs):
        self.pairs = pairs
    
    def reflect(self, c):
        return self.pairs[c]
    

class Enigma():
    rotors = []
    reflector = None
    changeBoard = {}
    double_step = False
    
    
    def __init__(self, alphabet, rotors, reflector, changeBoard):
        self.rotors = [Rotor(alphabet, rotor[0], rotor[1], rotor[2]) for rotor in rotors]
        self.reflector = Reflector(reflector)
        self.alphabet = alphabet
        for pair in changeBoard:
            self.changeBoard[pair[0]], self.changeBoard[pair[1]] = pair[1], pair[0]

    
    def encrypt_char(self, c):
        c = self.changeBoard[c] if c in self.changeBoard else c
        for i, rotor in enumerate(self.rotors[::-1]):
            if i is 0:
                c = self.alphabet[(self.alphabet.index(self.rotors[::-1][0].position) + self.alphabet.index(c)) % len(self.alphabet)]
                c = rotor.encrypt_forward(c)
            else:
                difference = self.alphabet.index(self.rotors[::-1][i].position) - self.alphabet.index(self.rotors[::-1][i-1].position) 
                c = rotor.encrypt_forward(self.alphabet[(self.alphabet.index(c) + difference) % len(self.alphabet)])

        c = self.alphabet[(self.alphabet.index(c) - self.alphabet.index(self.rotors[::-1][-1].position)) % len(self.alphabet)]
        c = self.reflector.reflect(c)
        c = self.alphabet[(self.alphabet.index(c) + self.alphabet.index(self.rotors[::-1][-1].position)) % len(self.alphabet)]

        for i, rotor in enumerate(self.rotors):
            if i is 0:
                c = rotor.encrypt_backward(c)
            else:
                difference = self.alphabet.index(self.rotors[i].position) - self.alphabet.index(self.rotors[i-1].position)
                c = rotor.encrypt_backward(self.alphabet[(self.alphabet.index(c) + difference) % len(self.alphabet)])
        c = self.alphabet[(self.alphabet.index(c) - self.alphabet.index(self.rotors[::-1][0].position)) % len(self.alphabet)]
        c = self.changeBoard[c] if c in self.changeBoard else c
        return c
    

    def step(self):
        if self.rotors[2].step():
            if self.rotors[1].step():        
                self.rotors[0].step()    
                
    def encrypt(self, s):
        out = ''
        for c in s:
            self.step()
            out += self.encrypt_char(c)
        return out
        
        
    
def generate_reflector(alphabet):
    resDict = {}
    while(alphabet != ''):
        lenAlphabet = len(alphabet)
        if (lenAlphabet == 1):
            resDict[alphabet[0]] = alphabet[0]
            break
        first, second = 0, 0
        while(first == second):
            first = np.random.randint(0, lenAlphabet)
            second = np.random.randint(0, lenAlphabet)
        a1 = alphabet[first]
        a2 = alphabet[second]

        resDict[a1], resDict[a2] = a2, a1
        
        alphabet = alphabet.replace(a2, '')
        alphabet = alphabet.replace(a1, '')
    return resDict


# reflDict = generate_reflector(alphabet)    
# print(reflDict)

def encode_decode_file(filename, mode='e'):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    rotors=[('ESOVPZJAYQUIRHXL16789+/NFTGKDCMWBabcdefghi2345jklmnouvwxyzpqrst0', 'J', 'G'),
            ('AJ56U89+/XBLHWTMCrsEaDKSIRbghiFVO23jklmnopqyzcdef01tuvwxQGZNPY47', 'A', '+'),
            ('VZYghoUPSDNHlmn6789+/LXAWECK0123abcdefBRGITpqrstMJQOFuvwxyz45ijk', 'Z', 'b')]
    reflector = {'Z': '+', '+': 'Z', '4': 'z', 'z': '4', '9': 'S', 'S': '9', 'u': '7', '7': 'u', 'L': '6', '6': 'L', 'h': 'r', 'r': 'h', 'm': 'T', 'T': 'm', 'D': 'H', 'H': 'D', 'Y': 'f', 'f': 'Y', 'K': 'n', 'n': 'K', 'R': 'W', 'W': 'R', 'x': 'a', 'a': 'x', 'U': 'v', 'v': 'U', 'e': 'P', 'P': 'e', 'c': 'o', 'o': 'c', 'g': 'j', 'j': 'g', 'B': 'G', 'G': 'B', 'E': '1', '1': 'E', 'l': 'X', 'X': 'l', 'p': 'Q', 'Q': 'p', 'y': 'J', 'J': 'y', '0': 'M', 'M': '0', 'b': 'i', 'i': 'b', 'k': 's', 's': 'k', 'V': 'q', 'q': 'V', 'O': 'I', 'I': 'O', 'F': '5', '5': 'F', 'd': 'A', 'A': 'd', 'N': '8', '8': 'N', 't': '/', '/': 't', '3': 'w', 'w': '3', 'C': '2', '2': 'C'}
    changeBoard = [('a', 'Z'), ('f', '5'), ('I', 'S'), ('K', 'C'), ('r', 'l'), ('T', 'M'), ('P', 'V'), ('H', 'Y'), ('F', 'W'), ('B', 'J')]

    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    encoded_string = str(encoded_string)[2:-1]
    enigma = Enigma(alphabet, rotors, reflector, changeBoard)
    out  = enigma.encrypt(encoded_string)
    if (mode == 'e'):
        with open('encode_' + filename, "wb") as fh:
            fh.write(base64.decodebytes(out.encode('ascii')))
    if (mode == 'd'):
        with open("decode_" + filename, "wb") as fh:
            fh.write(base64.decodebytes(out.encode('ascii')))


 
def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-e', '--filenameToEncode', nargs='+')
    parser.add_argument ('-d', '--filenameToDecode', nargs='+')
    return parser
 
 
if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    if (namespace.filenameToEncode is not None):
        for filename in namespace.filenameToEncode:
            encode_decode_file(filename, 'e')
    if (namespace.filenameToDecode is not None):
        for filename in namespace.filenameToDecode:
            encode_decode_file(filename, 'd')


