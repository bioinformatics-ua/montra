import random

try:
    from hashlib import sha1 as sha_constructor
except ImportError:
    from django.utils.hashcompat import sha_constructor

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

import userena.views
from userena.forms import SignupForm, EditProfileForm
from userena.utils import get_user_model
from django_countries.countries import COUNTRIES

from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Profile
from questionnaire.models import Questionnaire

from userena.utils import get_profile_model, get_user_model
from userena.decorators import secure_required
from guardian.decorators import permission_required_or_403
from django.shortcuts import redirect, get_object_or_404

options = (
        (5, '5'),
        (10, '10'),
        (25, '25'),
        (50, '50'),
        (-1, 'All'),
)

class SignupFormExtra(SignupForm):
    """
    A form to add extra fields to the signup form.
    """
    first_name = forms.CharField(label=_('First name'),
                                 max_length=30,
                                 required=True)
    last_name = forms.CharField(label=_('Last name'),
                                max_length=30,
                                required=True)
    country = forms.ChoiceField(COUNTRIES, required=True)

    organization = forms.CharField(label=_('Organization'),
                                   max_length=255,
                                   required=True)

    profiles = forms.ModelMultipleChoiceField(label=_('I am a (select all that apply):'),
                                                required=True,
                                                queryset=Profile.objects.all(),
                                                widget=forms.CheckboxSelectMultiple())


    interests = forms.ModelMultipleChoiceField(label=_('I am interested in (select all that apply):'),
                                                required=True,
                                                queryset=Questionnaire.objects.filter(disable='False'),
                                                widget=forms.CheckboxSelectMultiple())

    paginator = forms.ChoiceField(label=_('Select default value for paginations:'),
                                        choices = options
                                    )

    mail_news = forms.BooleanField(label=_('Receive weekly newsletter e-mail with database updates ?'),
                                    required=False, initial=True
                                    )

    mail_not = forms.BooleanField(label=_('Receive all notifications also over e-mail ?'),
                                    required=False, initial=False
                                    )

    def __init__(self, *args, **kw):
        """
        A bit of hackery to get the added fields at the top of the
        form instead at the end.

        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # Delete the username field
        del self.fields['username']

        # Put the new fields at the top

        if Profile.objects.all().count() and Questionnaire.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'email', 'password1', 'password2', 'profiles', 'interests', 'paginator','mail_news', 'mail_not']
        elif Profile.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'email', 'password1', 'password2', 'profiles', 'paginator', 'mail_news', 'mail_not']
        elif Questionnaire.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'email', 'password1', 'password2', 'interests','paginator', 'mail_news', 'mail_not']
        else:
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'email', 'password1', 'password2', 'paginator','mail_news', 'mail_not']

    def save(self):
        """
        Override the save method to save additional fields to the user profile
        and override username with email.

        """
        # Use trimmed email as username
        username = self.cleaned_data['email'][:30]
        try:
            get_user_model().objects.get(username__iexact=username)
        except get_user_model().DoesNotExist:
            pass
        else:  # Fallback to randomly assigned username
            while True:
                username = sha_constructor(str(random.random())).hexdigest()[:5]
                try:
                    get_user_model().objects.get(username__iexact=username)
                except get_user_model().DoesNotExist:
                    break

        self.cleaned_data['username'] = username


        # First save the parent form and get the user.
        new_user = super(SignupFormExtra, self).save()

        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        user_profile = new_user.get_profile()
        user_profile.country = self.cleaned_data['country']
        user_profile.organization = self.cleaned_data['organization']
        try:
            user_profile.paginator = int(self.cleaned_data['paginator'])
        except KeyError:
            user_profile.paginator = 5

        try:
            user_profile.mail_news = self.cleaned_data['mail_news']
        except KeyError:
            user_profile.mail_news = True

        try:
            user_profile.mail_not = self.cleaned_data['mail_not']
        except KeyError:
            user_profile.mail_not = False

        # Add selected profiles
        if (Profile.objects.all().count()):
            selected_profiles = self.cleaned_data['profiles']
            for sp in selected_profiles:
                prof = Profile.objects.get(name=sp)
                user_profile.profiles.add(prof)

        # Add selected interests
        if (Questionnaire.objects.all().count()):
            selected_interests = self.cleaned_data['interests']
            for inter in selected_interests:
                i = Questionnaire.objects.get(name=inter)
                user_profile.interests.add(i)

        user_profile.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user
class EditProfileFormExtra(EditProfileForm):

    profiles = forms.ModelMultipleChoiceField(label=_('I am a (select all that apply):'),
                                                required=True,
                                                queryset=Profile.objects.all(),
                                                widget=forms.CheckboxSelectMultiple())

    interests = forms.ModelMultipleChoiceField(label=_('I am interested in (select all that apply):'),
                                                required=True,
                                                queryset=Questionnaire.objects.filter(disable='False'),
                                                widget=forms.CheckboxSelectMultiple())

    paginator = forms.ChoiceField(label=_('Select default value for paginations:'),
                                        choices = options
                                    )
    mail_news = forms.BooleanField(label=_('Receive weekly newsletter e-mail with database updates ?'),
                                                required=False,

                                    )

    mail_not = forms.BooleanField(label=_('Receive all notifications also over e-mail ?'),
                                                required=False,
                                    )

    def __init__(self, *args, **kw):
        super(EditProfileFormExtra, self).__init__(*args, **kw)
        del self.fields['mugshot']
        del self.fields['privacy']

        if Profile.objects.all().count() and Questionnaire.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'profiles', 'interests', 'paginator', 'mail_news', 'mail_not']
        elif Profile.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'profiles', 'paginator', 'mail_news', 'mail_not']
        elif Questionnaire.objects.all().count():
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'interests', 'paginator', 'mail_news', 'mail_not']
        else:
            self.fields.keyOrder = ['first_name', 'last_name', 'country', 'organization', 'paginator']

# Prevent access to edit by not logged in users

@secure_required
def profile_edit(request,
                 edit_profile_form=EditProfileFormExtra,
                 template_name='userena/profile_form.html',
                 success_url=settings.BASE_URL + 'wherenext',
                 extra_context=None, **kwargs):

    if request.user.is_authenticated():
        username = request.user.username
        user = get_object_or_404(get_user_model(),
                                 username__iexact=username)

        profile = user.get_profile()

        user_initial = {'first_name': user.first_name,
                        'last_name': user.last_name}

        form = edit_profile_form(instance=profile, initial=user_initial)

        if request.method == 'POST':
            form = edit_profile_form(request.POST, request.FILES, instance=profile,
                                     initial=user_initial)

            if form.is_valid():
                profile = form.save()
                return redirect(success_url)

        if not extra_context: extra_context = dict()
        extra_context['form'] = form
        extra_context['profile'] = profile
        extra_context['request'] = request
        return userena.views.ExtraContextTemplateView.as_view(template_name=template_name,
            extra_context=extra_context)(request)

    return userena.views.signup(request, **kwargs)

# def profile_edit(request, **kwargs):
#     if request.user.is_authenticated():
#         extra_content = dict()
#         extra_content['request'] = request
#         return userena.views.profile_edit(request, username=request.user.username, extra_content=extra_content, **kwargs)

#     return userena.views.signup(request, **kwargs)

# Prevent access to signup/signin pages by logged in users
def signup(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.BASE_URL)

    return userena.views.signup(request, **kwargs)


def signin(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.BASE_URL)

    return userena.views.signin(request, **kwargs)
