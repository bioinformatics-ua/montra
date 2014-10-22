# -*- coding: utf-8 -*-
# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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
#

from questionnaire.models import *


# TODO: put this code in utils
def removehs(value):
    value = value.replace('h0. ','')
    value = value.replace('h1. ','')
    value = value.replace('h2. ','')
    value = value.replace('h3. ','')
    value = value.replace('h4. ','')
    value = value.replace('h5. ','')
    value = value.replace('h6. ','')
    value = value.replace('h7. ','')
    return value


"""This class is used to export the fingerprint template to excel
"""
class ExportFingerprint(object):


    def __init__(self, questionnaire ):
        self.questionnaire = questionnaire


    def ignore_questionsets(self, questionset_list):
        raise NotImplementedError("Please Implement this method")

    def export(self):
        raise NotImplementedError("Please Implement this method")


    def level(self, question):
        return question.number.count(".") + 1


    def clean(self, text):
        return removehs(text)


    """This method will build the object according with the type
    of the object to export.
    """
    @staticmethod
    def factory(t_type, questionnaire):
        if t_type == "csv_plain":
            return ExportFingerprintCSVPlain(questionnaire)
        else:
            raise Exception("The supplied format is not supported")


class ExportFingerprintCSVPlain(ExportFingerprint):

    def __init__(self, questionnaire ):
        ExportFingerprint.__init__(self, questionnaire)

    def ignore_questionsets(self, questionset_list):
        raise NotImplementedError("Please Implement this method")

    def get_tabs(self, level):

        return "\t" * level

    def export(self):
        result = ""
        questionsets = self.questionnaire.questionsets()

        for qs in questionsets:

            result += str(qs.sortid) + " - " + self.clean(qs.text)  + "\n"
            questions = qs.questions()
            for q in questions:
                _level  = self.level(q)
                result += self.get_tabs(_level)
                result += str(q.number)  + " " + self.clean(q.text) +"\n"


        f = open('/tmp/csvplain.csv','w')
        f.write(result)
        f.close()


def main():

    q = Questionnaire.objects.get(id=53)

    exporter = ExportFingerprint.factory("csv_plain", q)
    exporter.export()









