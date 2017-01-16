from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_url(value):
	url_validator = URLValidator()
	reg_val = value
	if "http" in reg_val:
		new_value = reg_val
	else:
		new_value = "http://" + value 
	
	try: #validate input 
		url_validator(new_value)
	except: #if url not valid
		raise ValidationError("Invalid input")
	return new_value

def validate_dot_com(value):
	if not ".com" in value:
		raise ValidationError("no .com, invalid input")
	return value