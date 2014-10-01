import csv

from fingerprint.models import *
from questionnaire.models import Questionnaire, QuestionSet, Question, QuestionSetPermissions
from questionnaire.views import *

from django.contrib.auth.models import User

from searchengine.search_indexes import generateFreeText, setProperFields, CoreEngine

from django.utils import timezone

from notifications.models import Notification
from notifications.services import sendNotification

from datetime import timedelta

#import api.models.FingerprintAPI

from searchengine.search_indexes import CoreEngine

def define_rows(request):
    if request.POST and "page_rows" in request.POST:
        rows = int(request.POST["page_rows"])

        profile = request.user.get_profile()

        profile.paginator = rows

        profile.save()

    else:
        # Otherwise get number of rows from preferences
        rows = 5

        try:
            profile = request.user.get_profile()

            rows = profile.paginator

        except:
            pass

    if rows == -1:
        rows = 99999

    return rows

def merge_highlight_results(query, resultHighlights):
    c = CoreEngine()
    h = {}
    h["results"] = resultHighlights

    if query:
        qresults = c.highlight_questions(query)
        h["questions"] = qresults.highlighting

    return h

def get_api_info(fingerprint_id):
    """This is an auxiliar method to get the API Info
    """
    result = {}


    results = FingerprintAPI.objects.filter(fingerprintID=fingerprint_id)
    result = {}
    for r in results:
        result[r.field] = r.value
    return result

def saveFingerprintAnswers(qlist_general, fingerprint_id, questionnaire, user, extra_fields=None, created_date=None):

    # Update or create fingerprint entry
    #print "Updating fingerprint "+fingerprint_id
    fingerprint = updateFingerprint(fingerprint_id, questionnaire, user)

    # If no errors on getting the fingerprint, update/add the new questions
    if fingerprint != None:
        #print "Getting answers"
        # i get them all, instead of a query for each, is probabily faster this way
        answers = Answer.objects.filter(fingerprint_id=fingerprint)

        # TO DO
        #print "Updating answers "+fingerprint_id
        # For each response in qlist_general

        versionhead = None

        # we must mark answer requests as solved if any exist when a question is given an response
        answer_requests = AnswerRequest.objects.filter(fingerprint=fingerprint, removed = False)

        #print "TO:"
        for qs_aux, qlist in qlist_general:
            for question, qdict in qlist:
                value = getAnswerValue(question, qdict)
                comment = getComment(question, extra_fields)

                #print question.slug_fk.slug1 + ": '"+value+"' Comment: " + str(comment)

                if value != None:
                    if value.strip() != "":
                        markAnswerRequests(user, fingerprint, question, answer_requests)

                    this_ans = None
                    try:
                        this_ans = Answer.objects.get(fingerprint_id=fingerprint, question=question)

                        current_value = this_ans.data
                        current_comment = this_ans.comment

                        # update existing answers
                        this_ans.data=value;

                        #if comment != None:
                        this_ans.comment=comment;

                        #print "UPDATE: "
                        #print this_ans
                        this_ans.save()

                        # if value or comment changed
                        if current_value != value or current_comment != comment:
                            # create version head if not any yet
                            if versionhead == None:
                                # find out if we already have other revisions, if not revision starts at 1
                                revision = None

                                try:
                                    last_revision = FingerprintHead.objects.filter(fingerprint_id=fingerprint).order_by('-id')[0]

                                    revision = last_revision.revision+1
                                except:
                                    revision = 1

                                versionhead = FingerprintHead(fingerprint_id=fingerprint, revision=revision)

                                versionhead.save()

                            # save answerchange
                            answerchange = AnswerChange(revision_head=versionhead, answer=this_ans, old_value=current_value, new_value=value, old_comment=current_comment, new_comment=comment)
                            answerchange.save()

                    except Answer.DoesNotExist:
                        # new ,create new answer
                        this_ans = Answer(question=question, data=value, comment=comment, fingerprint_id=fingerprint)
                        #print "NEW: "
                        #print this_ans
                        this_ans.save()

        return checkMandatoryAnswers(fingerprint)


        # format for answers : Answer(question=question, data=data, comment=comment, fingerprint_id=fingerprint_id)

def getComment(question, extra_fields):

    try:
        comment = extra_fields['comment_question_'+question.slug_fk.slug1+"_t"]

        return comment
    except:
        pass


    return None

