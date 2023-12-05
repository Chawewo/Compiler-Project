## ------------------------------------------------------------
## Group names: David Trujillo, Gerardo Robledo, Siddharth Vasu
## Final Project
## Due date: 12/07/23
## Purpose: This is a compiler program that tokenizes an input
##          text file into readable pseudocode, checks for
##          errors, and translates the pseudocode into Python
## ------------------------------------------------------------
import time

#Function to tokenize the input file
def tokenize(fileIn, fileOut):
  tokens = []
  comment = False
  
  # Reads input file "finalv1.txt"
  input_file = open(fileIn, 'r', encoding="utf-8")

  for line in input_file:
    # Tokenizes each line by spaces
    text = line.split()

    for i in range(len(text)):
      # Excludes comments
      if text[i] == "(*":
        comment = True

      # Adds tokens separated by one space
      if not comment:
        tokens.append(text[i] + " ")
        #Adds newline if semicolon is reached
        if (";" in text[i]):
          tokens.append("\n")

      # Continues once the comment ends
      if text[i] == "*)":
        comment = False

  input_file.close()

  output_file = open(fileOut, 'w', encoding="utf-8")

  # Writes tokens to output file "finalf23.txt"
  for i in range(len(tokens)):
    output_file.write(tokens[i])

  output_file.close()


# Function to parse the code
def parse(file):
  input_file = open(file, 'r', encoding="utf-8")
  # Initialize variables to keep track of reserved word tokens
  #reservedTokens = ["program","var","begin","end.","integer","write"]
  programPass = False
  varPass = False
  beginPass = False
  endPass = False  ## Dont think we need this but just incase
  integerPass = False
  writePass = False  ## This one I think has edge cases
  # currentReservedToken = 0 ## We will start at program and then increment *TBD may not need *
  # Puts all of the code into a list
  code = []
  reserved = [
      'program', ';', 'var', 'begin', 'end.', ':', ',', 'integer', 'write',
      '(', ')', '"value=",', '=', '+', '-', '*', '/', '0', '1', '2', '3', '4',
      '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'f', 'w'
  ]
  for line in input_file:
    text = line.split()
    for i in range(len(text)):
      # Begin checks to detect errors
      if text[i] == "program":  ## we have started the program
        programPass = True
      if text[i] == "var":
        if not programPass:
          print("Error: Program is expected (if program is missing or spelled wrong)")
          exit(1)
        else:
          varPass = True
      if text[i] == "begin":
        if not varPass:
          print( "Error: var is expected (if program is missing or spelled wrong)")
          exit(1)
        if not programPass:
          print("Error: program is expected (if program is missing or spelled wrong)")
        else:
          beginPass = True
      if text[i] == "end.":
        if not beginPass:
          print("Error: Begin is expected (if program is missing or spelled wrong)")
          exit(1)
        if not varPass:
          print("Error: var is expected (if program is missing or spelled wrong)")
          exit(1)
        if not programPass:
          print("Error: Program is expected (if program is missing or spelled wrong)")
          exit(1)
        else:
         endPass = True  # Dont think we need this
      # End checks to detect errors
      # print(str(beginPass) + " we have passed begin pass")

      if (text[i] in reserved):
        code.append(text[i])
      else:
        for n in text[i]:
          code.append(n)

  input_file.close()
  ## print(code)

  # Parses only if the reserved words are not missing
  if endPass:
    # Predictive parsing table 
    # DO NOTE THAT THE FIRST TEST WILL BE WITHOUT SPACING IN STRINGS SO E:T;, IF DOES NOT WORK TRY WITH SPACEs
    table = {
      'P': {'program': 'program I; var D begin S end.'},
      'I': {chr(i): 'LO' for i in range(ord('a'), ord('z') + 1)}, #This maps every letter in alphabet to 'LO'
      'O': {chr(i): 'LO' for i in range(ord('a'), ord('z') + 1)} | {str(i): 'FO' for i in range(10)} | {';': '', ':': '', ',': '', ')': '', '=': '', '+': '', '-': '', '*': '', '/': ''},
      'D': {chr(i): 'E : T ;' for i in range(ord('a'), ord('z') + 1)},
      'E': {chr(i): 'IK' for i in range(ord('a'), ord('z') + 1)},
      'T': {'integer':'integer'},
      'S': {chr(i): 'AQ' for i in range(ord('a'), ord('z') + 1)} | {'write':'AQ'},
      'A': {chr(i): 'G' for i in range(ord('a'), ord('z') + 1)} | {'write':'W'},
      'W': {'write': 'write(RI);' }, #Check this one later
      'R': {chr(i): '' for i in range(ord('a'), ord('z') + 1)} | {'value=':'"value=",', },
      'G': {chr(i): 'I=X;' for i in range(ord('a'), ord('z') + 1)},
      'X': {str(i): 'MH' for i in range(10)} | {chr(i): 'MH' for i in range(ord('a'), ord('z') + 1)} | {'+':'MH', '-': 'MH', '(': 'MH'},
      'M': {str(i): 'CJ' for i in range(10)} | {chr(i): 'CJ' for i in range(ord('a'), ord('z') + 1)} | {'-':'CJ', '+': 'CJ', '(': 'CJ'},
      'C': {str(i): 'N' for i in range(10)} | {chr(i): 'I' for i in range(ord('a'), ord('z') + 1)} | {'-':'N', '+': 'N', '(': '(X)'},
      'N': {str(i): 'BFZ' for i in range(10)} | {'-':'BFZ', '+': 'BFZ'},
      'B': {str(i): '' for i in range(10)} | {'+':'+', '-':'-'},
      'F': {'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9'},
      'L': {chr(i): chr(i) for i in range(ord('a'), ord('z') + 1)},
      'Z': {str(i): 'F' for i in range(10)} | {';': '', ')':'', '+':'', '-':'', '*':'', '/':''},
      'H': {';': '', ')':'', '+':'+MH', '-':'-MH'},
      'J': {';': '', ')':'', '+':'', '-':'', '*':'*CJ', '/':'/CJ'},
      'K': {':':'', ',':',E'},
      'Q': {chr(i): 'S' for i in range(ord('a'), ord('z') + 1)} | {'end.':'', 'write':'S',}
    }
  stack = ["P"]
  while len(stack) > 0:
    topStack = stack[-1]
    if topStack in table:
      if 
tokenize("finalv1.txt", "finalf23.txt")
parse("finalf23.txt")
