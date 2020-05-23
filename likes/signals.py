import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from notifications.signals import notify
from .models import LikeRecord


@receiver(post_save, sender=LikeRecord)
def send_notification(sender, instance, **kwargs):
    # 发送站内消息
    if instance.content_type.model == 'blog':
        target=instance.content_object
        verb = '{0} 点赞了你的《{1}》'.format(instance.user.username, target.title)
    elif instance.content_type.model == 'comment':
        # 回复
        comment = instance.content_object
        target = comment
        verb = '{0} 点赞了你的评论“{1}”'.format(
                instance.user.username, 
                strip_tags(comment.text)
            )
    recipient = instance.content_object.get_user()
    url = instance.content_object.get_url()+"#comment_" + str(target.pk)
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance,url=url)