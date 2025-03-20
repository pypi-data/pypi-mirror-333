import json
import logging
import traceback
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import PermissionDenied

from wagtail.models import Page

from .models import BlockClipboard
from .services import BlockExtractor, BlockApplicator, BlockClipboardService

logger = logging.getLogger(__name__)

@login_required
@require_POST
def copy_block_to_clipboard(request):
    """
    Copy a block to the user's clipboard.
    
    POST parameters:
    - page_id: ID of the page containing the block
    - block_id: ID of the block to copy
    - label: Optional label for the clipboard item
    """
    page_id = request.POST.get('page_id')
    block_id = request.POST.get('block_id')
    label = request.POST.get('label', '')
    
    logger.info(f"Copying block to clipboard - page_id: {page_id}, block_id: {block_id}, label: {label}")
    
    if not page_id or not block_id:
        logger.warning("Missing required parameters for copy_block_to_clipboard")
        return JsonResponse({
            'success': False,
            'error': 'Missing required parameters'
        }, status=400)
    
    try:
        # Check permissions
        page = get_object_or_404(Page, id=page_id)
        if not page.permissions_for_user(request.user).can_edit():
            logger.warning(f"User {request.user.id} does not have permission to edit page {page_id}")
            raise PermissionDenied
        
        # Log the page type and content
        logger.info(f"Page type: {page.specific_class.__name__}")
        
        # Print the block_id for debugging
        logger.info(f"Attempting to extract block with ID: {block_id}")
        
        # Copy the block
        clipboard_id = BlockClipboardService.copy_to_clipboard(
            request.user, int(page_id), block_id, label
        )
        
        if clipboard_id:
            logger.info(f"Successfully copied block {block_id} to clipboard, clipboard_id: {clipboard_id}")
            return JsonResponse({
                'success': True,
                'clipboard_id': clipboard_id
            })
        else:
            logger.error(f"BlockClipboardService.copy_to_clipboard returned None for block {block_id}")
            return JsonResponse({
                'success': False,
                'error': 'Failed to copy block - service returned None'
            }, status=500)
    except Page.DoesNotExist:
        logger.exception(f"Page with id {page_id} does not exist")
        return JsonResponse({
            'success': False,
            'error': f'Page with id {page_id} does not exist'
        }, status=404)
    except PermissionDenied:
        logger.exception("Permission denied")
        return JsonResponse({
            'success': False,
            'error': 'Permission denied'
        }, status=403)
    except Exception as e:
        # Log the detailed error with traceback
        logger.exception(f"Error copying block to clipboard: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'error': f'Failed to copy block: {str(e)}'
        }, status=500)


@login_required
@require_POST
def paste_block_to_page(request):
    """
    Paste a block from the clipboard to a page.
    
    POST parameters:
    - clipboard_id: ID of the clipboard item
    - page_id: ID of the page to paste to
    - field_name: (Optional) Name of the field to paste to
    - position: (Optional) Position to insert at
    """
    clipboard_id = request.POST.get('clipboard_id')
    page_id = request.POST.get('page_id')
    field_name = request.POST.get('field_name', None)
    position = request.POST.get('position', -1)
    
    if not clipboard_id or not page_id:
        logger.warning("Missing required parameters in paste request")
        return JsonResponse({
            'success': False,
            'error': 'Missing required parameters'
        }, status=400)
    
    try:
        clipboard_id = int(clipboard_id)
        page_id = int(page_id)
        position = int(position) if position else -1
    except ValueError:
        logger.error(f"Invalid parameter values: clipboard_id={clipboard_id}, page_id={page_id}, position={position}")
        return JsonResponse({
            'success': False,
            'error': 'Invalid parameter values'
        }, status=400)
    
    try:
        # Check if this page has a draft revision that is more recent than published
        base_page = Page.objects.get(id=page_id)
        latest_revision = base_page.get_latest_revision()
        
        if latest_revision and latest_revision.created_at > base_page.last_published_at:
            # Compare timestamps of the latest revision with the database page state
            if latest_revision.created_at.timestamp() != base_page.latest_revision_created_at.timestamp():
                # This indicates there are unsaved changes since the last revision
                logger.warning(f"Rejected paste operation: Page {page_id} has unsaved changes since last revision")
                return JsonResponse({
                    'success': False,
                    'error': 'Cannot paste when page has unsaved changes. Please save your changes first.'
                }, status=400)
        
        # Check permissions
        if not base_page.permissions_for_user(request.user).can_edit():
            logger.warning(f"Permission denied for user {request.user} on page {page_id}")
            return JsonResponse({
                'success': False,
                'error': 'You do not have permission to edit this page'
            }, status=403)
            
        # Call the service to handle the paste
        result = BlockClipboardService.paste_from_clipboard(
            clipboard_id,
            page_id,
            field_name,
            position
        )
        
        if result:
            logger.info(f"Paste operation successful for clipboard_id={clipboard_id} to page={page_id}")
            return JsonResponse({
                'success': True
            })
        else:
            logger.error(f"Paste operation failed for clipboard_id={clipboard_id} to page={page_id}")
            return JsonResponse({
                'success': False,
                'error': 'Failed to paste block'
            }, status=500)
    except BlockClipboard.DoesNotExist:
        logger.error(f"Clipboard item {clipboard_id} not found")
        return JsonResponse({
            'success': False,
            'error': 'Clipboard item not found'
        }, status=404)
    except Page.DoesNotExist:
        logger.error(f"Page {page_id} not found")
        return JsonResponse({
            'success': False,
            'error': 'Page not found'
        }, status=404)
    except Exception as e:
        logger.exception(f"Error pasting block: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_GET
def get_clipboard(request):
    """
    Get the user's block clipboard contents as JSON.
    """
    clipboard_items = BlockClipboardService.get_clipboard_for_user(request.user)
    
    return JsonResponse({
        'success': True,
        'items': clipboard_items
    })


@login_required
@require_POST
def clear_clipboard_item(request, clipboard_id):
    """
    Delete a clipboard item.
    """
    try:
        clipboard_item = BlockClipboard.objects.get(id=clipboard_id, user=request.user)
        clipboard_item.delete()
        return JsonResponse({'success': True})
    except BlockClipboard.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Clipboard item not found'
        }, status=404)


@login_required
def clipboard_view(request):
    """
    Render the clipboard view in the Wagtail admin.
    """
    clipboard_items = BlockClipboardService.get_clipboard_for_user(request.user)
    
    return render(request, 'wagtail_block_exchange/clipboard.html', {
        'clipboard_items': clipboard_items
    })


@login_required
@require_GET
def block_compatibility_check(request):
    """
    Check if a block is compatible with a page.
    
    GET parameters:
    - clipboard_id: ID of the clipboard item
    - page_id: ID of the page to check
    """
    clipboard_id = request.GET.get('clipboard_id')
    page_id = request.GET.get('page_id')
    
    if not clipboard_id or not page_id:
        return JsonResponse({
            'success': False,
            'error': 'Missing required parameters'
        }, status=400)
    
    try:
        clipboard_item = BlockClipboard.objects.get(id=clipboard_id, user=request.user)
        page = Page.objects.specific().get(id=page_id)
        
        # In a real implementation, this would do a more thorough check
        compatible_field = BlockApplicator._detect_compatible_field(
            page, clipboard_item.block_data
        )
        
        return JsonResponse({
            'success': True,
            'compatible': compatible_field is not None,
            'compatible_field': compatible_field
        })
        
    except (BlockClipboard.DoesNotExist, Page.DoesNotExist):
        return JsonResponse({
            'success': False,
            'error': 'Clipboard item or page not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500) 