# Checks if all mandatory answers have been answered, namely fingerprint name
def checkMandatoryAnswers(fingerprint):
    try:
        name = Answer.objects.get(fingerprint_id=fingerprint, question__slug_fk__slug1="database_name")

        if name.data.strip() == "":
            return False

    except Answer.DoesNotExist:
        return False

    return True

def getAnswerValue(question, qdict):

    try:
        choices = None
        value = None
        choices_txt = None
        if qdict.has_key('value'):
            value = qdict['value']

            #if "yes" in qdict['value']:
            #    appending_text += question.text

        elif qdict.has_key('choices'):
            #import pdb
            #pdb.set_trace()
            choices = qdict['choices']
            qv = ""
            try:
                qv = qdict['qvalue']

            except:
                # raise
                pass

            value = qv

            do_again = False
            try:
                if len(choices[0])==3:
                    for choice, unk, checked  in choices:
                        if checked == " checked":
                            value = value + "#" + choice.value

                elif len(choices[0])==4:
                    for choice, unk, checked, _aux  in choices:
                        if checked == " checked":
                            if _aux != "":
                                value = value + "#" + choice.value + "{" + _aux +"}"
                            else:
                                value = value + "#" + choice.value


                elif len(choices[0])==2:
                    for checked, choice  in choices:
                        # print("checked" + str(checked))
                        if checked:
                            value = value + "#" + choice.value

            except:
                do_again = True

            if do_again:
                for checked, choice  in choices:
                    # print("checked" + str(checked))
                    if checked:

                        value = value + "#" + choice.value


            # print("choice value " + value)

            '''
            TO-DO
            Verify if symbols || (separator) is compatible with solr
            '''
            #Save in case of extra field is filled
            if qdict.has_key('extras'):
                extras = qdict['extras']
                # print("EXTRAS: " + str(extras))
                for q, val in extras:
                    # print("VAL: " + str(q) + " - " + str(val))
                    if val:
                        value = value + "||" + val


        else:
            pass

        slug = question.slug_fk.slug1

        return value
    except:
        #raise
        pass

    return None

def updateFingerprint(fingerprint_id, questionnaire, user):

    def getUser(user):
        try:
            user = User.objects.get(username=user)

            return user

        except User.DoesNotExist:
            print "Couldnt find user "+user
            return None

    fingerprint = None

    try:
        fingerprint = Fingerprint.objects.get(fingerprint_hash=fingerprint_id)

        # In case already exists, update latest modification time
        fingerprint.last_modification = timezone.now()
        fingerprint.save()

    # In case is a new one, create it
    except Fingerprint.DoesNotExist:

        user_fk = getUser(user)

        if user_fk == None:
            print "-- ERROR: Could not save fingerprint because user '"+user+"' does not exist."
        elif questionnaire == None or not isinstance(questionnaire, Questionnaire):
            print "-- ERROR: You must pass a valid questionnaire object to save a fingerprint."
        else:
            # At this point the description isnt being used (since there's no way to add descriptions to a fingerprint on the gui)
            fingerprint = Fingerprint(fingerprint_hash=fingerprint_id,
                description="",
                questionnaire=questionnaire,
                last_modification=timezone.now(),
                created=timezone.now(),
                owner=user_fk)
            fingerprint.save()

    return fingerprint

def deleteFingerprint(fingerprint_id, username):
    user= str(username)

    try:
        fingerprint = Fingerprint.objects.get(fingerprint_hash=fingerprint_id)

        should_delete = belongsUser(fingerprint, user)


        if username.is_superuser or should_delete == True:
            #print "Should be deleted"
            fingerprint.removed=True
            fingerprint.save()
            unindexFingerprint(fingerprint_id)

    except Fingerprint.DoesNotExist:
        print "Tried to delete fingerprint who doesnt exist"

def belongsUser(fingerprint, username):

    #print "username: "+username

    #print "owner: "+fingerprint.owner.email

    if fingerprint.owner.email == username:
        return True

    for share in fingerprint.shared.all():
        #print "shared: "+share.email
        if share.email == username:
            return True

    return False

def unindexFingerprint(fingerprint_id):
    c = CoreEngine()
    c.delete(fingerprint_id)


def is_if_yes_no(question):
    return question.type in 'choice-yesno' or \
            question.type in 'choice-yesnocomment' or \
            question.type in 'choice-yesnodontknow'

