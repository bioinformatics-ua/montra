#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from searchengine.models import Slugs

def next_free_slug(slug_str, create=True, scope=None):
    # avoiding circular imports... this is ugly... i know...
    from questionnaire.models import Question, Questionnaire

    i=-1

    def success(this_try):
        if create:
            slug = Slugs(slug1=this_try)
            slug.save()

            return slug

        else:
            return this_try

    # if we have 1000 slugs with the same name we have something wrong...
    while i < 1000:
        this_try = slug_str
        if i >= 0:
            this_try = slug_str+'_'+str(i)

        slug = Slugs.objects.filter(slug1=this_try)

        if len(slug) == 0:
            return success(this_try)
        else:
            if scope != None:
                inscope = Question.objects.filter(questionset__questionnaire=scope, slug_fk__slug1=this_try)

                if len(inscope) == 0:
                    return success(this_try)

            i+=1

    return None

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

    def __str__(self):
        tmp = ""

        tmp += '%s.' % self._t0

        if self._t1:
            tmp += '%s.' % self._t1
        if self._t2:
            tmp += '%s.' % self._t2
        if self._t3:
            tmp += '%s.' % self._t3
        if self._t4:
            tmp += '%s.' % self._t4

        return tmp[:-1]

    def setState(self, number):
        ''' Jump starts the question number into a given state. Useful for merging operations
            P.S. I really dont like the way this function works, it limits the level to 4 levels only
            and makes us lose time repeating statements. We should use an array for state keeping...
        '''
        partials = number.split('.')
        plen = len(partials)

        if plen <= 5:
            self._t0 = partials[0]
            self._n0 = int(partials[0])+1

            if plen >= 2:
                self._t1 = partials[1]
                self._n1 = int(partials[1])+1

                if plen >= 3:
                    self._t2 = partials[2]
                    self._n2 = int(partials[2])+1


                    if plen >= 4:
                        self._t3 = partials[3]
                        self._n3 = int(partials[3])+1

                        if plen == 5:
                            self._t4 = partials[4]
                            self._n4 = int(partials[4])+1

        else:
            raise Exception('Tried to configure an invalid number of levels, max levels are %d', len(self.states))

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
