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
		
		Attributes:
			name: string, name of item
			price: int, price of item in us whole dollars
			description: string, description of item
			category: string, which category item belongs to
			images: list of links to image sources
			seller: string, the id of the user who's selling this item
			itemid: string. the itemid of this item
			quality: string, the condition of item (used, new, etc.)
			post_date: date, the day that this item was posted
			seller_name: string, the first name and last initial of the seller
			schoo: the school that the seller goes to
			seller_email: string, the seller's email address
			buyers: a list of people who are interested in buying the item
			available: boolean, represening if item is available for purchase
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