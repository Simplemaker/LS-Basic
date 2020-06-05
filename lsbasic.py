import sys

chars = 'abcdefghijklmnopqrstuvwxyz'

def toss(index):
  print('Index: '+str(index))
  return

def accessVar(var, varlist, varindex):
  if var in varindex:
    return(varlist[varindex.index(var)])
  else:
    print('Undefined variable')
    toss(index)
    return 0

def charVal(letter):
  letter=letter.lower()
  if letter in chars:
    return chars.index(letter)+1
  else:
    return 0

def score(word):
  try:
    s=int(word)
  except:
    s = 0
    for c in word:
      s+=charVal(c)
  return s

def fileToLines(filename):
  f=open(filename)
  out = stringToLines(f.read())
  f.close()
  return out

def stringToLines(string):
  lines = string.replace('\n',' ').split(' ')
  out = []
  for line in lines: #This loop eliminates double spaces and " \n" situations
    if score(line)!=0:
      out.append(score(line))
  return out

def labelSearch(numlist, label):
  mode='findLabel'
  for i in range(len(numlist)):
    c = numlist[i]
    if mode=='findLabel':
      if c==26:
        mode='labelCheck'
      elif c in [15,56,74,78,80,77]:
        mode='skip1'
      elif c == 37:
        mode='skipDone'
    elif mode=='skip1':
      mode='findLabel'
    elif mode=='skipDone':
      if c==38:
        mode='findLabel'
    elif mode=='labelCheck':
      if c==label:
        return i
      else:
        mode='findLabel'
  return -1

def executeNum(numlist, debug=False):
  index = 0
  stack = [0,0,0,0]
  varlist = [0,1,10]
  varindex =[64,34,39]
  mode='getCommand'
  running = True
  while running:
    c = numlist[index]
    if(debug):
      print(mode) #Debug script
      print(c) 
    if mode=='getCommand':
      if c==80: #input
        mode='storeInput'
      if c==23: #end
        running=False
      if c==77: #print
        mode='printVarAsNum'
      if c==107:#printchar
        mode='printVarAsChar'
      if c==37: #let
        mode='getArithOutputVar'
      if c==57: #goto
        mode='gotoLabel'
      if c==15: #if command
        mode='getCompVar'
    elif mode=='storeInput':
      if c in varindex:
        varlist[varindex.index(c)] = int(input('? '))
      else:
        varindex.append(c)
        varlist.append(int(input('? ')))
      mode='getCommand'
    elif mode=='printVarAsNum':
      print(accessVar(c, varlist, varindex))
      mode = 'getCommand'
    elif mode=='printVarAsChar':
      accessed = accessVar(c, varlist, varindex)
      sys.stdout.write(chr(accessed))
      mode = 'getCommand'
    elif mode=='getArithOutputVar':
      outputVar = c
      mode='getEqual'
    elif mode=='getEqual':
      if c==56:
        mode='arith'
      else:
        print('Expected equal sign')
        toss(index)
    elif mode=='arith':
      if c==38: #called when "done" is reached
        if outputVar in varindex: #update old variables
          varlist[varindex.index(outputVar)] = stack[0]
        else: #if a variable is new
          varindex.append(outputVar)
          varlist.append(stack[0])
        mode='getCommand'
      elif c==68: #plus
        stack[0] = stack[0]+stack[1]
        stack[1] = stack[2]
        stack[2] = stack[3]
        stack[3] = 0
      elif c==76: #minus
        stack[0] = stack[1]-stack[0]
        stack[1] = stack[2]
        stack[2] = stack[3]
        stack[3] = 0
      elif c==66: #times
        stack[0] = stack[1]*stack[0]
        stack[1] = stack[2]
        stack[2] = stack[3]
        stack[3] = 0
      elif c==53: #divide
        stack[0] = int(stack[1]/stack[0])
        stack[1] = stack[2]
        stack[2] = stack[3]
        stack[3] = 0
      elif c==32: #modulo
        stack[0] = stack[1]%stack[0]
        stack[1] = stack[2]
        stack[2] = stack[3]
        stack[3] = 0              
      else: #if a value is not a recognized command it is considered a variable
        stack[3] = stack[2]
        stack[2] = stack[1]
        stack[1] = stack[0]
        stack[0] = accessVar(c, varlist, varindex)
    elif mode=='gotoLabel':
      i2 = labelSearch(numlist, c)
      if i2 == -1:
        running = False
        print('Undefined label called')
        toss(index)
      else:
        index=i2
        mode='getCommand'
    elif mode=='getCompVar':
      compvar1 = accessVar(c, varlist, varindex)
      mode='getComparator'
    elif mode=='getComparator':
      if c == 56:
        mode='testEqual'
      elif c==74:
        mode='testGreater' 
      elif c==78:
        mode='testLesser'
      else:
        print('Invalid comparator')
        toss(index)
    elif mode in ['testEqual','testGreater','testLesser']:
      compvar2 = accessVar(c, varlist, varindex)
      if ((mode=='testEqual' and compvar1 == compvar2) or
       (mode=='testGreater' and compvar1 > compvar2) or
       (mode=='testLesser' and compvar1 < compvar2)):
        mode = 'gotoLabel' #if the condition is met, treat the if statement as a goto
      else:
        mode ='skip'
    elif mode == 'skip':
      mode='getCommand'
       #skip does not execute, but will resume execution next step
    index+=1
    if index>=len(numlist):
      running=False

if __name__ == "__main__":
  if len(sys.argv) == 2:
    p = fileToLines(sys.argv[1])
    executeNum(p)
  else:
    print("run this script followed by the filename to be executed.")
    print("python lsbasic.py script.bas")