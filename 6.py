import re


# txtorig = u'§B3 £pops£ Robot Pops§! $CLASS|Y$ $LEADER_Y$ gained experience from §H5 Pops§! Welcome, [root.GetBloodCourtRulerTitle].\n\nI am VIR, a prototype synthetic intelligence §H[Third_party.GetName]§!'
txtorig = u'B3 pops Robot Pops! $CLASS|Y$ $LEADER_Y$ gained experience from H5 Pops! Welcome, [root.GetTitle].\n\nI am VIR, a prototype synthetic intelligence H[Third_party.GetName]!'

# temporarily replace variables of format "%(example_name)s" with "__n__" to
#  protect them during translate()
VAR1 = re.compile(r'((\$)([\[\]\.\|\w]+)(\$))')
VAR2 = re.compile(r'((\[)([\.\|\w]+)(\]))')
VAR3 = re.compile(r'((\§)([\!\w]))')
VAR4 = re.compile(r'((\£)([\w]+)(\£))')
REPL = re.compile(r'__(\d+)__')

varlist = []

def replace(matchobj):
  varlist.append(matchobj.group())
  return "__%d__" %(len(varlist)-1)

def restore(matchobj):
  return varlist[int(matchobj.group(1))]

def reset_varlist():
    global varlist
    varlist = []

print(txtorig.encode("utf-8"))
txtorig = VAR1.sub(replace, txtorig)
txtorig = VAR2.sub(replace, txtorig)
txtorig = VAR3.sub(replace, txtorig)
txtorig = VAR4.sub(replace, txtorig)
print(txtorig.encode("utf-8"))
txttrans = REPL.sub(restore, txtorig)
print(txttrans.encode("utf-8"))
print(varlist)