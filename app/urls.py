from django.urls import path

from app.views import *

urlpatterns = [
    path('', choose_file, name='index'),
    path('customize/<uuid:template_id>/', customize_file, name='customize'),
    path('customize/<uuid:template_id>/render/', render_template, name='render'),
    path('customize/<uuid:template_id>/save/', save_customized_file, name='save_customized_file'),

    path('customized/', list_customized_files, name='list_customized_files'),
    path('customized/<int:customized_file_id>/preview/', preview_customized_file, name='preview_customized_file'),
    path('customized/<int:customized_file_id>/send/', send_to_laser, name='send_to_laser'),

    path('admin/', admin, name='admin'),
    path('admin/pat/', admin_save_pat, name='admin_save_pat'),
    path('admin/ip/', admin_save_ip, name='admin_save_ip'),
]