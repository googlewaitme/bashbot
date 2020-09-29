from config import longpoll, vk, VkEventType
from work import Work 

worker = Work()

for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
		if event.from_user:
			worker.set_event(event)
			worker.main()
