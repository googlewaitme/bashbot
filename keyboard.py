from vk_api.keyboard import VkKeyboard
from button import Button

def generate_keyboard(buttons, inline=False, one_time=False):
	"""
		Structure buttons:
		[
			[Button, Button],
			[Button, Button, Button],
			[Button]
			...
		]
		function return VkKeyboard
	"""
	if not buttons:
		return VkKeyboard.get_empty_keyboard()
	keyboard = VkKeyboard(inline=inline, one_time=one_time)
	for i in range(len(buttons)):
		for button in buttons[i]:
			keyboard.add_button(label=button.name, color=button.color)
		if i < len(buttons)-1:
			keyboard.add_line()
	return keyboard.get_keyboard()
