from django.db import models
from .states import INDIAN_STATES

class StateField(models.CharField):
	def__init__(self,*args,**kwargs):
		kwargs["max_length"]=2 #use State Code
		kwargs["choices"]=INDIAN_STATES
		super(),__init__(*args, **kwargs)