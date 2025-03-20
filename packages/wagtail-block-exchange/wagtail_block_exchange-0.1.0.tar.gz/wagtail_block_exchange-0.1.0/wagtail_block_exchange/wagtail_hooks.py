from django.urls import path, include
from django.utils.html import format_html
from django.templatetags.static import static
from django.urls import reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem


@hooks.register('register_admin_urls')
def register_admin_urls():
    """Register the block exchange URLs with the Wagtail admin."""
    return [
        path('block-exchange/', include('wagtail_block_exchange.urls', namespace='wagtail_block_exchange')),
    ]


@hooks.register('register_admin_menu_item')
def register_clipboard_menu_item():
    """Add a menu item for the block clipboard to the Wagtail admin menu."""
    return MenuItem(
        'Block Clipboard',
        reverse('wagtail_block_exchange:clipboard'),
        icon_name='copy',
        order=800
    )


@hooks.register('insert_editor_css')
def block_exchange_css():
    """Add custom CSS for the block exchange functionality."""
    # Use a unique tag to ensure our CSS is loaded properly
    return format_html(
        '<link rel="stylesheet" href="{}" id="block-exchange-css">',
        static('wagtail_block_exchange/css/block-exchange.css')
    )


@hooks.register('insert_editor_js')
def block_exchange_js():
    """Add JavaScript for the block exchange functionality.
    
    This loads the bundled JavaScript file that contains all the Block Exchange
    functionality, including clipboard integration and UI enhancements.
    """
    return format_html(
        '<script src="{}" defer id="block-exchange-js"></script>',
        static('wagtail_block_exchange/js/dist/wagtail_block_exchange.js')
    )


@hooks.register('register_streamfield_block_menu_item')
def register_block_copy_menu_item():
    """
    Add a Copy to Clipboard option to the block menu.
    """
    return {
        'name': 'copy_to_clipboard',
        'label': 'Copy to Clipboard',
        'icon_name': 'copy',
        'order': 100,
    }

# The previous insert_chooser_hook_js function has been removed.
# Its functionality is now included in the bundled JavaScript file. 