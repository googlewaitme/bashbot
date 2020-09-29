from .. import server_api

class Test_server_api:
	def setup_class(self):
		self.api = server_api.ServerApi()
		self.id = 'test_bashbot'
		self.api.request('remove_user', self.id)

	def teardown_class(self):
		pass

	def test_user_is_not_exist(self):
		assert not self.api.request('user_is_exist', self.id)

	def test_add_user(self):
		assert self.api.request('add_user', self.id)

	def test_user_is_exist(self):
		assert self.api.request('user_is_exist', self.id)

	def test_give_theory(self):
		assert self.api.request('give_theory', self.id)

	def test_give_question(self):
		assert self.api.request('give_question', self.id)

	def test_set_user_read_theory(self):
		assert self.api.request('set_user_read_theory', self.id, theory_id='2')

	def test_check_user_answer(self):
		assert self.api.request('check_user_answer', self.id, question_id='2', user_answer='2')

	def test_remove_user(self):
		assert self.api.request('remove_user', self.id)
