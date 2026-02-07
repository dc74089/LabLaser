from django.urls import path

from app.views import *

urlpatterns = [
    path('', choose_file, name='index'),
    path('customize/<uuid:template_id>/', customize_file, name='customize'),
    path('customize/<uuid:template_id>/render/', render_template, name='render'),

    path('admin/', admin, name='admin'),
    path('admin/pat/', admin_save_pat, name='admin_save_pat'),
    path('admin/ip/', admin_save_ip, name='admin_save_ip'),
]