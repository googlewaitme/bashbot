import requests
import json

class ServerApi:
	URL_TEMPLATES = {
		'user_is_exist': 'user_is_exist/{user_id}/',
		'add_user': 'add_user/{user_id}/',
		'remove_user': 'remove_user/{user_id}/',
		"set_user_read_theory": 'set_user_read_theory/{user_id}/{theory_id}/',
		"check_user_answer": 'check_user_answer/{user_id}/{question_id}/{user_answer}/',
		'give_question': 'give_question/{user_id}/',
		'give_theory': 'give_theory/{user_id}/'
	}
	URL_BOOL_TYPES = ['add_user', 'user_is_exist', 'remove_user', 'set_user_read_theory']


	def __init__(self, base_url='http://127.0.0.1:5000/'):
		self.base_url = base_url
		self.params = dict()

	def request(self, method_name, user_id, question_id=None, theory_id=None, user_answer=None):
		self.params = {
			'method_name': method_name,
			'user_id': user_id,
			'question_id': question_id, 
			'theory_id': theory_id, 
			'user_answer': user_answer
		}
		url = self.make_url()
		data = self.give(url)
		if method_name in self.URL_BOOL_TYPES:
			return self.returnAsBool(data)
		else:
			return data
		
	def returnAsBool(self, data):
		return data['boolean']

	def give(self, url):
		full_url = self.base_url + url
		undecoded_json =  requests.get(full_url)
		decoded_json = json.loads(undecoded_json.text)
		return  decoded_json

	def make_url(self):
		assert self.params['method_name'] in self.URL_TEMPLATES
		method_name = self.params['method_name']
		template = self.URL_TEMPLATES[method_name]
		url = template.format(**self.params)
		return url
