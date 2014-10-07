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
from fingerprint.services import indexFingerprint

from api.models import FingerprintAPI

from docs_manager.models import FingerprintDocuments

from population_characteristics.models import Characteristic, Comments

from hitcount.models import Hit, HitCount

from emif.utils import generate_hash

from django.core.management import call_command

if settings.DEBUG:
    PATH_STORE_FILES = settings.PROJECT_DIR_ROOT  + 'emif/static/files/'
else:
    PATH_STORE_FILES = settings.PROJECT_DIR_ROOT  + settings.MIDDLE_DIR +'static/files/'


IMPOSSIBLE = -1
AS_IS = 0
NEW_IDS = 1

class Command(BaseCommand):

    args = '<path>'
    help = 'Imports a fingerprint object to a serializable object'

    def handle(self, *args, **options):
        if len(args) == 1:

            with zipfile.ZipFile(args[0],"r") as zip:
                meta = json.loads(zip.read('metadata.json'),object_hook=json_util.object_hook)
                fdict = json.loads(zip.read('fingerprint.json'),object_hook=json_util.object_hook)

                new_fingerprint = Fingerprint()
                new_hash =None

                level = self.__checkFeasibility(meta, fdict)

                if level == AS_IS:
                    self.stdout.write('-- Hash/fingerprint_id are free, import as is on exported file.\n')

                    new_fingerprint.__dict__.update(fdict)

                    new_fingerprint.save()

                    self.__import(zip, args[0], new_fingerprint)

                elif level == NEW_IDS:
                    self.stdout.write('-- Hash/fingerprint_id are occupied, importing with a new id.\n')
                    new_hash = generate_hash()

                    fdict['fingerprint_hash'] = new_hash
                    del fdict['id']
                    new_fingerprint.__dict__.update(fdict)

                    new_fingerprint.save()

                    self.__addShares(meta, new_fingerprint)

                    self.__import(zip, args[0], new_fingerprint, replacing=True)

                else: # impossible
                    self.stdout.write('-- ERROR: Impossible to import fingerprint, the questionnaire doesnt exist, or doesnt match the slug.')


        else:
            self.stdout.write('-- USAGE: \n    '+
                'python manage.py fingerprint_import <path_file>'+
                '\n\n')

    # There's a need to check a couple of things. First we must ensure the owner of the database exists in the system.
    # Second, we need to check if the questionnaire also exists in the system. Without those two the import is pointless
    # After this, we must check if the shared users exist, while this are not mandatory, we can only add users available
    # We must also check if the fingerprint_hash is taken, or if the primary key that was used to export is taken, to see
    # if we must make new ones
    def __checkFeasibility(self, meta, fdict):
        try:
            quest = Questionnaire.objects.get(id=fdict['questionnaire_id'])

            if quest.slug != meta['questionnaire']:
                return IMPOSSIBLE

            try:
                finger = Fingerprint.objects.get(id = fdict['id'])

                return NEW_IDS

            except Fingerprint.DoesNotExist:
                return AS_IS

        except Questionnaire.DoesNotExist:
            return IMPOSSIBLE

    def __import(self, zip, old, fingerprint, replacing=False):

        print "- Saved fingerprint model"

        self.__writeFiles(zip)

        print "- Saved all files to static files folder"

        answers_map = self.__importAnswers(zip, fingerprint, replacing)

        print "- Saved all answers to models"

        fheads_map = self.__importFHeads(zip, fingerprint, replacing)

        print "- Saved fingerprint head revisions to models"

        self.__importFans(zip, fingerprint, answers_map, fheads_map,replacing)

        print "- Saved fingerprint answer changes to models"

        self.__importQsetPermissions(zip, fingerprint, replacing)

        print "- Saved Qset Permissions to models"

        self.__importDiscussion(zip, fingerprint, replacing)

        print "- Saved Discussion to models"

        hitmap = self.__importHitCount(zip, fingerprint, replacing)

        self.__importHitCountDetails(zip, fingerprint, hitmap, replacing)

        print "- Saved hitcount to models"

        self.__importAPI(zip, fingerprint, replacing)

        print "- Saved extra API data to models"

        self.__importDocumentReferences(zip, fingerprint, replacing)

        print "- Saved Document References (except pop char.) to models"


        charmap = self.__importCharacteristicReferences(zip, fingerprint, replacing)

        print "- Saved PopChar Documents References to models"

        self.__importPopCharComments(zip, fingerprint, charmap, replacing)

        print "- Saved PopChar comments to models"

        indexFingerprint(fingerprint.fingerprint_hash)

        print "- Indexed the imported fingerprint on solr "

        call_command('index_mongod')

        print "- Ran mongod indexing and aggregation"

        print "---- Finished importing "+str(old)+" with fingerprint hash "+fingerprint.fingerprint_hash

    # Since we  can be changing references, i have to map the changes...
    def __importAnswers(self, zip ,fingerprint , replacing):
        answers = json.loads(zip.read('answers.json'), object_hook=json_util.object_hook)
        tmap = None
        before = None

        if replacing:
            tmap = {}

        for ans in answers:

            this_ans = Answer()

            if replacing:
                ans['fingerprint_id_id'] = fingerprint.id

                before = ans['id']
                del ans['id']

            this_ans.__dict__.update(ans)

            this_ans.save()

            if replacing:
                tmap[before] = this_ans.id


        return tmap

    # Since we  can be changing references, i have to map the changes...
    def __importFHeads(self, zip ,fingerprint , replacing):
        fheads = json.loads(zip.read('fheads.json'), object_hook=json_util.object_hook)
        tmap = None
        before = None

        if replacing:
            tmap = {}

        for head in fheads:

            this_head = FingerprintHead()

            if replacing:
                head['fingerprint_id_id'] = fingerprint.id

                before = head['id']
                del head['id']

            this_head.__dict__.update(head)

            this_head.save()

            if replacing:
                tmap[before] = this_head.id


        return tmap

    def __importFans(self, zip, fingerprint, answers_map, fheads_map, replacing):
        fans = json.loads(zip.read('fans.json'), object_hook=json_util.object_hook)

        for fan in fans:

            this_fan = AnswerChange()

            if replacing:
                fan['revision_head_id'] = fheads_map[fan['revision_head_id']]
                fan['answer_id'] = answers_map[fan['answer_id']]

                del fan['id']

            this_fan.__dict__.update(fan)

            this_fan.save()

    def __importQsetPermissions(self, zip, fingerprint, replacing):
        qperms = json.loads(zip.read('qset_permissions.json'), object_hook=json_util.object_hook)

        for qperm in qperms:

            this_qperm = QuestionSetPermissions()

            if replacing:
                qperm['fingerprint_id'] = fingerprint.fingerprint_hash
                del qperm['id']

            this_qperm.__dict__.update(qperm)

            this_qperm.save()

    def __importDiscussion(self, zip, fingerprint, replacing):
        comments = json.loads(zip.read('discussion.json'), object_hook=json_util.object_hook)

        for comment in comments:

            this_comment = Comment()

            if replacing:
                comment['object_pk'] = fingerprint.id
                del comment['id']

            # Here we also have to check if user exists, otherwise we set it to anonymous
            try:
                this_user = User.objects.get(id=comment['user_id'])
            except:
                comment['user_id'] = -1

            this_comment.__dict__.update(comment)

            this_comment.save()

    # Since we  can be changing references, i have to map the changes...
    def __importHitCount(self, zip , fingerprint , replacing):
        hits = json.loads(zip.read('hitcount.json'), object_hook=json_util.object_hook)
        tmap = None
        before = None

        if replacing:
            tmap = {}

        for hit in hits:

            this_hit = HitCount()

            if replacing:
                hit['object_pk'] = fingerprint.id

                before = hit['id']
                del hit['id']

            this_hit.__dict__.update(hit)

            this_hit.save()

            if replacing:
                tmap[before] = this_hit.id


        return tmap

    def __importHitCountDetails(self, zip, fingerprint, hitmap, replacing):
        hitdetails = json.loads(zip.read('hitcount_detail.json'), object_hook=json_util.object_hook)

        for hitdetail in hitdetails:

            this_hitdetail = Hit()

            if replacing:
                hitdetail['hitcount_id'] = hitmap[hitdetail['hitcount_id']]

                del hitdetail['id']

            try:
                this_user = User.objects.get(id=hitdetail['user_id'])
            except:
                hitdetail['user_id'] = -1

            this_hitdetail.__dict__.update(hitdetail)

            this_hitdetail.save()

    def __importAPI(self, zip, fingerprint, replacing):
        extra = json.loads(zip.read('extra.json'), object_hook=json_util.object_hook)

        for ex in extra:

            this_extra = FingerprintAPI()

            if replacing:
                ex['fingerprintID'] = fingerprint.fingerprint_hash
                del ex['id']

            this_extra.__dict__.update(ex)

            this_extra.save()

    # Since we  can be changing references, i have to map the changes...
    def __importDocumentReferences(self, zip ,fingerprint , replacing):
        docs = json.loads(zip.read('documents_index.json'), object_hook=json_util.object_hook)
        popcharlist = json.loads(zip.read('popchar.json'), object_hook=json_util.object_hook)

        for doc in docs:
            # PopChar dont pass through here. Are added using Characteristic model
            if doc['id'] not in popcharlist:
                this_doc = FingerprintDocuments()

                if replacing:
                    doc['fingerprint_id'] = fingerprint.fingerprint_hash

                    del doc['id']

                # update absolute paths, since they are relative to static file folder in every setup
                doc['path'] = os.path.abspath(PATH_STORE_FILES)+"/"+doc['revision']+doc['file_name']

                this_doc.__dict__.update(doc)

                this_doc.save()

    # Since we  can be changing references, i have to map the changes...
    def __importCharacteristicReferences(self, zip ,fingerprint , replacing):
        docs = json.loads(zip.read('documents_index.json'), object_hook=json_util.object_hook)
        popcharlist = json.loads(zip.read('popchar.json'), object_hook=json_util.object_hook)
        tmap = None
        before = None

        if replacing:
            tmap = {}

        for doc in docs:
            # PopChar dont pass through here. Are added using Characteristic model
            if doc['id'] in popcharlist:
                this_doc = Characteristic()

                if replacing:
                    doc['fingerprint_id'] = fingerprint.fingerprint_hash

                    before = doc['id']
                    del doc['id']

                # update absolute paths, since they are relative to static file folder in every setup
                doc['path'] = os.path.abspath(PATH_STORE_FILES)+"/"+doc['revision']+doc['file_name']

                this_doc.__dict__.update(doc)

                this_doc.save()

                if replacing:
                    tmap[before] = this_doc.id

        return tmap

    def __importPopCharComments(self, zip, fingerprint, charmap, replacing):
        comments = json.loads(zip.read('popcharcomments.json'), object_hook=json_util.object_hook)

        for comment in comments:

            this_comment = Comments()

            if replacing:
                comment['fingerprint_id'] = fingerprint.fingerprint_hash
                del comment['id']

            # Here we also have to check if user exists, otherwise we set it to anonymous
            try:
                this_user = User.objects.get(id=comment['user_id'])
            except:
                comment['user_id'] = -1

            this_comment.__dict__.update(comment)

            this_comment.save()

    def __addShares(self, meta, fingerprint):
        for m in meta['shared-with']:
            try:
                share = User.objects.get(email=m)
                fingerprint.shared.add(share)
            except User.DoesNotExist:
                print "User with email "+str(m)+" doesn't exist."

        fingerprint.save()

    def __writeFiles(self, zip):
        for file in zip.namelist():
            if file.startswith('documents/'):
                name = file[10:]
                f = zip.read(file)
                with open(os.path.join(os.path.abspath(PATH_STORE_FILES), name), 'wb+') as destination:
                    destination.write(f)
                print "Wrote file "+str(name)
