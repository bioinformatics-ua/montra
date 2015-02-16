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
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone

import os
import re
import fileinput
import os.path
import zipfile
import json
from bson import json_util
from copy import deepcopy

from django.contrib.comments import Comment
from django.conf import settings

from questionnaire.models import Questionnaire, Question, QuestionSet, QuestionSetPermissions

from fingerprint.models import Fingerprint, Answer, FingerprintHead, AnswerChange

from api.models import FingerprintAPI

from docs_manager.models import Document

from population_characteristics.models import Characteristic, Comments

from hitcount.models import Hit, HitCount

class Command(BaseCommand):

    args = '<fingerprint_hash> <dir_file>'
    help = 'Exports a fingerprint object to a serializable object'

    def handle(self, *args, **options):
        if len(args) == 2:

            with zipfile.ZipFile(args[1]+"/"+args[0]+".emif","w") as zip:
                try:
                    print "- Finding fingerprint with hash "+str(args[0])
                    finger = Fingerprint.objects.get(fingerprint_hash=args[0])

                    print "- Writing fingerprint data"
                    zip.writestr('fingerprint.json', self.__generateFingerprintJson(finger))

                    print "- Writing answers"
                    zip.writestr('answers.json', self.__generateAnswersJson(finger))

                    print "-- Writing Fingerprint head revisions"
                    zip.writestr('fheads.json', self.__generateFingerprintHeadsJson(finger))

                    print "-- Writing Answer Changes"
                    zip.writestr('fans.json', self.__generateAnswersChangesJson(finger))

                    print "- Writing extra api information"
                    zip.writestr('extra.json', self.__generateExtra(finger))

                    print "- Writing discussion"
                    zip.writestr('discussion.json', self.__generateComment(finger))

                    print "- Handling documents"
                    print "-- Writing documents entries"
                    zip.writestr('documents_index.json', self.__generateDocuments(finger))

                    docs = self.__listDocuments(finger)

                    print "-- Writing relevant characteristic links"
                    zip.writestr('popchar.json', self.__generateCharacteristics(finger))

                    print "-- Writing files themselves"
                    for doc in docs:
                        try:
                            zip.write(doc.path, arcname="documents/"+doc.revision+doc.file_name)
                            print "--- Writing file "+str(doc.file_name)
                        except:
                            print "--- ERROR: Couldn't find file "+str(doc.file_name)

                    print "-- Writing characteristic comments"
                    zip.writestr('popcharcomments.json', self.__generatePopCharComments(finger))

                    print "- Writing hitcount"
                    zip.writestr('hitcount.json', self.__generateHitcount(finger))
                    zip.writestr('hitcount_detail.json', self.__generateHitcountDetail(finger))

                    print "- Writing qset permissions"
                    zip.writestr('qset_permissions.json', self.__generatePermissions(finger))

                    print "- Writing metadata"
                    zip.writestr('metadata.json', self.__generateMeta(finger))

                except Fingerprint.DoesNotExist:
                    print "-- ERROR: Fingerprint with hash " +hash+" doesn't exist on the system"


        else:
            self.stdout.write('-- USAGE: \n    '+
                'python manage.py fingerprint_export <fingerprint_hash> <dir_file>'+
                '\n\n')

    # This is used mainly to ensure some kind of integrity on data imported
    def __generateMeta(self, fingerprint):
        meta = {}

        emails = fingerprint.shared.all().values_list('email', flat=True)

        meta['shared-with'] = [e for e in emails]

        meta['catalogue-version'] = settings.VERSION
        meta['export-date'] = timezone.now().strftime('%B %d, %Y, %I:%M %p')

        meta['questionnaire'] = fingerprint.questionnaire.slug

        return json.dumps(meta, indent=4, default=json_util.default)

    def __generateFingerprintJson(self, fingerprint):
        finger = deepcopy(fingerprint.__dict__)

        del finger['_state']

        return json.dumps(finger, indent=4, default=json_util.default)

    def __generateAnswersJson(self, fingerprint):
        ans = Answer.objects.filter(fingerprint_id=fingerprint)

        return self.__getCleanJson(ans)

    def __generateFingerprintHeadsJson(self, fingerprint):
        fheads = FingerprintHead.objects.filter(fingerprint_id=fingerprint)

        return self.__getCleanJson(fheads)

    def __generateAnswersChangesJson(self, fingerprint):
        fans = AnswerChange.objects.filter(revision_head__fingerprint_id=fingerprint)

        return self.__getCleanJson(fans)

    def __generateExtra(self, fingerprint):
        extra = FingerprintAPI.objects.filter(fingerprintID=fingerprint.fingerprint_hash)

        return self.__getCleanJson(extra)

    def __generateComment(self, fingerprint):
        comments = Comment.objects.filter(object_pk = fingerprint.id)

        return self.__getCleanJson(comments)

    def __generateDocuments(self, fingerprint):
        docs = Document.objects.filter(fingerprint_id=fingerprint.fingerprint_hash)

        return self.__getCleanJson(docs)

    def __generateCharacteristics(self, fingerprint):

        ids = Document.objects.filter(fingerprint_id=fingerprint.fingerprint_hash).values_list('id', flat=True)

        relchar = Characteristic.objects.filter(id__in=ids).values_list('document_ptr', flat=True)

        return json.dumps([e for e in relchar], indent=4, default=json_util.default)

    def __generatePopCharComments(self, fingerprint):
        popcomments = Comments.objects.filter(fingerprint_id=fingerprint.fingerprint_hash)

        return self.__getCleanJson(popcomments)

    def __generateHitcount(self, fingerprint):
        count = HitCount.objects.filter(object_pk=fingerprint.id)

        return self.__getCleanJson(count)

    def __generateHitcountDetail(self, fingerprint):
        count = Hit.objects.filter(hitcount__object_pk=fingerprint.id)

        return self.__getCleanJson(count)

    def __generatePermissions(self, fingerprint):
        count = QuestionSetPermissions.objects.filter(fingerprint_id=fingerprint.fingerprint_hash)

        return self.__getCleanJson(count)

    def __listDocuments(self, fingerprint):
        docs = Document.objects.filter(fingerprint_id=fingerprint.fingerprint_hash)

        return docs

    def __getCleanJson(self, objects):
        objects = [ obj.__dict__ for obj in objects]

        try:
            for obj in objects:
                del obj['_state']
        except:
            pass

        return json.dumps(objects, indent=4, default=json_util.default)


