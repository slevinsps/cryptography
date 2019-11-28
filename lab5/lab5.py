# from Crypto.PublicKey import RSA
from hashlib import sha256
import rsa as RSA
# from Crypto.Signature import pkcs1_15
import os

def readFromFile(filename):
    fileToRead = open(filename, "rb")
    data = fileToRead.read()
    fileToRead.close()
    return data

def writeToFile(data, filename):
    fileToWrite = open(filename, "wb")
    fileToWrite.write(data)
    fileToWrite.close()

def main():
    mode = int(input("Enter mode(1 - encode, 2 - decode) :"))
    if mode == 1:

        source = input("Enter file name: ")
        data = readFromFile(source)

        h1 = sha256()
        h1.update(data)
        hash = [i for i in h1.digest()]

        rsa = RSA.RSA()
        public, private = rsa.encrypt('signature_' + source, hash)
    else:
        source = input("Enter file name: ")
        signature = input("Enter signature name: ")
        pub_exp = int(input("Enter public exponent: "))
        pub_module = int(input("Enter public module: "))
        public = (pub_exp, pub_module)
        data = readFromFile(source)
        h1 = sha256()
        h1.update(data)
        hash1 = [i for i in h1.digest()]
        rsa = RSA.RSA()
        hash2 = rsa.decrypt(signature, public)
        if hash1 == hash2:
            print("Verified")
        else:
            print("Not verified")


if __name__ == "__main__":
    main()