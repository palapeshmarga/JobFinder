from django import forms

class JobSearchForm(forms.Form):
    resume = forms.FileField(
        label="Upload Resume (PDF)",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'})
    )
    gemini_key = forms.CharField(
        label="Gemini API Key",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    rapid_key = forms.CharField(
        label="RapidAPI Key (Optional)",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    search_query = forms.CharField(
        label="Job Search Query",
        initial="Django Developer",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        label="Location",
        initial="Remote",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )