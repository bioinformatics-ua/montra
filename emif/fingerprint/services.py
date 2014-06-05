from fingerprint.models import Fingerprint, Answer, FingerprintHead, AnswerChange
from questionnaire.models import Questionnaire
from django.contrib.auth.models import User

from searchengine.search_indexes import generateFreeText, setProperFields, CoreEngine

from django.utils import timezone    


def saveFingerprintAnswers(qlist_general, fingerprint_id, questionnaire, user, extra_fields=None, created_date=None):

    # Update or create fingerprint entry
    print "Updating fingerprint "+fingerprint_id
    fingerprint = updateFingerprint(fingerprint_id, questionnaire, user)

    # If no errors on getting the fingerprint, update/add the new questions
    if fingerprint != None:
        print "Getting answers"
        # i get them all, instead of a query for each, is probabily faster this way
        answers = Answer.objects.filter(fingerprint_id=fingerprint)

        # TO DO
        print "Updating answers "+fingerprint_id
        # For each response in qlist_general

        versionhead = None

        print "TO:"
        for qs_aux, qlist in qlist_general:
            for question, qdict in qlist:
                value = getAnswerValue(question, qdict)
                
                comment = getComment(question, extra_fields)

                #print question.slug_fk.slug1 + ": '"+value+"' Comment: " + str(comment)

                if value != None:
                    this_ans = None
                    try:
                        this_ans = Answer.objects.get(fingerprint_id=fingerprint, question=question)

                        current_value = this_ans.data
                        current_comment = this_ans.comment

                        # update existing answers
                        this_ans.data=value;

                        if comment != None:
                            this_ans.comment=comment;

                        print "UPDATE: "
                        print this_ans
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
                        print "NEW: "
                        print this_ans
                        this_ans.save()
                

        # format for answers : Answer(question=question, data=data, comment=comment, fingerprint_id=fingerprint_id) 

def getComment(question, extra_fields):

    try:
        comment = extra_fields['comment_question_'+question.slug_fk.slug1+"_t"]

        return comment
    except:
        pass

    return None

def getAnswerValue(question, qdict):
    try:
        choices = None
        value = None
        choices_txt = None
        if qdict.has_key('value'):
            value = qdict['value']

            if "yes" in qdict['value']:
                appending_text += question.text

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
        # raise
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
            print "Should be deleted"
            fingerprint.removed=True
            fingerprint.save()
            unindexFingerprint(fingerprint_id)

    except Fingerprint.DoesNotExist:
        print "Tried to delete fingerprint who doesnt exist"

def belongsUser(fingerprint, username):

    print "username: "+username

    print "owner: "+fingerprint.owner.email

    if fingerprint.owner.email == username:
        return True

    for share in fingerprint.shared.all():
        print "shared: "+share.email
        if share.email == username:
            return True

    return False

def unindexFingerprint(fingerprint_id):
    c = CoreEngine()
    c.delete(fingerprint_id)


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

        # Add answers
        answers = Answer.objects.filter(fingerprint_id=fingerprint)

        for answer in answers:
            setProperFields(d, answer.question, answer.question.slug_fk.slug1, answer.data)
            if answer.comment != None:
                d['comment_question_'+answer.question.slug_fk.slug1+'_t'] = answer.comment
            
        
        d['text_t']= generateFreeText(d)
        
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
    users.add(fingerprint.owner.email)
    for share in fingerprint.shared.all():
        users.add(share.email)

    users = list(users)
    users_string = users[0]

    for i in xrange(1, len(users)):
        users_string+= ' \\ ' + users[i]

    return users_string
