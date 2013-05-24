import random,sys,codecs


##########################################################################################################
# A random name generator, adapted from "A random name generator, by Peter Corbett", found at
# http://roguebasin.roguelikedevelopment.org/index.php?title=Markov_chains_name_generator_in_Python
##########################################################################################################


class MCD(dict):
    """A class to generate Markov-chain random words from a given list of words.

    How it works:
    We receive a list of words that seed our algorithm. The algorithm then populates a
    dictionary with prefixes as keys and a list of possible suffixes as values.

    The idea is that when we create a random word we can only use combinations of 
    letters that have already been observed in the seeding list of words. 
    This creates random, yet 'pronounceable' words.

    If for example our input is one word: "science" and we have a chainlength of 2,
    the populated dictionary would be:
    
    dict = {
    '  ' : ['s'], #We insert two spaces before the word, so '  ' is one of the prefixes
    ' s' : ['c'],
    'sc' : ['i'],
    'ci' : ['e'],
    'ie' : ['n'],
    'en' : ['c'],
    'nc' : ['e'],
    'ce' : ['\n'] #We add a newline character as a suffix for the end of the word.
    }

    Now when we create a word, we start with two spaces: '  '
    That's our first prefix, and it can only be followed by 's' as 's' is the only
    available suffix for '  '.
    Now our word is ' s' and because of our very limited seed, the only available
    suffix for ' s' is 'c'.

    Obviously, the bigger the seeding list of words, the greater variety we can have !

    Notice that the size of the chainlength is important, bigger chainlengths produce 
    words more similar to the original words while shorter chainlengths produce more
    random words. If chainlength is set to 1 you will encounter  words with triple (or more)
    consonants since the 'memory' of the algorithm is only one letter deep :
    e.g. if the word "suggest" is in the seeding list of words and chainlength is 1,
    the algorithm knows that 'g' can be followed by 'g', the new 'g' can also be followed 
    by 'g' and so on, but if chainlength is 2, 'ug' ('u' chosen randomly) can be followed
    by another 'g' but then 'gg' cannot be followed by a third one except if you have a 
    word with 'ggg' in your seeding list.
    """
    def __init__(self, filename,chainlen,encoding = None):
        """
        We inherit from the normal python dictionary class, so we initialize as such

        arguments:
        chainlen:   The length of the Markov chain. The bigger this value is, the more
                    similar the generated words will be to the original ones.
        filename:   Path to a text file that stores the original words (one word per row)
        encoding:   If you intend to read from a file that contains unicode, you will need
                    to provide its encoding, something like 'utf-8' or 'utf-16',
                    you can read more here: http://docs.python.org/2/library/codecs.html
        """
        self.encoding=encoding
        dict.__init__(self)
        self.chainlen = chainlen
        self.filename = filename
        self.populate()
        

    def __getitem__(self, key):
        """Dictionary inheritance stuff, not 100% sure this is needed but what the hell"""
        return dict.__getitem__(self, key)

    def __setitem__(self, key, val):
        """Dictionary inheritance stuff, not 100% sure this is needed but what the hell"""
        dict.__setitem__(self, key, val)

    def add_key(self, prefix, suffix):
        """Our dictionary's values are lists, this function adds a new key if it doesn't
        already exist or appends a new element in the value list if the key exists"""
        if prefix in self:
            self[prefix].append(suffix)
        else:
            self[prefix] = [suffix]
    def get_suffix(self,prefix):
        """Returns a random element of the value list of a key"""
        return random.choice(self[prefix])
    def getlistfromtext(self,filename):
        """Reads the text file and produces a list"""
        l=[]

        if self.encoding:
            f = codecs.open(filename,"r",encoding=self.encoding)
            for line in f:
                l.append(line.rstrip())
            f.close()

        else:
            f = open(filename,"r")
            for line in f:
                l.append(line.rstrip())
            f.close()
        return l
    def populate(self):
        """Populates the dictionary"""
        words = self.getlistfromtext(self.filename)
        if self.chainlen > 10 or self.chainlen < 1:
            print "Chain length must be between 1 and 10, inclusive"
            sys.exit(0)
        for l in words:
            l = l.strip()
            s = " " * self.chainlen + l
            for n in xrange(len(l)):
                self.add_key(s[n:n+self.chainlen], s[n+self.chainlen])
                
            self.add_key(s[len(l):len(l)+self.chainlen], "\n")
    def generate_words(self,N):
        """A generator that yields our new random words"""
        for i in xrange(N):
            prefix = " " * self.chainlen
            name = ""
            suffix = ""
            while True:
                suffix = self.get_suffix(prefix)
                if suffix == "\n" or len(name) > 9:
                    break
                else:
                    name = name + suffix
                    prefix = prefix[1:] + suffix
            yield name.capitalize()  

########################################################################################################
#Example usage
# initialize the class with a textfile that holds the input(seed) words and the desired chainlength
# a=MCD("./yourtextfile.txt",3)
#
# Reap the new words :)
# for i in a.generate_words(100):
#     print i
########################################################################################################

a=MCD("./new.txt",3,encoding='utf-16')
for i in a.generate_words(20):
    print i
