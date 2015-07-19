from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import TemplateView, View
from django.shortcuts import redirect


class HomePageTemplateView(TemplateView):
    template_name = 'home_page.html'


class ManualFeedUpdateView(View):
    def get(self, request, *args, **kwargs):
        call_command('xml_all')
        call_command('xml_cheapest')
        messages.add_message(request, messages.SUCCESS, 'Dokonane')
        return redirect(reverse('home-page'))