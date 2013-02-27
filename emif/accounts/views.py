import random

try:
    from hashlib import sha1 as sha_constructor
except ImportError:
    from django.utils.hashcompat import sha_constructor

from django import forms
from django.utils.translation import ugettext_lazy as _

from userena.forms import SignupForm
from userena.utils import get_user_model
from django_countries.countries import COUNTRIES


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

    def __init__(self, *args, **kw):
        """
        A bit of hackery to get the added fields at the top of the
        form instead at the end.

        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # Delete the username field
        del self.fields['username']

        # Put the new fields at the top
        new_order = self.fields.keyOrder[:-4]
        new_order.insert(0, 'first_name')
        new_order.insert(1, 'last_name')
        new_order.insert(2, 'country')
        new_order.insert(3, 'organization')
        self.fields.keyOrder = new_order

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
        user_profile.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user
