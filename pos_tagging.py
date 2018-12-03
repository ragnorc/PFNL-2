# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    nn_list = set([])
    nns_list = set([])
    with open("sentences.txt", "r") as f:
        for line in f:
            for w in line.split(" "):
                if re.match(".*\|NNS",w):
                    nns_list.add(w.replace("|NNS","").replace('\n', ''))
                elif re.match(".*\|(NN)",w):
                    nn_list.add(w.replace("|NN","").replace('\n', ''))
                

    return [w for w in nn_list if w in nns_list]

           

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    if s in unchanging_plurals_list:
       return s
    elif re.match(".*men",s):
        return (s[:-3] + "man")
    else: # Apply 3s Rules
       ret = ""
       if not re.match(".*(a|e|i|o|u|s|x|y|z|ch|sh)s", s): # Rule 1
         ret = s[:-1]
       elif re.match(".*(a|e|i|o|u)ys", s): # Rule 2
         ret = s[:-1]
       elif len(s) >= 5 and re.match(".*ies", s) and not re.match(".*(a|e|i|o|u)ies", s): # Rule 3
         ret = (s[:-3] + "y")
       elif re.match(".*ies", s) : # Rule 4
         ret = s[:-1]
       elif re.match(".*(o|x|ch|sh|ss|zz)es", s): # Rule 5
         ret = s[:-2]
       elif re.match(".*(se|ze)s", s) and not re.match(".*(sse|zze)s", s): # Rule 6
         ret = s[:-1]
       elif re.match(".*es",s) and not re.match(".*(i|o|s|x|z|ch|sh)es",s):
         ret = s[:-1]
  #TODO Also check in in Brown Corpus?
    return ret

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    #complete_lexicon = lx.getAll("P")+lx.getAll("A")+lx.getAll("Ns")+lx.getAll("Np")+lx.getAll("Is")+lx.getAll("Ip")+lx.getAll("Ts")+lx.getAll("Tp")+lx.getAll("BEs")+lx.getAll("BEp")+lx.getAll("DOs")+lx.getAll("DOp")+lx.getAll("AR")+lx.getAll("AND")+lx.getAll("WHO")+lx.getAll("WHICH")+lx.getAll("?") 
    tag_set = set([])
    if wd in lx.getAll("P"):
      tag_set.add("P") 
    if wd in lx.getAll("A"):
      tag_set.add("A")
    if wd in lx.getAll("N"):
      tag_set.add("Ns")
    if noun_stem(wd) in lx.getAll("N") or wd in unchanging_plurals_list or wd in lx.getAll("Np"): # last check in case the lexicon stores plurals
      tag_set.add("Np")
    if wd in lx.getAll("I"):
      tag_set.add("Ip")
    if verb_stem(wd) in lx.getAll("I"):
      tag_set.add("Is")
    if wd in lx.getAll("T"):
      tag_set.add("Tp")
    if verb_stem(wd) in lx.getAll("T") or wd in lx.getAll("Ts"): # last check in case the lexicon stores plurals
      tag_set.add("Ts")
    for t in function_words_tags:
        if wd == t[0]:
            tag_set.add(t[1])

    return list(tag_set)
    #return list(set([t[1] for t in complete_lexicon if t[0]==wd or t[0] == verb_stem(wd) or t[0] == noun_stem(wd)]))

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.