import statements as st
import pos_tagging as pt
from statements import Lexicon, FactBase

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
    assert st.verb_stem('fixes') == '' # not in Brown Corpus
    assert st.verb_stem('goes') == 'go'
    assert st.verb_stem('boxes') == '' # not in Brown Corpus
    assert st.verb_stem('attaches') == 'attach'
    assert st.verb_stem('washes') == '' # not in Brown Corpus
    assert st.verb_stem('fizzes') == '' # not in Brown Corpus
    assert st.verb_stem('dresses') == '' # not in Brown Corpus
    assert st.verb_stem('loses') == 'lose'
    assert st.verb_stem('losses') == 'loss'
    assert st.verb_stem('dazes') == '' # not in Brown Corpus
    assert st.verb_stem('has') == 'have'
    assert st.verb_stem('likes') == 'like'
    assert st.verb_stem('hates') == 'hate'
    assert st.verb_stem('bathes') == '' # not in Brown Corpus
    assert st.verb_stem('has') == 'have'
    assert st.verb_stem('cats') == ''
    assert st.verb_stem('analyses') == '' # not in Brown Corpus

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
    #lx.add("sells", "T") Why is sells a stem of T?
    lx.add("sell", "T")
    lx.add("flies", "I")
    lx.add("fly", "I")
    lx.add("oranges", "N")
    lx.add("men", "N")
    lx.add("man", "N")
    # testing:
    print(pt.tag_word(lx, "John"))
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
    assert pt.tag_word(lx, "ffjjdjd") == []



def test():
    test_factBase()
    test_lexicon()
    test_unchanging_plurals()
    test_tag_word()
test()