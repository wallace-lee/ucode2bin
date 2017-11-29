#!/bin/python

import sys, getopt
import binascii
import re

def show_usage():
    print '*************************************************************'
    print '*   This utility convert Intel microcode in text (*.txt)    *'
    print '*         format to binary equivalent (*.bin)               *'
    print '*************************************************************'    
    print sys.argv[0],'-i <inputfile> -o <outputfile>'
def main(argv):
    inputfile = ''
    outputfile = '<stdout>'
    has_i = False
    
    try:
       opts, args = getopt.getopt(argv, "hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
       print sys.argv[0],'-i <inputfile> -o <outputfile>'
       sys.exit(2)
       
    for opt, arg in opts:
       if opt == '-h':
          show_usage()
          sys.exit()
       elif opt in ("-i", "--ifile"):
          inputfile = arg
          has_i = True
       elif opt in ("-o", "--ofile"):
          outputfile = arg
          
    sys.stderr.write("Input file: {:s}\n".format(inputfile))
    sys.stderr.write("Output file: {:s}\n".format(outputfile))

    if(has_i == False):
       print 'Usage:'
       show_usage()
       print '\t*Input file is required.'
       sys.exit(3)

    with open(inputfile, 'rb') as f:
       content = f.read()
       f.close()
    
    lines = re.findall('[^\r\n\Z]+', content)
    bytes_string = ""

    ll=len(lines)
    
    for index in range(0, ll) :
       match=re.search('^;.*?', lines[index])
       if not match:
          c=lines[index].split(' ')
          d=re.findall('0([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})h', c[1])
          bytes_string += '\\x'+d[0][3]+'\\x'+d[0][2]+'\\x'+d[0][1]+'\\x'+d[0][0]
    
    if(outputfile == '<stdout>'):
       print binascii.a2b_hex(bytes_string.replace('\\x',''))
    else:
       with open(outputfile, 'wb') as f:
          f.write(binascii.a2b_hex(bytes_string.replace('\\x','')))
          f.close()


if __name__ == "__main__":
     main(sys.argv[1:])
