from vk_api.keyboard import VkKeyboardColor


class ColorByName:
	COLORS_BY_NAME = {
		'white': VkKeyboardColor.PRIMARY,
		'red': VkKeyboardColor.NEGATIVE,
		'green': VkKeyboardColor.POSITIVE,
		'gray': VkKeyboardColor.DEFAULT
	}

	def color_is_exist(color_name):
		return self.color_name in COLORS_BY_NAME
		
	def give_color_by_name(color_name):
		return self.COLORS_BY_NAME[color_name]
		

class Button:
	def __init__(self, name, color='white', type_bt='default'):
		self.color=VkKeyboardColor.DEFAULT
		self.set_color(color)
		self.name = name
		self.type = type_bt
	
	def set_color(self, color_name):
		if ColorByName.color_is_exist(color_name):
			self.color = ColorByName.give_color_by_name(color_name)		
		else:
			raise f'Button not {color_name} in colors'
