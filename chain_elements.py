from abc import ABC, abstractmethod
from server_api import ServerApi
from models import User
from constants import *
from keyboard import BotKeyboard

# Сделать так, чтобы если вопросов больше не осталось, то у пользователя было просто меню

keyboard = BotKeyboard()
api = ServerApi()


class Handler(ABC):
	@abstractmethod
	def set_next(self, handler):
		pass 

	@abstractmethod
	def handle(self, request):
		pass


class AbstractHandler(Handler):
	_next_handler = None

	def set_next(self, handler):
		self._next_handler = handler 
		return handler

	@abstractmethod
	def handle(self, request):
		if self._next_handler:
			return self._next_handler.handle(request)
		return None


class UserIsExistOnServerHandler(AbstractHandler):
	def handle(self, request):
		print('user_is_exist server')
		if not api.request('user_is_exist', request.user_id):
			api.request('add_user', request.user_id)
		return super().handle(request)


class UserIsExistInDataBaseHandler(AbstractHandler):
	def handle(self, request):
		print('user_is_exist bd')
		if not self.user_is_exist(request):
			User.create(user_id=request.user_id)
		return super().handle(request)

	def user_is_exist(self, request):
		query = User.select().where(User.user_id==request.user_id)
		users = list(query)
		return bool(users)


class CheckUserStartHandler(AbstractHandler):
	def handle(self, request):
		if request.text in BOT_START_TRIGGERS:
			return self.make_data(request)
		else:
			return super().handle(request)
	
	def make_data(self, request):
		message = dict()
		message['message'] = FIRST_MESSAGE_FOR_NEW_USERS
		message['keyboard'] = keyboard.menu()
		return message


class CheckUserAnswerHandler(AbstractHandler):
	def handle(self, request):
		print('check_user_answer')
		if self.user_answering(request):
			self.request = request
			data = api.request(
				method_name='check_user_answer', 
				user_id=request.user_id, 
				question_id=self.give_question_id(), 
				user_answer=request.text
			)
			return self.make_data(data)
		else:
			return super().handle(request)

	def user_answering(self, request):
		user_model = User.get(User.user_id==request.user_id)
		return user_model.status == 'question'

	def give_question_id(self):
		user_model = User.get(User.user_id==self.request.user_id)
		return user_model.question_id

	def update_user_status(self):
		query = User.update({User.status: 'ok'}).where(User.user_id==self.request.user_id)
		query.execute()

	def make_data(self, data):
		message = dict()
		if data['user_answer_is_right']:
			message['message'] = 'Ваш ответ правильный'
			message['keyboard'] = keyboard.menu()
			self.update_user_status()
		else:
			message['message'] = 'Ваш ответ не правильный, попробуйте еще раз'
		return message


class SendQuestionHandler(AbstractHandler):
	def handle(self, request):
		print('sendquestion')
		if request.text not in NEW_QUESTION_TRIGGERS:
			return super().handle(request)
		
		data = self.new_question(request)
		print(data)
		if data['id'] == -1:
			return self.user_have_passed_all_questions()

		self.save_question_id_in_user(request, data['id'])
		return self.make_data(data)
	

	def new_question(self, request):
		data = api.request(
			method_name='give_question',
			user_id=request.user_id
		) 
		return data

	def user_have_passed_all_questions(self):
		message = {
			'message': 'Вопросов больше нет! Изучите новую тему, нажав на нужную кнопку',
			'keyboard': keyboard.menu()	
		}
		return message

	def save_question_id_in_user(self, request, question_id):
		query = (User
			.update({User.question_id: question_id,
				User.status: 'question'})
			.where(User.user_id==request.user_id)
		)
		query.execute()

	def make_data(self, data):
		message = dict()
		message['message'] = data['text']
		message['keyboard'] = keyboard.question(data)
		return message



class SendTheoryHandler(AbstractHandler):
	def handle(self, request):
		print('send theory')
		if request.text not in NEW_THEORY_TRIGGERS:
			return super().handle(request)
		data = self.new_theory(request)
		return self.make_data(data)

	def new_theory(self, request):
		data = api.request(
			method_name='give_theory',
			user_id=request.user_id
		)
		api.request(
			method_name='set_user_read_theory',
			user_id=request.user_id,
			theory_id=data['id']
		)
		return data

	def make_data(self, data):
		message = {
			'message': f"{data['theme']}\n\n{data['text']}",
			'keyboard': keyboard.menu()
		}
		return message


class RemoveUserHandler(AbstractHandler):
	def handle(self, request):
		print('remove user')
		if request.text == 'remove':
			data = api.request(
				method_name='remove_user',
				user_id=request.user_id
			)
			return {'message': 'Ваш аккаунт удален', 'keyboard': keyboard.return_key()}
		else:
			return super().handle(request)


class CommandIsNotFound(AbstractHandler):
	def handle(self, request):
		print('is_not_found')
		return {'message': 'Я вас не понял', 'keyboard': keyboard.menu()}
