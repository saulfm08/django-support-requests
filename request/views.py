from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import *

# Create your views here.
class FormRequest(LoginRequiredMixin, TemplateView):
    template_name = 'request_form.html'

    def get_context_data(self, **kwargs):
        context = super(FormRequest, self).get_context_data(**kwargs)     

        print(f"ln 15, request: {self.request.method}")

        return context

class RequestList(LoginRequiredMixin, TemplateView):
    template_name = 'request_list.html'

    def get_context_data(self, **kwargs):
        context = super(RequestList, self).get_context_data(**kwargs)     

        print(f"ln 25, request: {self.request.method}")
        print(f"ln 26, self.request.user: {self.request.user} {self.request.user.is_superuser } ")

        if self.request.user.is_superuser:
            print(f"User {self.request.user} is superuser; It can view all requests")
            context['results']  = f"User {self.request.user} is superuser; It can view all requests..."
            context['requests'] = Request.objects.all()
            
        else:
            print(f"User {self.request.user} is NOT superuser; It can view only its requests")
            context['results']  = f"User {self.request.user} is NOT superuser; It can view only its own requests..."
            context['requests'] = Request.objects.get(requester=self.request.user)

        return context

@login_required
def post_request(request):

    print(f"ln 43, request: {request.method}")
    if request.method == "POST":
        print(f"Request Title: {request.POST.get('req_title')}")
        print(f"Request Type: {request.POST.get('req_type')}")
        print(f"Request Priority: {request.POST.get('req_priority')}")
        print(f"Request User: {request.POST.get('req_user')}")
        print(f"Request req_body: <start>{request.POST.get('req_body')}<end>")

        req_obj = Request()
        req_obj.req_title = request.POST.get('req_title')
        req_obj.req_type  = request.POST.get('req_type')
        req_obj.req_body  = request.POST.get('req_body')
        req_obj.requester = request.user

        print(f"ln 57, Save Request: {req_obj.save()}")

    return HttpResponseRedirect('/?success=True')