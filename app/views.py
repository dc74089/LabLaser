from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from app.models import TemplateFile


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


def admin(request):
    return render(request, "app/admin.html")


def admin_save_pat(request):
    if request.method == "POST" and 'pat' in request.POST:
        pat = request.POST['pat']

        request.session['pat'] = pat

        return redirect('admin')

    return HttpResponseBadRequest()