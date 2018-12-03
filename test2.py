from nltk.sem.logic import *
from nltk.sem.logic import LogicParser
from semantics import *

exceptionMessage="""
You can now interact with the system by using the 'run' method
of the 'tester' object, eg: 'tester.run("Who is a pony?")'"""

class SemanticTester:
    def __init__(self):
        self.lp = LogicParser()
        self.lx = Lexicon()
        self.fb = FactBase()

    def run(self,s):
        if (s[-1]=='?'):
            sent = s[:-1] + ' ?'  # tolerate absence of space before '?'
            if len(sent) == 0:
                return ("Eh??")
            else:
                wds = sent.split()
                trees = all_valid_parses(self.lx,wds)
                if (len(trees)==0):
                    return ("Eh??")
                elif (len(trees)>1):
                    return ("Ambiguous!")
                else:
                    tr = restore_words (trees[0],wds)
                    lam_exp = self.lp.parse(sem(tr))
                    L = lam_exp.simplify()
                    #print L  # useful for debugging
                    entities = self.lx.getAll('P')
                    results = find_all_solutions (L,entities,self.fb)
                    if (results == []):
                        if (wds[0].lower() == 'who'):
                            return ("No one")
                        else:
                            return ("None")
                    else:
                        return results
        elif (s[-1]=='.'):
            s = s[:-1]  # tolerate final full stop
            if len(s) == 0:
                return ("Eh??")
            else:
                wds = s.split()
                msg = process_statement(self.lx,wds,self.fb)
                if (msg == ''):
                    return ("OK.")
                else:
                    return ("Sorry - " + msg)
        else:
            return ("Please end with \".\" or \"?\" to avoid confusion.")
    
tester = SemanticTester()

def process(inputs):
    global tester
    tester = SemanticTester()
    for singleIn in inputs.split("\n"):
        if singleIn == "": continue
        if singleIn.endswith("."):
            #a statement
            output = tester.run(singleIn)
            if (output != "OK."):
                raise Exception("Expected 'OK.' but got '" + output + "' for '" + singleIn + "'" + exceptionMessage)
        else:
            #a query
            (query, expected) = singleIn.split("|")
            expected = expected.split(" ")
            output = tester.run(query)
            if not isinstance(output,list):
                output = [output]
            if (set(expected) != set(output)):
                raise Exception("Expected '" + " ".join(expected) + "' but got '" + " ".join(output) + "' for '" + query + "'" + exceptionMessage)
    return True
                

process("""Jack is an orange duck.
Who is an orange duck?|Eh??
Jack is a duck.
Who is an orange duck?|Eh??
Jack is orange.
Who is orange?|Jack
Who is a duck?|Jack
Who is an orange duck?|Jack""")

process("""Jack is a duck.
Jack is orange.
Which duck is orange?|Jack
Jill is a duck.
Jill is blue.
Jill is orange.
Which duck is blue and orange?|Eh??
Who is a duck and is orange?|Jack Jill""")

process("""Cheddar is a cheese.
Sam is a goat.
Sam eats Cheddar.
Who is a goat and eats a cheese?|Sam""")

process("""
Inf2A is a course.
Inf2C-SE is a course.
Inf2C-CS is a course.
DMMR is a course.
Tom is a person.
Dick is a person.
Harry is a person.
George is a person.
A is a pass.
B is a pass.
C is a pass.
D is a pass.
F is a fail.
Tom skips Inf2C-CS.
Dick skips Inf2C-SE.
Harry skips Inf2A.
Harry skips Inf2C-CS.
Tom gets B.
Dick gets A.
Harry gets F.
George gets A.
Who skips a course and gets a pass?|Tom Dick""")

process("""
Inf2A is a course.
Inf2C-SE is a course.
Inf2C-CS is a course.
Tom is a person.
Dick is a person.
Harry is a person.
Tom skips Inf2C-CS.
Dick skips Inf2C-SE.
Harry skips Inf2A.
Harry skips Inf2C-CS.
Tom passes Inf2C-CS.
Tom passes Inf2C-SE.
Tom passes Inf2A.
Dick fails Inf2C-CS.
Dick passes Inf2C-SE.
Dick fails Inf2A.
Harry passes Inf2C-CS.
Harry fails Inf2C-SE.
Harry fails Inf2A.
Who is a person who skips a course?|Tom Dick Harry
Who is a person who fails a course?|Dick Harry
Who skips a course and fails a course?|Dick Harry
Who is a person who skips a course and fails a course?|Ambiguous!""")