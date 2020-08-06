from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver
from .models import PrivateLetter

@receiver(post_save,sender = PrivateLetter)
def send_chatNotification(sender,instance,**kwargs):
	print("notify test")
	verb = "收到一条消息"
	description = "您收到一条消息"
	notify.send(instance.sender,recipient=instance.receiver,verb=verb,
		action_object=instance.chat,description = description)