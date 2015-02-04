# Copyright (C) 2014 Ricardo Ribeiro and Universidade de Aveiro
#
# Authors: Ricardo Ribeiro <ribeiro.r@ua.pt>
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

from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User

from questionnaire.imports import ImportQuestionnaire, ImportQuestionnaireExcel

from optparse import make_option

from Levenshtein import ratio

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--similar',
            dest='similar',
            default=1,
            help='Instead of exact match, analyse choice changes using an similarity approach'),
            make_option('--ignore',
            dest='ignore',
            default=0.4,
            help='When using a similar approach, ignore strings with proximity lower of 0.4')
        )

    args = '<file_path> <questionnaire_id>'
    help = 'Import the questionnaire from excel merging with an already existing questionnaire'

    def handle(self, *args, **options):
        if len(args) == 2:

            iq = ImportQuestionnaire.factory('excel', args[0])

            if options['similar'] != 1:
                print "Similarity mode"
                def infer_function(question, new, old):
                    # default map translations that need no manual confirmation( this should go to a separate file later)
                    default_map = {
                        'Repeated collection(more than once)': 'Repeated collection (specify frequency and/or time interval) ',
                        'Subgroup analyzed (eg. Dementia)': 'Subgroup analyzed (eg. Dementia, please specify subgroup)'
                    }

                    try:
                        if ratio(unicode(default_map[old]), unicode(new)) > 0.97:
                            return True

                        return False

                    except KeyError:
                        print "Not default mapping, manual input required"

                    input = None


                    # Ignore low scores automatically
                    if ratio(old, new) < float(options['ignore']):
                        return False

                    while not (input == 'y' or input == 'n'):
                        print """The number of new choices missing processing for question %s is 1, there could be a non obvious match.\n

                        Is '%s' a change of '%s' ? (y/n)
                        """ % (question, new, old)
                        input = raw_input()

                    if input == 'y':
                        return True

                    return False

                res = iq.import_questionnaire(merge=args[1], mode=ImportQuestionnaireExcel.SIMILARITY_MODE,
                    percentage=float(options['similar']), infer_function=infer_function)


            else:
                print "Exact match mode"

                res = iq.import_questionnaire(merge=args[1])


            print "RESULT:"
            print res

            print "-- Finished processing "+args[0]

        else:
            self.stdout.write('-- USAGE: \n    '+
                'python manage.py merge_questionnaire <path_file> <questionnaire_id> [--similar <percentage>]'+
                '\n\n')
