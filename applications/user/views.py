from django.shortcuts import render
from rest_framework.decorators import action

from component.drf.viewsets import GenericViewSet


class UserInfoViewSets(GenericViewSet):
    @action(methods=["GET"], detail=False)
    def info(self, request, *args, **kwargs):
        username = request.user.username
        if username:
            user_data = {
                "username": username,
                "is_login": True
            }
        else:
            user_data = {
                "username": "游客",
                "is_login": False
            }
        return self.success_response(data=user_data)
