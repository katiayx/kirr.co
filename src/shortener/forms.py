from django import forms

from .validators import validate_url, validate_dot_com

class SubmitUrlForm(forms.Form):
	url = forms.CharField(
			label='', 
			validators=[validate_url],
			widget= forms.TextInput(
					attrs={'placeholder':'Long URL',
							'class':'form-control'},
				)
			) #make sure this is a real URL

	# def clean(self):
	# 	"""related to form.is_valid() method called in views
	# 	clean_data -> it's real data and it works  

	# 	validating on the form"""
		
	# 	cleaned_data = super(SubmitUrlForm, self).clean()
	# 	print(cleaned_data)
	# 	url = cleaned_data.get('url')

	def clean_url(self):
		""" validating directly on the field, if this another 
		field that needs validation, another method needs to be
		written"""

		url = self.cleaned_data['url'] #clean() already extracted url, so we just need to grab it
		if "http" in url:
			return url
		return "http://" + url