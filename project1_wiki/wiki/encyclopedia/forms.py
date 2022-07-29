from django import forms


# for create.html
class create_page_form(forms.Form):
    title = forms.CharField(label="Title", max_length=100, min_length=1, strip=True,
                            widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(label="Markdown Content", min_length=1, strip=True,
                            widget=forms.Textarea(attrs={'class':'form-control'}))


# for edit.html
class edit_page_form(forms.Form):
    content = forms.CharField(label="Markdown Content", min_length=1, strip=True,
                            widget=forms.Textarea(attrs={'class':'form-control'}))
