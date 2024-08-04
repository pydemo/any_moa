import  sys, json, codecs
import re



from os.path import isfile


e=sys.exit


class Config(object): 
	
	def __init__(self, **kwargs):
		self.home=None

