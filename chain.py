from chain_elements import *


def give_chain():
	handlers = [
		UserIsExistOnServerHandler(),
		UserIsExistInDataBaseHandler(),
		CheckUserAnswerHandler(),
		SendQuestionHandler(),
		SendTheoryHandler(),
		RemoveUserHandler(),
		CommandIsNotFound()
	]

	for i in range(6):
		handlers[i].set_next(handlers[i + 1])	
	chain = handlers[0]
	return chain
