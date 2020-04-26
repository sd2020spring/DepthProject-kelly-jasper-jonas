"""
Supporting Code for Frank's List,
an open source webapp for buying and
selling items across college campuses.

@author(s): 
Jasper Katzban, Olin '23
Jonas Kazlauskas, Olin '23
Kelly Yen, Olin '23
"""


import numpy as np
from datetime import datetime

class User:
	"""Class to represent the user"""

	def __init__(self, fname, lname, email, password, school, phone=None):
		"""Create a User objecta
		TODO: impelement database connection
		"""
		self.fname = fname
		self.lname = lname
		self.email = email
		self.phone = phone
		self.school = school
		self.password = password
		self.items_sold = []
		self.looking_for = []
		self.purchases = []
		self.saved_items = []
		self.pic = ''

	def to_dict(self):
		
		user_dict = {
			'fname' : self.fname,
			'lname' : self.lname,
			'email' : self.email,
			'phone' : self.phone,
			'school' : self.school,
			'password' : self.password,
			'items selling' : self.items_sold,
			'looking for' : self.looking_for,
			'previous purchase' : self.purchases,
			'saved items' : self.saved_items,
			'profile picture' : self.pic, 
		}
		return user_dict




