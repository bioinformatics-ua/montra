from django.contrib.auth.models import User
from newsletter.models import Subscription, Newsletter

def importUsers():

    try:
        newsl = Newsletter.objects.get(slug='emif-catalogue-newsletter')


        users = User.objects.all()

        for user in users:
            try:
                subscription = Subscription.objects.get(user=user,  newsletter=newsl)

            except Subscription.DoesNotExist:
                # create subscription if doesnt exist yet
                user_sub = Subscription(user=user,  newsletter=newsl)

                user_sub.subscribe()  

                user_sub.save()    

                print "-- Created subscription for emif newsletter to user "+str(user.username)

                pass

    except Newsletter.DoesNotExist:
        print "Problem finding default newsletter for emif"

importUsers()
