from django.http import HttpResponse
from django.shortcuts import render

from app.models import TemplateFile


# Create your views here.
def choose_file(request):
    return render(request, "app/choose_file.html", {
        "templates": TemplateFile.objects.all()
    })


def customize_file(request, template_id):
    template = TemplateFile.objects.get(id=template_id)

    return render(request, "app/customize_file.html", {
        "template": template,
    })


def render_template(request, template_id):
    template = TemplateFile.objects.get(id=template_id)
    data = request.GET.getlist('data[]')
    out = template.render(data)

    print(dict(request.GET))

    return HttpResponse(out)