from accounts.models import Profile, NavigationHistory
from django.contrib import admin
from django.contrib.auth.models import User
from adminplus.sites import AdminSitePlus

from django.shortcuts import render

from django.forms import ModelForm, ModelChoiceField

from django import forms
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from django.db.models import Count, Avg, Max, Min

from django.utils import timezone
import datetime

class NavigationAdmin(admin.ModelAdmin):
    list_display = ['user', 'path', 'date']
    search_fields = ['user__username','user__email','path']
    list_filter = ['user']

class ChoiceForm(forms.Form):
    user = forms.ModelChoiceField(User.objects.all())

class UserStatistics(View):
    template_name = 'admin/user_statistics.html'

    def get(self, request):
        form = ChoiceForm()

        history = NavigationHistory.objects.all()

        most_viewed = history.values('path').annotate(number_viewed=Count('path')).order_by('-number_viewed')[:15]

        session_time, average_time = self.getSessionTimes(history)

        views_time, average_views = self.getViewTimes(history)

        return render(request, self.template_name, {'choice': form, 'global': True, 
                                                    'most_viewed': most_viewed,
                                                    'session_time': session_time,
                                                    'session_average': average_time,
                                                    'views_time': views_time,
                                                    'views_average': average_views
                                                    })

    def post(self, request):
        user = request.POST.get('user', -1)

        if(user == ""):
            return self.get(request)

        form = ChoiceForm(initial = {'user': user})
        
        user_history = NavigationHistory.objects.filter(user=user)

        most_viewed = user_history.values('path').annotate(number_viewed=Count('path')).order_by('-number_viewed')[:15]

        session_time, average_time = self.getSessionTimes(user_history)

        views_time, average_views = self.getViewTimes(user_history)

        return render(request, self.template_name, {'choice': form, 'global': False,
                                                    'most_viewed': most_viewed,
                                                    'session_time': session_time,
                                                    'session_average': average_time,
                                                    'views_time': views_time,
                                                    'views_average': average_views
                                                    }) 

    def getSessionTimes(self, user_history):

        session_times = []
        average = 0
        d = timezone.now().date()
        end_date = (timezone.now()-datetime.timedelta(days=30)).date()

        delta = datetime.timedelta(days=1)
        while d >= end_date:
            
            user_day_history = user_history.filter(date__startswith=d)

            min = user_day_history.aggregate(Min('date'))['date__min']
            max = user_day_history.aggregate(Max('date'))['date__max']

            try:
                session = (max-min).total_seconds() // 3600

                average += session

                session_times.append({ 'label': d, 'value': session })
            except:
                session_times.append({ 'label': d, 'value': 0 })
                          
            d -= delta

        return [session_times, average/30]

    def getViewTimes(self, user_history):

        view_times = []
        average = 0
        d = timezone.now().date()
        end_date = (timezone.now()-datetime.timedelta(days=30)).date()

        delta = datetime.timedelta(days=1)
        while d >= end_date:
            
            user_day_history = user_history.filter(date__startswith=d)

            try:
                views = len(user_day_history)

                average += views

                view_times.append({ 'label': d, 'value': views })
            except:
                view_times.append({ 'label': d, 'value': 0 })
                          
            d -= delta

        return [view_times, average/30]

admin.site.register_view('user_statistics', view=login_required(staff_member_required(UserStatistics.as_view())))

admin.site.register(Profile)

admin.site.register(NavigationHistory, NavigationAdmin)
