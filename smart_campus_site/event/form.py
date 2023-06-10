from django import forms

class loc_form(forms.Form):
    loc_list= ['W311a','W311b','W311-H1','W311-H2','W311-H3','W311d-Z1','W311d-Z2']
    location = forms.ChoiceField(choices=loc_list)
    