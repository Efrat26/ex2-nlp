from collections import defaultdict
import random

class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)

    def add_rule(self, lhs, rhs, weight):
        assert(isinstance(lhs, str))
        assert(isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w,l,r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l,r,w)
        return grammar

    def is_terminal(self, symbol): return symbol not in self._rules

    def gen(self, symbol, print_tree):
        if self.is_terminal(symbol):
            begin = ""
            if print_tree:
                begin = " "
            return begin + symbol
        else:
            expansion = self.random_expansion(symbol)
            begin = ""
            end = ""
            if print_tree:
                begin = "(" + symbol + " "
                end = ")"
            return begin + " ".join(self.gen(s, print_tree) for s in expansion) + end

    def random_sent(self, print_tree):
        return self.gen("ROOT", print_tree)

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r,w in self._rules[symbol]:
            p = p - w
            if p < 0:
                return r
        return r


if __name__ == '__main__':

    import sys
    pcfg = PCFG.from_file(sys.argv[1])
    num_of_sentences = 1
    print_tree = False
    if len(sys.argv) > 2:
        if sys.argv[2] == '-n':
            try:
                temp = int(sys.argv[3])
                num_of_sentences = temp
            except ValueError:
                num_of_sentences = 1

        elif sys.argv[2] == '-t':
            print_tree = True
    if len(sys.argv) == 5:
        if sys.argv[4] == '-t':
            print_tree = True
    for i in range(0, num_of_sentences):
        result = pcfg.random_sent(print_tree)
        print result
        original_sentence = ""
        sentence = result.replace("(", "")
        sentence = sentence.replace(")", "")
        splitted_sentece = sentence.split(" ")
        for symbol in splitted_sentece:
            if pcfg.is_terminal(symbol):
                original_sentence += symbol + " "
        print "original sentence is:\n" + original_sentence