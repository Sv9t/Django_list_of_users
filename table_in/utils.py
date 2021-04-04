from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import *
from django.urls import reverse
from django.contrib import messages

# render and save pdf
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, pk):
        obj = self.model.objects.get(pk__iexact=pk)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, pk):
        obj = self.model.objects.get(pk__iexact=pk)
        bound_form = self.model_form(request.POST, request.FILES, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('list_users_url')
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, pk):
        obj = self.model.objects.get(pk__iexact=pk)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, pk):
        obj = self.model.objects.get(pk__iexact=pk)
        obj.delete()
        return redirect(reverse(self.redirect_url))


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    link_callback = r'C:\Python_scripts\!PROD\table_one\media\pdf\1.pdf'
    with open('mypdf.pdf', 'wb') as output:
        pdf = pisa.CreatePDF(html.encode("UTF-8"), output, encoding='UTF-8')
        # pdf = pisa.pisaDocument(BytesIO(
        #     html.encode("UTF-8")), output)
    # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    # if not pdf.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
