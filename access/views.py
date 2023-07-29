from .models import AlbumAccessRequest
from .forms import AlbumAccessRequestForm

from django.views.generic import CreateView

# class AccessRequestView(CreateView):
#     model = AlbumAccessRequest
#     template_name = 'album_access_request.html'
#     form_class = AlbumAccessRequestForm

#     def form_valid(self, form):

#         return super().form_valid(form)
