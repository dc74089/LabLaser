import json
import requests
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from app.models import TemplateFile, CustomizedFile


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
    # Fetch available import profiles if credentials are configured
    import_profiles = []
    error_message = None

    api_key = request.session.get('pat')
    ip_address = request.session.get('ip')

    if api_key and ip_address:
        try:
            base_url = f"http://{ip_address}:5001/api/OpenApi"
            headers = {
                'Authorization': f'PersonalAccessToken {api_key}',
                'Accept': 'application/json',
                'x-api-version': '1.0-OpenApi'
            }

            response = requests.get(
                f"{base_url}/GetImportProfiles",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            import_profiles = response.json()
        except requests.RequestException as e:
            error_message = f"Could not fetch import profiles: {str(e)}"

    return render(request, "app/admin.html", {
        'import_profiles': import_profiles,
        'error_message': error_message,
        'selected_profile_id': request.session.get('import_profile_id')
    })


def admin_save_pat(request):
    if request.method == "POST" and 'pat' in request.POST:
        pat = request.POST['pat']

        request.session['pat'] = pat

        return redirect('admin')

    return HttpResponseBadRequest()


def admin_save_ip(request):
    if request.method == "POST" and 'ip' in request.POST:
        ip = request.POST['ip']

        request.session['ip'] = ip

        return redirect('admin')

    return HttpResponseBadRequest()


def admin_save_import_profile(request):
    if request.method == "POST" and 'import_profile_id' in request.POST:
        profile_id = request.POST['import_profile_id']

        request.session['import_profile_id'] = profile_id

        messages.success(request, 'Default import profile saved successfully.')
        return redirect('admin')

    return HttpResponseBadRequest()


@require_POST
def save_customized_file(request, template_id):
    """Save a customized file when user clicks 'Finished Customizing'"""
    template = get_object_or_404(TemplateFile, id=template_id)

    # Get the customization data from POST
    guest_name = request.POST.get('guest_name', 'Guest')
    slot_data_list = request.POST.getlist('data[]')

    # Create the CustomizedFile
    customized_file = CustomizedFile.objects.create(
        guest_name=guest_name,
        template=template,
        slot_data=json.dumps(slot_data_list)
    )

    return JsonResponse({
        'success': True,
        'id': str(customized_file.id),
        'message': 'File saved successfully'
    })


def send_to_laser(request, customized_file_id):
    """Send a customized file to the Trotec Ruby laser via API"""
    customized_file = get_object_or_404(CustomizedFile, id=customized_file_id)

    # Get API credentials from session
    api_key = request.session.get('pat')
    ip_address = request.session.get('ip')
    import_profile_id = request.session.get('import_profile_id')

    if not api_key or not ip_address:
        messages.error(request, 'API credentials not configured. Please configure in admin.')
        return redirect('list_customized_files')

    base_url = f"http://{ip_address}:5001/api/OpenApi"

    try:
        # Render the SVG
        svg_content = customized_file.render()

        # Upload the file using the documented /Upload endpoint
        # According to swagger spec, the field name should be 'uploadedFile'
        files = {
            'uploadedFile': ('web_export.svg', svg_content.encode('utf-8'), 'image/svg+xml')
        }
        headers = {
            'Authorization': f'PersonalAccessToken {api_key}',
            'Accept': 'application/json',
            'x-api-version': '1.0-OpenApi'
        }

        # Build URL with optional import profile
        url = f"{base_url}/Upload"
        params = {}
        if import_profile_id:
            params['importProfileId'] = import_profile_id

        # Use guest name as tracking number for easier identification
        params['trackingNumber'] = customized_file.guest_name

        upload_response = requests.post(
            url,
            headers=headers,
            files=files,
            params=params,
            timeout=30
        )
        upload_response.raise_for_status()

        messages.success(request, f'Successfully uploaded "{customized_file.guest_name}" to laser! The file should now be in the queue. Press START on the machine.')

    except requests.RequestException as e:
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_json = e.response.json()
                if 'code' in error_json:
                    error_detail = f"{error_json['code']}: {error_json.get('additionalInfo', '')}"
            except:
                error_detail = e.response.text if e.response.text else str(e)

        messages.error(request, f'Failed to send to laser: {error_detail}')

    return redirect('list_customized_files')


def list_customized_files(request):
    """Display the last 50 customized files, newest first"""
    customized_files = CustomizedFile.objects.select_related('template').order_by('-created')[:50]

    return render(request, 'app/list_customized_files.html', {
        'customized_files': customized_files
    })


def preview_customized_file(request, customized_file_id):
    """Return the rendered SVG for preview"""
    customized_file = get_object_or_404(CustomizedFile, id=customized_file_id)
    svg_content = customized_file.render()
    return HttpResponse(svg_content)