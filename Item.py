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

	def __init__(self, name, price, description, category, images, quality, userid, sellername, selleremail, school, itemid): 
		"""Create an Item object with relevant attributes
		- is it better to contain attributes in a single object?
		TODO: implement database conenction
		"""
		self.name = name
		self.price = price
		self.description = description
		self.category = category
		self.images = images
		self.seller = userid
		self.itemid = itemid
		self.quality = quality
		self.post_date = datetime.now()
		self.seller_name = sellername
		self.school = school
		self.seller_email = selleremail
		self.buyers = []
		self.available = True

	def to_dict(self):

		items_dict={
            'name' : self.name,
            'price' : self.price,
            'description' : self.description,
            'category' : self.category,
            'images' : self.images,
            'seller' : self.seller,
			'seller_email' : self.seller_email,
			'seller_name' : self.seller_name,
			'school' : self.school,
            'id' : self.itemid,
            'post_date' : self.post_date,
			'available' : self.available,
			'quality' : self.quality,
			'buyers' : self.buyers,
        }
		
		return items_dict