import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os

token = os.environ.get('API_KEY')

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
