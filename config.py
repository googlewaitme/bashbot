import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = '7eaa97e3703e92bae3d2fdb23ebbe570b0984294546537ddc25ec21130a04a0fc8b0416ac1e58f5583641' 

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
