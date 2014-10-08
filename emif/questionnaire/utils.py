#!/usr/bin/python

def split_numal(val):
    """Split, for example, '1a' into (1, 'a')
>>> split_numal("11a")
(11, 'a')
>>> split_numal("99")
(99, '')
>>> split_numal("a")
(0, 'a')
>>> split_numal("")
(0, '')
    """
    if not val:
        return 0, ''
    for i in range(len(val)):
        if not val[i].isdigit():
            return int(val[0:i] or '0'), val[i:]
    return int(val), ''
        

def numal_sort(a, b):
    """Sort a list numeric-alphabetically

>>> vals = "1a 1 10 10a 10b 11 2 2a z".split(" "); \\
... vals.sort(numal_sort); \\
... " ".join(vals)
'z 1 1a 2 2a 10 10a 10b 11'
    """
    anum, astr = split_numal(a)
    bnum, bstr = split_numal(b)
    cmpnum = cmp(anum, bnum)
    if(cmpnum == 0):
        return cmp(astr, bstr)
    return cmpnum

def numal0_sort(a, b):
    """
    numal_sort on the first items in the list
    """
    return numal_sort(a[0], b[0])

if __name__ == "__main__":
    import doctest
    doctest.testmod()

class QuestionNumber:
    """
    State machine to create number of questions dynamically
    """
    def __init__(self):
        """
        n1, n2, n3, n4: level count
        t0, t1, t2, t3, t4: level text
        state: level state
        nQuestion: result
        :rtype : object
        """
        self._n1 = self._n2 = self._n3 = self._n4 = 1
        self._t0 = self._t1 = self._t2 = self._t3 = self._t4 = ''
        self._state = 'h1'
        self._nQuestion = ''

    def saveQuestionNumber(self):
        self._nQuestion = ''
        if self._t0:
            self._nQuestion += self._t0
        if self._t1 != '':
            self._nQuestion += '.' + self._t1
        if self._t2:
            self._nQuestion += '.' + self._t2
        if self._t3:
            self._nQuestion += '.' + self._t3
        if self._t4:
            self._nQuestion += '.' + self._t4

    def resetH0(self, hValue=1):
        self._t0 = str(hValue)
        self._n1 = self._n2 = self._n3 = self._n4 = 1
        self._t1 = self._t2 = self._t3 = self._t4 = ''
        self._state = 'h1'

    def resetH1(self):
        self._t1 = str(self._n1)
        self._n2 = self._n3 = self._n4 = 1
        self._t2 = self._t3 = self._t4 = ''
        self._n1 += 1
        self._state = 'h1'
        self.saveQuestionNumber()

    def resetH2(self):
        self._t2 = str(self._n2)
        self._n2 += 1
        self._n3 = self._n4 = 1
        self._t3 = self._t4 = ''
        self._state = 'h2'
        self.saveQuestionNumber()

    def resetH3(self):
        self._t3 = str(self._n3)
        self._n3 += 1
        self._n4 = 1
        self._t4 = ''
        self._state = 'h3'
        self.saveQuestionNumber()

    def resetH4(self):
        self._t4 = str(self._n4)
        self._n4 += 1
        self._state = 'h4'
        self.saveQuestionNumber()

    def getNumber(self, headingValue, hValue=1):
        """
        Function to get number of question, subquestion, etc.
        """
        # headingValue = 'h0' : QuestionSet
        if headingValue == 'h0':
            self.resetH0(hValue)
        elif self._state == 'h1':
            if headingValue == 'h1':
                self.resetH1()
            elif headingValue == 'h2':
                self.resetH2()
        elif self._state == 'h2':
            if headingValue == 'h1':
                self.resetH1()
            elif headingValue == 'h2':
                self.resetH2()
            elif headingValue == 'h3':
                self.resetH3()
        elif self._state == 'h3':
            if headingValue == 'h1':
                self.resetH1()
            elif headingValue == 'h2':
                self.resetH2()
            elif headingValue == 'h3':
                self.resetH3()
            elif headingValue == 'h4':
                self.resetH4()
        elif self._state == 'h4':
            if headingValue == 'h1':
                self.resetH1()
            elif headingValue == 'h2':
                self.resetH2()
            elif headingValue == 'h3':
                self.resetH3()
            elif headingValue == 'h4':
                self.resetH4()

        return self._nQuestion