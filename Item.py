"""
Supporting Code for Frank's List,
an open source webapp for buying and
selling items across college campuses.

@author(s): 
Jasper Katzban, Olin '23
Jonas Kazlauskas, Olin '23
Kelly Yen, Olin '23
"""

from datetime import datetime

class Item:
	"""Class to represent an item to be listed"""

	def __init__(self, name, price, description, images, quality, user, tags=None): 
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
		self.quality = quality
		self.post_date = datetime.now()
		self.available = True

	def to_dict(self):

		items_dict={
            'name' : self.name,
            'price' : self.price,
            'description' : self.description,
            'images' : self.images,
            'seller' : self.seller,
            'tags' : self.tags,
            'post_date' : self.post_date,
			'available' : self.available,
			'quality' : self.quality,
        }
		
		return items_dict