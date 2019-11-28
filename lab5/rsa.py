import random
import math
import argparse
import sys
import os
class RSA():
  def __init__(self, lenOfkey = 512):
    self.lenOfKey = lenOfkey

  def rabinMiller(self, n):
      s = n-1
      t = 0
      while s&1 == 0:
          s = s//2
          t +=1
      k = 0
      while k<128:
          a = random.randrange(2,n-1)
          v = pow(a,s,n)
          if v != 1:
              i=0
              while v != (n-1):
                  if i == t-1:
                      return False
                  else:
                      i = i+1
                      v = pow(v,2,n)
          k+=2
      return True

  def isPrime(self, n):
      lowPrimes =   [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
                    ,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
                    ,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
                    ,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
                    ,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
                    ,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
                    ,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
                    ,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
                    ,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
                    ,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]
      if (n >= 3):
          if (n&1 != 0):
              for p in lowPrimes:
                  if (n == p):
                      return True
                  if (n % p == 0):
                      return False
              return self.rabinMiller(n)
      return False

  def generateLargePrime(self, k):
      r=100*(math.log(k,2)+1) 
      r_ = r
      while r>0:
          n = random.randrange(2**(k-1),2**(k))
          r-=1
          if self.isPrime(n) == True:
              return n
      return -1

  def gcd(self, a, b):
      while b != 0:
          a, b = b, a % b
      return a

  def egcd(self, a, b):
      x,y, u,v = 0,1, 1,0
      while a != 0:
          q, r = b//a, b%a
          m, n = x-u*q, y-v*q
          b,a, x,y, u,v = a,r, u,v, m,n
      gcd = b
      return gcd, x, y
      
  def generate_keypair(self, p, q):
      n = p * q
      phi = (p-1) * (q-1)

      e = random.randrange(1, phi)

      #Use Euclid's Algorithm to verify that e and phi(n) are comprime
      g = self.gcd(e, phi)
      while g != 1:
          e = random.randrange(1, phi)
          g = self.gcd(e, phi)

      #Use Extended Euclid's Algorithm to generate the private key
      _, d, _ = self.egcd(e, phi)
      if d < 0:
        d = phi + d
      
      return ((e, n), (d, n))

  def encrypt(self, filename, data):

      p = -1
      while p == -1:
        p = self.generateLargePrime(self.lenOfKey)
      q = -1
      while q == -1:
        q = self.generateLargePrime(self.lenOfKey)

      public, private = self.generate_keypair(p, q)
      print("Public key is ", public ," Private key is ", private)
      # with open(input_path, 'rb') as f:
      #   data = f.read()
      crypted_data = []
      temp = []
      for byte in data:
        temp.append(byte)

      key, n = private
      encrypted_msg = [str(pow(char, key, n)) for char in temp]
      encrypted_msg = ';'.join(encrypted_msg)
      with open(filename, 'w') as ff:
        ff.write(encrypted_msg)
      print('All encrypt')
      # f.close()
      ff.close()

      return public, private
      

  def decrypt(self, filename, private):
      input_path = os.path.abspath(filename)
      if not os.path.isfile(input_path):
        print('This is not a file')
        exit()
  
      with open(input_path, 'r') as f:
        data = f.read()
      temp = [int(i) for i in data.split(';')]
      


      key, n = private
      decrypted_data = [pow(char, key, n) for char in temp]

      # out_path = os.path.join(os.path.dirname(input_path) , 'dec_' + os.path.basename(input_path))

      # with open(out_path, 'wb') as ff:
      #   ff.write(bytes(decrypted_data))
      # print('All decrypt')
      # f.close()
      # ff.close()
      return decrypted_data

    