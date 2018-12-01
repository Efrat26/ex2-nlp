from collections import defaultdict
import random

class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)
        self.tree_string = ''

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

    def null_tree_string(self): self.tree_string = ''

    def gen(self, symbol):
        if self.is_terminal(symbol):
            self.tree_string += symbol + ')'
            return symbol
        else:
            expansion = self.random_expansion(symbol)
            result = " ".join(self.gen(s) for s in expansion)
            return result

    def random_sent(self):
        return [self.tree_string, self.gen("ROOT")]

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r,w in self._rules[symbol]:
            p = p - w
            if p < 0:
                #self.tree_string += '(' + r + ' '
                return r
        #self.tree_string += '(' + r + ' '
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
    if len(sys.argv) == 5:
        if sys.argv[4] == '-t':
            print_tree = True
    for i in range(0, num_of_sentences):
        pcfg.null_tree_string()
        print pcfg.random_sent()[1]
        if print_tree:
            print pcfg.random_sent()[0]