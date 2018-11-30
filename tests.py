import statements as st
import pos_tagging as pt
from statements import Lexicon, FactBase
import agreement  as ag

def test_lexicon():
    lx = Lexicon()
    lx.add("John","P")
    lx.add("Mary","P")
    lx.add("like","T")
    assert set(lx.getAll("P")) == set(["John", "Mary"])

def test_factBase():
    fb = FactBase()
    fb.addUnary("duck", "John")
    fb.addBinary("love", "John", "Mary")
    assert fb.queryUnary("duck", "John") == True
    assert fb.queryUnary("duck", "Mary") == False
    assert fb.queryBinary("love", "Mary", "John") == False
    assert fb.queryBinary("love", "John", "Mary") == True

def test_verb_stem():
    assert st.verb_stem('tells') == 'tell'
    assert st.verb_stem('buys') == 'buy'
    assert st.verb_stem('buysa') == ""
    assert st.verb_stem('tries') == 'try'
    assert st.verb_stem('flies') == 'fly'
    assert st.verb_stem('dies') == 'die'
    assert st.verb_stem('fixes') == 'fix' 
    assert st.verb_stem('goes') == 'go'
    assert st.verb_stem('boxes') == 'box' # is in Brown Corpus
    assert st.verb_stem('attaches') == 'attach'
    assert st.verb_stem('washes') == 'wash' # is in Brown Corpus
    assert st.verb_stem('fizzes') == '' # not in Brown Corpus
    assert st.verb_stem('dresses') == 'dress' # not in Brown Corpus
    assert st.verb_stem('loses') == 'lose'
    assert st.verb_stem('dazes') == '' # not in Brown Corpus
    assert st.verb_stem('has') == 'have' # should be ignored according to https://piazza.com/class/jkuzor9eypxov?cid=240
    assert st.verb_stem('likes') == 'like'
    assert st.verb_stem('hates') == 'hate'
    assert st.verb_stem('bathes') == 'bathe' # not in Brown Corpus
    assert st.verb_stem('is') == '' # should be ignored according https://piazza.com/class/jkuzor9eypxov?cid=240
    assert st.verb_stem('unties') == '' # not in Brown Corpus
    assert st.verb_stem('cats') == ''
    assert st.verb_stem('analyses') == '' # not in Brown Corpus
    assert st.verb_stem('does') == 'do'

def test_unchanging_plurals():
    assert set(pt.unchanging_plurals()) == set(['dna', 'headquarters',
                                       'series', 'fish', 'cannabis',
                                       'multimedia', 'sheep',
                                       'species', 'police',
                                       'marijuana', 'deer',
                                       'salmon', 'moose', 'swine',
                                       'bison', 'buffalo', 'trout'])

def test_noun_stem():
    assert pt.noun_stem('deer') == 'deer'
    assert pt.noun_stem('buffalo') == 'buffalo'
    assert pt.noun_stem('women') == 'woman'
    assert pt.noun_stem('men') == 'man'
    assert pt.noun_stem('dogs') == 'dog'
    assert pt.noun_stem('countries') == 'country'
    assert pt.noun_stem('ashes') == 'ash'

def test_tag_word():
    # Creating and training the lexicon:
    lx = Lexicon()
    lx.add("John", "P")
    lx.add("orange", "N")
    lx.add("orange", "A")
    lx.add("fish", "N")
    lx.add("fish", "T")
    lx.add("fish", "I")
    lx.add("sell", "T")
    lx.add("fly", "I")
    lx.add("man", "N")
    # testing:

    assert sorted(pt.tag_word(lx, "John")) == sorted(["P"])
    assert sorted(pt.tag_word(lx, "orange")) == sorted(["Ns", "A"])
    assert (sorted(pt.tag_word(lx, "fish")) ==
            sorted(["Ns", "Np", "Ip", "Tp"]))
    assert sorted(pt.tag_word(lx, "a")) == sorted(["AR"])
    assert sorted(pt.tag_word(lx, "sells")) == sorted(["Ts"])
    assert sorted(pt.tag_word(lx, "sell")) == sorted(["Tp"])
    assert sorted(pt.tag_word(lx, "flies")) == sorted(["Is"])
    assert sorted(pt.tag_word(lx, "fly")) == sorted(["Ip"])
    assert sorted(pt.tag_word(lx, "oranges")) == sorted(["Np"])
    assert sorted(pt.tag_word(lx, "men")) == sorted(["Np"])
    assert sorted(pt.tag_word(lx, "man")) == sorted(["Ns"])
    assert sorted(pt.tag_word(lx, "is")) == sorted(["BEs"])
    assert pt.tag_word(lx, "ffjjdjd") == []

def test_check_node():
    lx = Lexicon()
    lx.add("John","P")
    lx.add("Mary","P")
    lx.add("like","T")
    lx.add("orange","N")
    lx.add("apple","N")
    tr0 = ag.all_valid_parses(lx, ['Who','likes','oranges','?'])[0]
    tr = ag.restore_words(tr0,['Who','likes','oranges','?'])
    tr.draw()


def test():
    test_factBase()
    test_lexicon()
    test_verb_stem()
    test_noun_stem()
    test_unchanging_plurals()
    test_tag_word()
    test_check_node()
test()