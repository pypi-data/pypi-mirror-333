from django import forms

from doorkeeper.helpers import get_doorkeeper_setting


class DoorkeeperEntranceForm(forms.Form):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    doorkeeper_next_url = forms.CharField(label="Next URL", widget=forms.HiddenInput, required=False)

    NEXT_URL_FIELD_NAME = "doorkeeper_next_url"

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password != get_doorkeeper_setting("PASSWORD"):
            raise forms.ValidationError("Invalid password")
        return password
