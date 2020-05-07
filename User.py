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

class User:
	"""Class to represent the user"""

	def __init__(self, fname, lname, email, password, school, grad_year, profilepic, phone=None):
		"""Create a User object

		Attributes: 
			fname: string, first name of user
			lname: string, last name of user
			email: string, user's valid school email
			phone: string, optional, user's phone number
			school: string, the college the student attends
			password: string, the hashed version of the password user picked
			grad_year: int, the year user will graduate 
			items_sold: A list of items user sold in past
			looking_for: a list of keywords or categories that user's looking for. Will be used to send notification to user
			purchases: a list of items users bought in the past
			saved_items: list of of itmes user's interested in buying (aka wishlsit)
			pic: string, link to image source of profile picture
		"""
		self.fname = fname
		self.lname = lname
		self.email = email
		self.phone = phone
		self.school = school
		self.password = password
		self.grad_year = grad_year
		self.items_sold = []
		self.looking_for = []
		self.purchases = []
		self.saved_items = []
		self.pic = [profilepic]

	def to_dict(self):
		
		user_dict = {
			'fname' : self.fname,
			'lname' : self.lname,
			'email' : self.email,
			'phone' : self.phone,
			'school' : self.school,
			'password' : self.password,
			'selling' : self.items_sold,
			'looking_for' : self.looking_for,
			'purchases' : self.purchases,
			'saved_items' : self.saved_items,
			'profile_pic' : self.pic, 
			'grad_year' : self.grad_year,
		}
		return user_dict




