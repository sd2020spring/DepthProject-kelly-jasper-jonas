"""
Supporting Code for Frank's List,
an open source webapp for buying and
selling items across college campuses.

@author(s): 
Jasper Katzban, Olin '23
"""

import numpy as np
from datetime import datetime

class User(object):
	"""Class to represent the user"""

	def __init__(self, fname, lname, email, phone, grad_year, school=None):
		"""Create a User objecta
		TODO: impelement database connection
		"""
		self.fname = fname
		self.lname = lname
		self.email = email
		self.phone = phone
		self.grad_year = grad_year
		self.school = school

	def __str__(self, verbose=False):
		print


class Item(object):
	"""Class to represent an item to be listed"""

	def __init__(self, name, price, description, images, user, tags=None): 
		"""Create an Item object with relevant attributes
		- is it better to contain attributes in a single object?
		TODO: implement database conenction
		"""
		self.name = name
		self.price = price
		self.description = description
		self.images = images
		self.seller = user.name
		self.tags = tags
		self.post_date = datetime.now()

	def __str__(self, verbose=False):
		"""Print out an item's attributes, useful for debugging"""
		print(f"Name: {self.name}")
		if verbose:
			print(f"Price: ${self.price}")
			print(f"Description: {self.description}")
			print(self.images)
			print(f"Seller: {self.user}")
			print(f"Tags: {tags}")
			print(f"{post_date}")

	def get(self, attribute):
		"""Return a specified attribute

		attribute: the attribute to pull as a string"""
		return self.attribute

	def update(self, attribute, value):
		"""Update changes to an object
		- this may be funky for images

		TODO: update actual database listing
		"""
		if self.attribute != value:
			self.attribute = value

	def remove(self):
		"""Delete item from database
		- can we use builtin .__remove__ for this?
		"""
		pass



def find_tags(query):
	"""Suggest tags as the user types them"""
	pass

"""
user:
name
email
phone
grad yr
items onsale
profile pic
school
looking for

item:
name
price
description
images
categories/tags
post date
seller user

stretch goals:

pull relevant images/info from
the web about an item upon entry into listing

ability to contact user within app or call them (like uber)


"""
