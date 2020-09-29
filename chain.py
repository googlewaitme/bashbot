from abc import ABC, abstractmethod
from server_api import ServerApi
from models import User


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
		if not api.request('user_is_exist', request.user_id):
			api.request('add_user', request.user_id)
		return super().handle(request)


class UserIsExistInDataBaseHandler(AbstractHandler):
	def handle(self, request):
		if not self.user_is_exist():
			User.create(user_id=request.user_id)
		return super().handle(request)

	def user_is_exist(self, request):
		query = User.select().where(User.user_id==request.user_id)
		users = list(query)
		return bool(users)

		


class CheckUserAnswerHandler(AbstractHandler):
	def handle(self, request):
		if self.user_answering(request):
			data = api.request(
				method_name='check_user_answer', 
				user_id=request.user_id, 
				question_id=self.question_id, 
				user_answer=request.text
			)
			return self.make_data(data)
		else:
			return super().handle(request)


	def user_answering(self, request):
		user_model = User.get(User.user_id==request.user_id)
		return user_model.status == 'question'

	def make_data(self, data):
		# TODO keyboards
		# TODO send right answer or no
		message = dict()
		if data['user_answer_is_right']:
			message['message'] = 'Ваш ответ правильный'
		else:
			message['message'] = 'Ваш ответ не правильный, попробуйте еще раз'

		return message


class SendQuestionHandler(AbstractHandler):
	pass


class SendTheoryHandler(AbstractHandler):
	pass

class RemoveUserHandler(AbstractHandler):
	pass