def indexFingerprint(fingerprint_id):
    try:
        fingerprint = Fingerprint.objects.get(fingerprint_hash=fingerprint_id)


        d = {}

        # Get parameters that are only on fingerprint
        # type_t
        d['id']=fingerprint_id
        d['type_t'] = fingerprint.questionnaire.slug
        d['date_last_modification_t'] = fingerprint.last_modification.strftime('%Y-%m-%d %H:%M:%S.%f')
        d['created_t'] = fingerprint.created.strftime('%Y-%m-%d %H:%M:%S.%f')

        d['user_t'] = unique_users_string(fingerprint)

        adicional_text = ""


        # Add answers
        answers = Answer.objects.filter(fingerprint_id=fingerprint)

        for answer in answers:
            # We try to get permissions preferences for this question
            permissions = getPermissions(fingerprint_id, QuestionSet.objects.get(id=answer.question.questionset.id))

            slug = answer.question.slug_fk.slug1

            if permissions.allow_indexing or slug == 'database_name':
                setProperFields(d, answer.question, slug, answer.data)
                if is_if_yes_no(answer.question) and 'yes' in answer.data:
                    adicional_text += answer.question.text+ " "
                if answer.comment != None:
                    d['comment_question_'+slug+'_t'] = answer.comment


        d['text_t']= generateFreeText(d) +  " " + adicional_text

        c = CoreEngine()

        results = c.search_fingerprint("id:"+fingerprint_id)
        if len(results) == 1:
            # Delete old entry if any
            c.delete(results.docs[0]['id'])

        c.index_fingerprint_as_json(d)

    # In case is a new one, create it
    except Fingerprint.DoesNotExist:
        print "-- ERROR: Can't find the fingerprint with hash "+fingerprint_id+" to export."

def unique_users_string(fingerprint):
    # user_t (owner + shared)
    # i don't know if the user is
    users = set()
    users.add(fingerprint.owner.username)
    for share in fingerprint.shared.all():
        users.add(share.username)

    users = list(users)
    users_string = users[0]

    for i in xrange(1, len(users)):
        users_string+= ' \\ ' + users[i]

    return users_string


def findName(fingerprint):
    name = ""
    try:
        name_ans = Answer.objects.get(question__slug_fk__slug1='database_name', fingerprint_id=fingerprint)

        name = name_ans.data

    except Answer.DoesNotExist:
        name ="Unnamed"

    return name


# GET permissions model
def getPermissions(fingerprint_id, question_set):

    if fingerprint_id == None or question_set == None:
        return None


    permissions = None
    try:
        permissions = QuestionSetPermissions.objects.get(fingerprint_id=fingerprint_id, qs=question_set)

    except QuestionSetPermissions.DoesNotExist:
        print "Does not exist yet, creating a new permissions object."
        permissions = QuestionSetPermissions(fingerprint_id=fingerprint_id, qs=question_set, visibility=0,
         allow_printing=True, allow_indexing=True, allow_exporting=True)
        permissions.save()

    except QuestionSetPermissions.MultipleObjectsReturned:
        print "Error retrieved several models for this questionset, its impossible, so something went very wrong."

    return permissions

def markAnswerRequests(user, fingerprint, question, answer_requests):

    this_requests = answer_requests.filter(question=question)

    for req in this_requests:
        # We set the request as fullfilled
        req.removed = True
        req.save()

        message = "User "+str(fingerprint.owner.get_full_name())+" answered some questions you requested on database "+str(findName(fingerprint))+"."

        sendNotification(timedelta(hours=12), req.requester, fingerprint.owner, 
            "fingerprint/"+fingerprint.fingerprint_hash+"/1/", message)

def intersect(answers, questionset):

    # i know, this would be simpler if we just had the __in query, but we could only do this
    # if we deleted entries on Answer, and i don't want to do that because of the versioning
    # (on field can be empty, be filled, be empty and be filled again), the version has a pointer to the answer
    # we can't go around deleting entries... is preferable to do the process of checking for emptyness in this query

    non_empty = []
    for ans in answers.filter(question__in=questionset.questions()):
        if ans.data != None and ans.data != '':
            non_empty.append(ans)

    return non_empty

# Set new permissions for a questionset, based on a post request
def setNewPermissions(request):

    if(request == None or not request.POST):
        return False

    id = request.POST['_qs_perm']

    if(id != None):

        try:
            this_permissions                = QuestionSetPermissions.objects.get(id=id)

            this_permissions.visibility     = int(request.POST['_qs_visibility'])
            this_permissions.allow_printing = (request.POST['_qs_printing'] == 'true')
            this_permissions.allow_indexing = (request.POST['_qs_indexing'] == 'true')
            this_permissions.allow_exporting= (request.POST['_qs_exporting'] == 'true')

            this_permissions.save()

            return True

        except QuestionSetPermissions.DoesNotExist:
            print "Can't save this since, there's no permissions object to this questionset yet."
        except QuestionSetPermissions.MultipleObjectsReturned:
            print "Can't save this since there's several objects for this questionset permissions (should be only one)"


    return False

