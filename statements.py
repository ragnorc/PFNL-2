# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    lexList = set([])
    def add(self, stem, cat):
        self.lexList.add((stem, cat.upper()))
    def getAll(self, cat):
        return [v[0] for v in self.lexList if v[1] == cat]


class FactBase:
    """stores unary and binary relational facts"""
    factList = []
    def addUnary(self, pred, e1):
        add(self.factList, (pred, e1))
    def addBinary(self, pred, e1, e2):
        add(self.factList, (pred, e1,e2))
    def queryUnary(self, pred, e1):
        return (pred, e1) in self.factList
    def queryBinary(self, pred, e1, e2):
        return (pred, e1, e2) in self.factList
    # add code here

import re
from nltk.corpus import brown 

print('Loading Brown Corpus. Please wait ...')
brown_vb = set([])
brown_vbz = set([])
for v in brown.tagged_words():
    if v[1] == "VB":
        brown_vb.add(v[0])
    elif v[1] == "VBZ":
        brown_vbz.add(v[0])
print('Brown Corpus successfully loaded.')

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    ret = ""
    exceptionsDict = {
        "has": "have",
        "does" : "do"
    } # Should exceptions be ignored? https://piazza.com/class/jkuzor9eypxov?cid=240
    if not re.match(".*(a|e|i|o|u|s|x|y|z|ch|sh)s", s): # Rule 1
      print("Rule 1")
      ret = s[:-1]
    elif re.match(".*(a|e|i|o|u)ys", s): # Rule 2
      print("Rule 2")
      ret = s[:-1]
    elif len(s) >= 5 and re.match(".*ies", s) and not re.match(".*(a|e|i|o|u)ies", s): # Rule 3
      print("Rule 3")
      ret = (s[:-3] + "y")
    elif re.match(".*ies", s) : # Rule 4
      print("Rule 4")
      ret = s[:-1]
    elif re.match(".*(o|x|ch|sh|ss|zz)es", s): # Rule 5
      print("Rule 5")
      ret = s[:-2]
    elif re.match(".*(se|ze)s", s) and not re.match(".*(sse|zze)s", s): # Rule 6
      print("Rule 6")
      ret = s[:-1]
    elif re.match(".*es",s) and not re.match(".*(i|o|s|x|z|ch|sh)es",s):
      print("Rule 8")
      ret = s[:-1]
    else:
        pass
    if not s in brown_vbz and not ret in brown_vb:
      print("Not in brown corpus")
      ret = ""
    if s in exceptionsDict:
       ret = exceptionsDict[s]
    return ret


def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
# End of PART A.

