# proto type Quadtree class, used for checking collision faster. Somewhat tested.


class Quadtreenode(object):
	def __init__(self,parent,window_width,window_height,point,split):
		self.window_height = window_height
		self.window_width = window_width
		self.start_point = point
		self.split = split
		self.parent = parent
		self.upper_left = None
		self.upper_right = None
		self.lower_left = None
		self.lower_right = None

		self.char_contents = []
		self.enemy_contents = []
	def add_nodes(self):
		k= [self.start_point[0] + self.window_width/2,self.start_point[1]] 
		x = [self.start_point[0] + self.window_width/2, self.start_point[1] + self.window_height/2]
		j = [self.start_point[0], self.start_point[1] + self.window_height/2]
		self.upper_right = Quadtreenode(self,self.window_width/2,self.window_height/2,x,self.split -1)
		self.upper_left = Quadtreenode(self,self.window_width/2,self.window_height/2,j,self.split -1)
		self.lower_right = Quadtreenode(self,self.window_width/2,self.window_height/2,k,self.split -1)
		self.lower_left = Quadtreenode(self,self.window_width/2,self.window_height/2,self.start_point,self.split -1)
	def resize(self):
		if len(self.char_contents) + len(self.enemy_contents) > 3 and self.split > 0:
			self.add_nodes()
			for char in self.char_contents:
				self.insert_char(char)
			for enemy in self.enemy_contents:
				self.insert_enemy(enemy)
			self.char_contents = []
			self.enemy_contents = []

	def does_fit(self, object):
		upper_y = object.sprite.y + object.sprite.height
		lower_y = object.sprite.y
		upper_node_y = self.start_point[1] + self.window_height
		lower_node_y = self.start_point[1]
		upper_x = object.sprite.x + object.sprite.width
		lower_x = object.sprite.x
		upper_node_x = self.start_point[0] + self.window_width
		lower_node_x = self.start_point[0]
		k = (lower_y < lower_node_y < upper_y or lower_y < upper_node_y < upper_y or lower_node_y < lower_y < upper_node_y or lower_node_y < upper_y < upper_node_y ) and (lower_x < lower_node_x < upper_x or lower_x < upper_node_x < upper_x or lower_node_x < lower_x < upper_node_x or lower_node_x < upper_x < upper_node_x )
		return k
	def insert_char(self,object):
		if self.upper_left == None:			
			self.char_contents.append(object)
			self.resize()
		else:
			if self.upper_left.does_fit(object):
				self.upper_left.insert_char(object)
			if self.upper_right.does_fit(object):
				self.upper_right.insert_char(object)
			if self.lower_left.does_fit(object):
				self.lower_left.insert_char(object)
			if self.lower_right.does_fit(object):
				self.lower_right.insert_char(object)
	def insert_enemy(self,object):
		if self.upper_left == None:
			self.enemy_contents.append(object)
			self.resize()
		else:
			if self.upper_left.does_fit(object):
				self.upper_left.insert_enemy(object)
			if self.upper_right.does_fit(object):
				self.upper_right.insert_enemy(object)
			if self.lower_left.does_fit(object):
				self.lower_left.insert_enemy(object)
			if self.lower_right.does_fit(object):
				self.lower_right.insert_enemy(object)

	def get_lists(self,checks):
		if self.upper_left == None:
			if len(self.char_contents) > 0 and len(self.enemy_contents) > 0:
				checks.append([self.char_contents,self.enemy_contents])
				return checks
			else:
				return checks
		else:
			checks = self.upper_left.get_lists(checks)
			checks = self.upper_right.get_lists(checks)
			checks = self.lower_left.get_lists(checks)
			checks = self.lower_right.get_lists(checks)
			return checks
		return checks



class Quadtree(object):
	def __init__(self,size,point):
		self.root = Quadtreenode(None,size[0],size[1],point,3)
	def get_lists(self):
		checks = []
		checks = self.root.get_lists(checks)
		return checks
	def insert_char(self,object):
		self.root.insert_char(object)
	def insert_enemy(self,object):
		self.root.insert_enemy(object)



class sprite(object):
	def __init__(self,x,y,xs,ys):
		self.y = y
		self.x = x
		self.width = xs
		self.height = ys
class whatever(object):
	def  __init__(self,x,y,xs,ys):
		self.sprite = sprite(x,y,xs,ys)