def extract_answers(request2, questionnaire_id, question_set, qs_list):


    question_set2 = question_set
    request = request2
    # Extract files if they exits
    try:
        if request.FILES:
            for name, f in request.FILES.items():
                handle_uploaded_file(f)
    except:
        pass

    qsobjs = QuestionSet.objects.filter(questionnaire=questionnaire_id)
    questionnaire = qsobjs[0].questionnaire

    sortid = 0

    if request.POST:
        try:
            question_set = request.POST['active_qs']
            sortid = request.POST['active_qs_sortid']
            fingerprint_id = request.POST['fingerprint_id']
        except:
            for qs in qsobjs:
                if qs.sortid == int(sortid):
                    question_set = qs.pk
                    break

    expected = []
    for qset in qsobjs:
        questions = qset.questions()
        for q in questions:
            expected.append(q)

    items = request.POST.items()
    extra = {} # question_object => { "ANSWER" : "123", ... }
    extra_comments = {}
    extra_fields = {}
    # this will ensure that each question will be processed, even if we did not receive
    # any fields for it. Also works to ensure the user doesn't add extra fields in
    '''for x in expected:
        items.append((u'question_%s_Trigger953' % x.number, None))
    '''
    # generate the answer_dict for each question, and place in extra
    for item in items:
        key, value = item[0], item[1]
        if key.startswith('comment_question_'):
            continue
        if key.startswith('question_'):
            answer = key.split("_", 2)
            question = get_question(answer[1], questionnaire)
            if not question:
                logging.warn("Unknown question when processing: %s" % answer[1])
                continue
            extra[question] = ans = extra.get(question, {})
            if (len(answer) == 2):
                ans['ANSWER'] = value
            elif (len(answer) == 3):
                ans[key] = value
            else:
                print "Poorly formed form element name: %r" % answer
                logging.warn("Poorly formed form element name: %r" % answer)
                continue
            extra[question] = ans



            comment_id = "comment_question_"+question.number#.replace(".", "")
            try:
                if request.POST and request.POST[comment_id]!='':
                    #comment_id_index = "comment_question_"+question.slug
                    comment_id_index = "comment_question_"+question.slug_fk.slug1
                    extra_comments[question] = request.POST[comment_id]
                    extra_fields[comment_id_index+'_t'] = request.POST[comment_id]
            except KeyError:
                pass
    errors = {}

    #print "Extra comments"
    #print extra_comments

    # Verification of qprocessor answers
    def verify_answer(question, answer_dict):

        type = question.get_type()

        if "ANSWER" not in answer_dict:
            answer_dict['ANSWER'] = None
        answer = None
        if type in Processors:
            answer = Processors[type](question, answer_dict) or ''
        else:
            print AnswerException("No Processor defined for question type %s" % type)

        return True

    active_qs_with_errors = False

    for question, ans in extra.items():

        '''if u"Trigger953" not in ans:
            logging.warn("User attempted to insert extra question (or it's a bug)")
            continue
        '''
        try:
            cd = question.getcheckdict()

            depon = cd.get('requiredif', None) or cd.get('dependent', None)

            verify_answer(question, ans)

        except AnswerException, e:
            errors[question.number] = e
            print e

            if (str(question.questionset.id) == question_set):
                #print "active enable"
                active_qs_with_errors = True
        except Exception:
            logging.exception("Unexpected Exception")
            raise

    try:
        questions = question_set2.questions()

        questions_list = {}
        for qset_aux in qs_list:
            questions_list[qset_aux.id] = qset_aux.questions()

        qlist = []
        jsinclude = []      # js files to include
        cssinclude = []     # css files to include
        jstriggers = []
        qvalues = {}

        qlist_general = []

        for k in qs_list:
            qlist = []
            qs_aux = None
            for question in questions_list[k.id]:
                qs_aux = question.questionset
                Type = question.get_type()
                _qnum, _qalpha = split_numal(question.number)

                qdict = {
                    'template': 'questionnaire/%s.html' % (Type),
                    'qnum': _qnum,
                    'qalpha': _qalpha,
                    'qtype': Type,
                    'qnum_class': (_qnum % 2 == 0) and " qeven" or " qodd",
                    'qalpha_class': _qalpha and (ord(_qalpha[-1]) % 2 \
                                                     and ' alodd' or ' aleven') or '',
                }

                # add javascript dependency checks
                cd = question.getcheckdict()
                depon = cd.get('requiredif', None) or cd.get('dependent', None)
                if depon:
                    # extra args to BooleanParser are not required for toString
                    parser = BooleanParser(dep_check)

                    # qdict['checkstring'] = ' checks="%s"' % parser.toString(depon)

                    #It allows only 1 dependency
                    #The line above allows multiple dependencies but it has a bug when is parsing white spaces
                    qdict['checkstring'] = ' checks="dep_check(\'question_%s\')"' % depon

                    qdict['depon_class'] = ' depon_class'
                    jstriggers.append('qc_%s' % question.number)
                    if question.text[:2] == 'h1':
                        jstriggers.append('acc_qc_%s' % question.number)
                if 'default' in cd and not question.number in cookiedict:
                    qvalues[question.number] = cd['default']
                if Type in QuestionProcessors:

                    qdict.update(QuestionProcessors[Type](request2, question))
                    try:
                        qdict['comment'] = extra_comments[question]
                    except KeyError:
                        pass

                    if question.number in errors:
                        qdict["qprocessor_errors"] = errors[question.number].message

                    if 'jsinclude' in qdict:
                        if qdict['jsinclude'] not in jsinclude:
                            jsinclude.extend(qdict['jsinclude'])
                    if 'cssinclude' in qdict:
                        if qdict['cssinclude'] not in cssinclude:
                            cssinclude.extend(qdict['jsinclude'])
                    if 'jstriggers' in qdict:
                        jstriggers.extend(qdict['jstriggers'])

                qlist.append((question, qdict))

            if qs_aux == None:
                qs_aux = k
            qlist_general.append((qs_aux, qlist))
    except:
        raise

        ## HOT FIX for qvalues to work properly, THIS SHOULD BE FIXED IN THE CODE ABOVE

    qvalues = {}
    for question, qdict in qlist_general:
        for k, v in qdict:
            try:
                qval = v['qvalue']

                print str(k.number)+" - "+qval
                if qval != None and qval != '':

                    try:
                        cutzone = qval.index('#');
                        qvalues[k.number] = qval[0:cutzone]
                    except ValueError:
                        qvalues[k.number] = qval

            except KeyError:
                pass

    return (qlist_general, qlist, jstriggers, qvalues, jsinclude, cssinclude, extra_fields, len(errors)!=0)

