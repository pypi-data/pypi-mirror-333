from django.urls import path

from . import views

app_name = 'wagtail_block_exchange'

urlpatterns = [
    path('copy/', views.copy_block_to_clipboard, name='copy_block'),
    path('paste/', views.paste_block_to_page, name='paste_block'),
    path('clipboard/', views.clipboard_view, name='clipboard'),
    path('clipboard/list/', views.get_clipboard, name='get_clipboard'),
    path('clipboard/clear/<int:clipboard_id>/', views.clear_clipboard_item, name='clear_clipboard_item'),
    path('compatibility-check/', views.block_compatibility_check, name='compatibility_check'),
] 