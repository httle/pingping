from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from ..models import FriendsSystem


register = template.Library()

@register.simple_tag
def get_if_friend(user1,user2):
    iffriend = FriendsSystem.objects.filter(Q(user1 = user1) | Q(user2 = user1)).filter(Q(user2 = user2) | Q(user1 = user2)).filter(ifprocess=1)
    if(iffriend):
        if(iffriend[0].agree==1):
        	status = 1
        else:
        	status = 0
    else:
        status = 0
    return status




# @register.simple_tag
# def get_like_count(obj):
#     content_type = ContentType.objects.get_for_model(obj)
#     like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
#     return like_count.liked_num

# @register.simple_tag(takes_context=True)
# def get_like_status(context, obj):
#     content_type = ContentType.objects.get_for_model(obj)
#     user = context['user']
#     if not user.is_authenticated:
#         return ''
#     if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
#         return 'active'
#     else:
#         return ''

# @register.simple_tag
# def get_content_type(obj):
#     content_type = ContentType.objects.get_for_model(obj)
#     return content_type.model