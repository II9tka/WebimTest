import requests
from random import choices as rand

from .models import FirstVisit


def get_user_friends(token, user_id):
    version = '5.21'
    fields = ('id', 'first_name', 'last_name', 'photo_200_orig')
    response = requests.get('https://api.vk.com/method/friends.get', params={
        'user_id': user_id,
        'access_token': token,
        'v': version,
        'fields': fields
    })
    try:
        return response.json()['response']['items']
    except KeyError:
        return {}


def get_data_visit(request, token, user_id):
    if not FirstVisit.objects.filter(user=request.user.id, url=request.path).exists():
        FirstVisit(user=request.user, url=request.path).save()
    try:
        if len(get_user_friends(token, user_id)) <= 1:
            return get_user_friends(token, user_id)
        return rand(get_user_friends(token, user_id), k=5)
    except IndexError:
        return None
