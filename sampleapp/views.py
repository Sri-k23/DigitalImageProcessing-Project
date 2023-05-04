from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from sampleapp.forms import EmployeeForm

from django.views.generic import DetailView
from sampleapp.models import Sampleapp


class EmployeeImage(TemplateView):

    form = EmployeeForm
    template_name = 'emp_image.html'

    def post(self, request, *args, **kwargs):

        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('emp_image_display', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class EmpImageDisplay(DetailView):
    model = Sampleapp
    template_name = 'emp_image_display.html'
    context_object_name = 'emp'