def save_answers_to_csv(list_databases, filename):
    """
    Method to export answers of a given database to a csv file
    """
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="EMIF_Catalogue_%s_%s.csv"' % (filename, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

    if list_databases:
        writer = csv.writer(response, delimiter = '\t')
        writer.writerow(['DB_ID', 'DB_name', 'Questionset', 'Question', 'QuestionNumber', 'Answer', 'Date Last Modification'])
        for t in list_databases:
            id = t.id

            returned = createqsets(id, clean=False, changeSearch=True, noprocessing=False)

            qsets, name, db_owners, fingerprint_ttype  = returned

            qsets = attachPermissions(id, qsets)

            for (k, qs), permissions in qsets:
                if permissions.visibility == 0 and permissions.allow_exporting == True:
                    writeGroup(id, k, qs, writer, name, t)

        writer.writerow([id, name, "System", "Date", "99.0", t.date])
        writer.writerow([id, name, "System", "Date Modification", "99.1", t.date_modification])
        writer.writerow([id, name, "System", "Type", "99.2", t.type_name])
        writer.writerow([id, name, "System", "Type Identifier", "99.3", t.ttype])
    return response

def attachPermissions(fingerprint_id, qsets):
    zipper = qsets
    zipee = []

    for q, v in zipper.ordered_items():
        qpermissions = getPermissions(fingerprint_id, QuestionSet.objects.get(id=v.qsid))
        zipee.append(qpermissions)

    merged = zip(zipper.ordered_items(), zipee)

    return merged

def writeGroup(id, k, qs, writer, name, t):
    if (qs!=None and qs.list_ordered_tags!= None):
        list_aux = sorted(qs.list_ordered_tags)

        for q in list_aux:
            _answer = clean_str_exp(str(q.value))
            if (_answer == "" and q.ttype=='comment'):
                _answer = "-"
            writer.writerow([id, name, k.replace('h1. ', ''), clean_str_exp(str(q.tag)), str(q.number), _answer, q.lastChange])
