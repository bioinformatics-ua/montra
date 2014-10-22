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
"""This class is used to export the fingerprint template to excel
"""
class ExportFingerprint(object):


    def __init__(self, questionnaire ):
        self.questionnaire = questionnaire


    def ignore_questionsets(self, questionset_list):
        raise NotImplementedError("Please Implement this method")

    def export(self):
        raise NotImplementedError("Please Implement this method")

    """This method will build the object according with the type
    of the object to export.
    """
    @staticmethod
    def factory(t_type, questionnaire):
        if t_type == "csv_plain":
            pass
        else:
            raise Exception("The supplied format is not supported")


class ExportFingerprintCSVPlain(ExportFingerprint):

    def __init__(self, questionnaire ):
        super.__init__(self, questionnaire)
        pass

    def ignore_questionsets(self, questionset_list):
        raise NotImplementedError("Please Implement this method")

    def export(self):
        result = ""
        questionsets = Questionnaire.questionsets()

        for qs in questionsets:

            qs.questions()


