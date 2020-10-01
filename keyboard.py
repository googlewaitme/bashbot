from vk_api.keyboard import VkKeyboard
from button import Button

class Keyboard:
	def generate_keyboard(self, buttons, inline=False, one_time=False):
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


class BotKeyboard(Keyboard):
	def menu(self):
		new_question_but = Button('Новый вопрос')
		new_theory_but = Button('Новая теория')
		buttons = [[new_theory_but], [new_question_but]]
		return self.generate_keyboard(buttons)

	def question(self, question):
		buttons = list()
		if not 'answers' in question:
			return self.generate_keyboard(buttons)
		for answer in question['answers']:
			buttons.append([Button(answer)])
		return self.generate_keyboard(buttons)

	def return_key(self):
		buttons = [['Вернуться']]
