import mimetypes
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.utils.encoding import smart_str
from django.views.generic import TemplateView, View


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class HomePageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'home_page.html'


class ManualFeedUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        call_command('xml_all')
        call_command('xml_cheapest')
        messages.add_message(request, messages.SUCCESS, 'Dokonane')
        return redirect(reverse('home-page'))


def download(request, file_name):
    if file_name not in settings.VALID_FILE_NAMES:
        raise Http404
    file_path = os.path.join(settings.XML_FEED_DIR, file_name)
    file_wrapper = FileWrapper(open(file_path, 'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % \
                                      smart_str(file_name)
    return response