from django.views.generic import ListView

from allauth.socialaccount.models import SocialAccount, SocialToken

from .services import get_data_visit
from .models import FirstVisit


class MainPageView(ListView):
    context_object_name = 'vk_profile'

    def get_user(self):
        return self.request.user

    def get_queryset(self):
        if self.get_user().is_authenticated and not self.get_user().is_superuser:
            return SocialAccount.objects.filter(user=self.request.user)

    def get_vk_id(self):
        return SocialAccount.objects.get(user=self.get_user()).uid

    def get_access_token(self):
        return SocialToken.objects.get(account__user=self.get_user().id, account__provider='vk')

    def check_visit(self):
        if FirstVisit.objects.filter(user=self.get_user().id, url=self.request.path).exists():
            return False
        return True

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data()
        try:
            if self.get_user().is_authenticated:
                context['first_visit'] = self.check_visit()
                context['my_friends'] = get_data_visit(self.request, self.get_access_token(), self.get_vk_id())
            return context
        except SocialToken.DoesNotExist:
            pass

    def get_template_names(self):
        if self.get_user().is_authenticated:
            return ["vk_profile/about_account.html"]
        return ["vk_profile/main_page.html"]