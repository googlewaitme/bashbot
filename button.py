from vk_api.keyboard import VkKeyboardColor


class ColorByName:
	def __init__(self):
		self.COLORS_BY_NAME = {	
			'white': VkKeyboardColor.PRIMARY,
			'red': VkKeyboardColor.NEGATIVE,
			'green': VkKeyboardColor.POSITIVE
		}

	def color_is_exist(self, color_name):
		return color_name in self.COLORS_BY_NAME
		
	def give_color_by_name(self, color_name):
		return self.COLORS_BY_NAME[color_name]
		

class Button:
	def __init__(self, name, color='white', type_bt='default'):
		self.color = VkKeyboardColor.PRIMARY
		self.set_color(color)
		self.name = name
		self.type = type_bt
	
	def set_color(self, color_name):
		color_by_name = ColorByName()
		if color_by_name.color_is_exist(color_name):
			self.color = color_by_name.give_color_by_name(color_name)		
		else:
			raise f'Button not {color_name} in colors'
