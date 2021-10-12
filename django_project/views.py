from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse


def redirect_view(request):
    response = redirect('/home/')
    return response


class NewLoginView(LoginView):
    def get_redirect_url(self):
        print(f'entroooou {self.request.method} 1')
        if self.request.method == "POST" and self.request.user.get_username()\
                and not self.request.user.has_changed_pw and not self.request.user.is_superuser :
            redirect_to = reverse("change_password")
        else:
            redirect_to = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name, '')
            )
        return redirect_to