# Python 3.4.2 64bit
class Subsequence:

    def __init__(self, pattern):
        self.perfect = pattern
        self.edit1 = self.edits1(pattern)

    # Norvig code with slight change: http://norvig.com/spell-correct.html
    def edits1(self, pattern):
        alphabet = 'GATC'

        splits     = [(pattern[:i], pattern[i:]) for i in range(len(pattern) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
        inserts    = [a + c + b     for a, b in splits for c in alphabet]

        return set(deletes + transposes + replaces + inserts)


    # match new sequence with search pattern

    def perfectMatch(self, sequence):
        if self.perfect in sequence:
            return self.perfect

        return []

    def match(self, sequence):
        if self.perfect in sequence:
            return self.perfect
        else:
            for sub in self.edit1:
                if sub in sequence:
                    return sub

        return []

    def getEdits1(self):
        return self.edit1

