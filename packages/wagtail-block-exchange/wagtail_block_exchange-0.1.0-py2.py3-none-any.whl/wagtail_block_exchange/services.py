import json
import importlib
import logging
import inspect
import traceback
import re
import datetime
from typing import Dict, Any, List, Optional, Tuple

from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.models import Page
from wagtail.images.models import Image
from wagtail.documents.models import Document
from wagtail.blocks import StreamBlock, StreamValue, BlockField, StructValue
from wagtail.fields import StreamField, RichTextField
from wagtail.rich_text import RichText
from wagtail.snippets.models import get_snippet_models
from django.core.serializers.json import DjangoJSONEncoder
from django.apps import apps
from django.db.models import Model
from django.contrib.auth import get_user_model

from .models import BlockClipboard

logger = logging.getLogger(__name__)

User = get_user_model()


class WagtailJSONEncoder(DjangoJSONEncoder):
    """
    Custom JSON encoder that can handle Wagtail-specific types
    like RichText, StructValue, Images, Documents, Pages, Snippets, and DateTimes.
    """
    def default(self, obj):
        # Handle RichText by converting to a string
        if isinstance(obj, RichText):
            return str(obj)
        # Handle list blocks (previously handled as ListValue)
        elif hasattr(obj, '__iter__') and not isinstance(obj, (dict, str)):
            logger.debug(f"WagtailJSONEncoder: Converting list-like object to list")
            return [self._process_item(item) for item in obj]
        # Handle StructValue by converting to dict
        elif isinstance(obj, StructValue):
            logger.debug(f"WagtailJSONEncoder: Converting StructValue to dict")
            return {key: self._process_item(value) for key, value in obj.items()}
        # Handle Image objects
        elif isinstance(obj, Image):
            logger.debug(f"WagtailJSONEncoder: Converting Image to reference id={obj.id}")
            return f"__image__{obj.id}"
        # Handle Document objects
        elif isinstance(obj, Document):
            logger.debug(f"WagtailJSONEncoder: Converting Document to reference id={obj.id}")
            return f"__document__{obj.id}"
        # Handle Page objects
        elif isinstance(obj, Page):
            logger.debug(f"WagtailJSONEncoder: Converting Page to reference id={obj.id}")
            return f"__page__{obj.id}"
        # Handle datetime objects
        elif isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            logger.debug(f"WagtailJSONEncoder: Converting datetime to ISO format")
            if hasattr(obj, 'isoformat'):
                return f"__datetime__{obj.isoformat()}"
            return str(obj)
        # Handle Snippet models
        elif self._is_snippet_model(obj):
            model_name = type(obj).__module__ + '.' + type(obj).__name__
            logger.debug(f"WagtailJSONEncoder: Converting Snippet {model_name} to reference id={obj.id}")
            return f"__snippet__{model_name}__{obj.id}"
        # Try the parent class's default method
        return super().default(obj)
    
    def _process_item(self, item):
        """Process an item from a list or dict to handle any complex types"""
        if isinstance(item, RichText) or isinstance(item, StructValue) or isinstance(item, Image) or \
           isinstance(item, Document) or isinstance(item, Page) or \
           isinstance(item, (datetime.datetime, datetime.date, datetime.time)) or \
           self._is_snippet_model(item):
            return self.default(item)
        # For list-like objects
        elif hasattr(item, '__iter__') and not isinstance(item, (dict, str)):
            return [self._process_item(i) for i in item]
        return item
    
    def _is_snippet_model(self, obj):
        """Check if an object is a Wagtail snippet model instance"""
        try:
            if not hasattr(obj, 'id'):
                return False
                
            # Get all registered snippet models
            snippet_models = get_snippet_models()
            
            # Check if object is an instance of any snippet model
            for model in snippet_models:
                if isinstance(obj, model):
                    return True
            
            return False
        except Exception as e:
            logger.warning(f"Error checking snippet model: {e}")
            return False


class BlockExtractor:
    """
    Extracts block data from any Wagtail page with StreamFields.
    """
    
    @classmethod
    def extract_block(cls, page_id: int, block_id: str) -> Optional[Dict[str, Any]]:
        """
        Extract a block from a page by its ID.
        
        Args:
            page_id: The ID of the page containing the block
            block_id: The ID of the block to extract
            
        Returns:
            Dict with block data or None if not found
        """
        try:
            logger.info(f"BlockExtractor: Attempting to extract block {block_id} from page {page_id}")
            page = Page.objects.specific().get(id=page_id)
            logger.info(f"BlockExtractor: Page found, type: {type(page).__name__}")
            return cls._find_block_in_page(page, block_id)
        except Page.DoesNotExist:
            logger.error(f"Page with ID {page_id} does not exist")
            return None
        except Exception as e:
            logger.exception(f"Error extracting block {block_id} from page {page_id}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    @classmethod
    def _find_block_in_page(cls, page: Model, block_id: str) -> Optional[Dict[str, Any]]:
        """
        Search through all StreamFields in a page to find a specific block.
        
        Args:
            page: The page object to search
            block_id: The ID of the block to extract
            
        Returns:
            Dict with block data or None if not found
        """
        try:
            logger.info(f"BlockExtractor: Finding block {block_id} in page {page.id}")
            
            # Find all StreamFields in the page
            streamfields = cls._get_streamfields(page)
            logger.info(f"BlockExtractor: Found {len(streamfields)} StreamFields in page: {list(streamfields.keys())}")
            
            for field_name, field in streamfields.items():
                logger.info(f"BlockExtractor: Checking field '{field_name}'")
                field_value = getattr(page, field_name)
                
                if not field_value:
                    logger.info(f"BlockExtractor: Field '{field_name}' is empty, skipping")
                    continue
                    
                # Search for the block in this field
                result = cls._find_block_in_streamfield(field_value, block_id, field_name)
                if result:
                    logger.info(f"BlockExtractor: Found block {block_id} in field '{field_name}'")
                    return result
            
            logger.warning(f"BlockExtractor: Block {block_id} not found in any StreamField")
            return None
        except Exception as e:
            logger.exception(f"Error finding block {block_id} in page: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    @classmethod
    def _get_streamfields(cls, page: Model) -> Dict[str, StreamField]:
        """
        Get all StreamFields from a page.
        
        Args:
            page: The page model
            
        Returns:
            Dict of {field_name: field} for all StreamFields
        """
        try:
            streamfields = {}
            for field in page._meta.get_fields():
                if isinstance(field, StreamField):
                    streamfields[field.name] = field
                    logger.info(f"BlockExtractor: Found StreamField '{field.name}'")
            
            return streamfields
        except Exception as e:
            logger.exception(f"Error getting StreamFields: {e}")
            return {}
    
    @classmethod
    def _find_block_in_streamfield(
        cls, field_value: StreamValue, block_id: str, field_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Find a block by ID within a StreamField value.
        
        Args:
            field_value: The StreamField value to search
            block_id: The ID of the block to find
            field_name: The name of the field for context
            
        Returns:
            Dict with block data or None if not found
        """
        try:
            logger.info(f"BlockExtractor: Searching for block {block_id} in field '{field_name}'")
            
            # Log the block structure for debugging
            try:
                block_count = len(field_value)
                logger.info(f"BlockExtractor: Field contains {block_count} blocks")
                
                # Log the first few blocks for debugging
                for i, block in enumerate(field_value):
                    if i < 5:  # Limit to first 5 blocks to prevent huge logs
                        logger.info(f"BlockExtractor: Block {i} - ID: {block.id}, Type: {block.block_type}")
                        # Log more detailed structure
                        try:
                            value_repr = str(block.value)[:100]  # First 100 chars
                            logger.debug(f"BlockExtractor: Block {i} value preview: {value_repr}...")
                        except Exception:
                            pass
            except Exception as log_err:
                logger.warning(f"Error logging block structure: {log_err}")
            
            for block in field_value:
                logger.debug(f"BlockExtractor: Checking block with ID {block.id}")
                
                if str(block.id) == block_id:
                    logger.info(f"BlockExtractor: Found exact match for block ID {block_id}")
                    return cls.serialize_block(block, field_name)
                
                # If block_id is a section identifier (like "block-XXX-section")
                if block_id.endswith("-section") and str(block.id) in block_id:
                    logger.info(f"BlockExtractor: Found section match for block ID {block_id} (contains {block.id})")
                    return cls.serialize_block(block, field_name)
                    
                # Check for nested blocks in StructBlocks
                nested_block = cls._find_in_nested_blocks(block, block_id, field_name)
                if nested_block:
                    return nested_block
                    
            logger.info(f"BlockExtractor: Block {block_id} not found in field '{field_name}'")
            return None
        except Exception as e:
            logger.exception(f"Error finding block {block_id} in StreamField: {e}")
            return None
    
    @classmethod
    def _find_in_nested_blocks(
        cls, block: Any, block_id: str, field_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Recursively search for a block ID in nested blocks.
        
        Args:
            block: The block that might contain nested blocks
            block_id: The ID to search for
            field_name: The name of the parent field
            
        Returns:
            Dict with block data or None if not found
        """
        # This is a simplified version - would need more robust handling for 
        # different block types in a production implementation
        return None  # For now, we just handle top-level blocks
    
    @classmethod
    def serialize_block(cls, block: Any, field_name: str) -> Dict[str, Any]:
        """
        Create a portable representation of a block.
        
        Args:
            block: The block to serialize
            field_name: Name of the parent field
            
        Returns:
            Dict with serialized block data
        """
        try:
            # Get the block data based on its type
            if hasattr(block.value, 'get_prep_value'):
                # StreamValue or similar with get_prep_value method
                logger.debug("BlockExtractor: Using get_prep_value() for serialization")
                block_data = block.value.get_prep_value()
            elif isinstance(block.value, StructValue):
                # For StructValue objects, we need to convert to a dict
                logger.debug("BlockExtractor: Handling StructValue object")
                
                # Convert StructValue to a dict and process any RichText fields
                block_data = {}
                rich_text_fields = []  # Track rich text fields for restoration
                
                for key, value in block.value.items():
                    # Handle RichText fields
                    if isinstance(value, RichText):
                        logger.debug(f"BlockExtractor: Converting RichText field '{key}' to string")
                        block_data[key] = str(value)
                        rich_text_fields.append(key)  # Mark this field as containing rich text
                    else:
                        block_data[key] = value
                
                # Store the RichText field names for later use during pasting
                if rich_text_fields:
                    block_data['_rich_text_fields'] = rich_text_fields
                
                # Log the processed data for debugging
                logger.debug(f"BlockExtractor: Processed StructValue data: {block_data}")
            else:
                # For any other type, try to get a reasonable representation
                logger.debug(f"BlockExtractor: Using fallback serialization for {type(block.value).__name__}")
                if hasattr(block.block, 'get_prep_value'):
                    block_data = block.block.get_prep_value(block.value)
                else:
                    # Last resort - try direct conversion
                    try:
                        block_data = dict(block.value) if hasattr(block.value, '__iter__') else block.value
                    except (TypeError, ValueError):
                        logger.warning(f"BlockExtractor: Cannot convert {type(block.value).__name__} to dict, using str representation")
                        block_data = str(block.value)
            
            # Add metadata for later use
            metadata = {
                'block_id': str(block.id),
                'block_type': block.block_type,
                'field_name': field_name,
                'wagtail_version': '.'.join(str(v) for v in WAGTAIL_VERSION),
                'block_class': block.block.__class__.__name__,
            }
            
            logger.info(f"BlockExtractor: Serialized block {block.id} of type {block.block_type}")
            
            # Log detailed structure of the data
            try:
                # Use our custom encoder to ensure RichText objects are handled
                json_data = json.dumps(block_data, cls=WagtailJSONEncoder, indent=2)
                logger.debug(f"BlockExtractor: Block data structure: {json_data[:500]}...")
            except Exception as json_err:
                logger.warning(f"Could not log block data as JSON: {json_err}")
                logger.debug(f"BlockExtractor: Block data preview: {str(block_data)[:500]}...")
            
            return {
                'block_type': block.block_type,
                'value': block_data,
                'metadata': metadata
            }
        except Exception as e:
            logger.exception(f"Error serializing block: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                'block_type': getattr(block, 'block_type', 'unknown'),
                'value': {},
                'metadata': {'error': str(e)}
            }


class BlockApplicator:
    """
    Applies blocks to pages, handling validation and transformation.
    """
    
    @classmethod
    def apply_block_to_page(
        cls, 
        page_id: int, 
        block_data: Dict[str, Any],
        field_name: Optional[str] = None,
        position: int = -1
    ) -> bool:
        """
        Apply a block to a page.
        
        Args:
            page_id: ID of the destination page
            block_data: Serialized block data
            field_name: Name of the field to apply to (auto-detect if None)
            position: Position to insert (-1 = append at end)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"BlockApplicator: Applying block to page {page_id}")
            # Use custom encoder to ensure RichText objects are handled
            json_data = json.dumps(block_data, cls=WagtailJSONEncoder, indent=2)
            logger.debug(f"BlockApplicator: Block data: {json_data[:500]}...")
            
            # First get the basic page to check for revisions
            base_page = Page.objects.get(id=page_id)
            
            # Check if there's a draft revision (unpublished changes)
            latest_revision = base_page.get_latest_revision()
            
            if latest_revision and not latest_revision.approved_go_live_at:
                # Use the draft version of the page
                logger.info(f"BlockApplicator: Using latest draft revision (id: {latest_revision.id}) for page {page_id}")
                page = latest_revision.as_object()
            else:
                # No draft exists, use the published version
                logger.info(f"BlockApplicator: Using published version for page {page_id}")
                page = Page.objects.specific().get(id=page_id)
            
            # Determine the appropriate field
            target_field_name = field_name or cls._detect_compatible_field(page, block_data)
            if not target_field_name:
                logger.error(f"No compatible field found for block type {block_data.get('block_type')}")
                return False
            
            logger.info(f"BlockApplicator: Selected field '{target_field_name}' for block application")
                
            # Get the field
            field_value = getattr(page, target_field_name)
            
            # Validate block compatibility
            if not cls._validate_block_compatibility(field_value, block_data):
                logger.error(f"Block is not compatible with field {target_field_name}")
                return False
                
            # Apply the block
            return cls._apply_block_to_field(page, target_field_name, field_value, block_data, position)
            
        except Page.DoesNotExist:
            logger.error(f"Page with ID {page_id} does not exist")
            return False
        except Exception as e:
            logger.exception(f"Error applying block to page {page_id}: {e}")
            return False
    
    @classmethod
    def _detect_compatible_field(cls, page: Model, block_data: Dict[str, Any]) -> Optional[str]:
        """
        Auto-detect a compatible StreamField for the block.
        
        Args:
            page: The page model
            block_data: The block data
            
        Returns:
            Name of a compatible field or None
        """
        block_type = block_data.get('block_type')
        if not block_type:
            logger.error("No block_type in block data")
            return None
        
        logger.info(f"BlockApplicator: Looking for fields compatible with {block_type}")
            
        # First, try to use the original field name if provided in metadata
        if 'metadata' in block_data and 'field_name' in block_data['metadata']:
            original_field_name = block_data['metadata']['field_name']
            logger.info(f"BlockApplicator: Original field was '{original_field_name}'")
            
            # Check if this field exists and is compatible
            if hasattr(page, original_field_name):
                field = getattr(page.__class__, original_field_name)
                if isinstance(field, StreamField) and cls._field_accepts_block_type(field, block_type):
                    logger.info(f"BlockApplicator: Original field '{original_field_name}' is compatible")
                    return original_field_name
        
        # Find StreamFields that accept this block type
        for field_name, field in BlockExtractor._get_streamfields(page).items():
            if cls._field_accepts_block_type(field, block_type):
                logger.info(f"BlockApplicator: Field '{field_name}' accepts block type '{block_type}'")
                return field_name
                
        # If we couldn't find an exact match, return the first StreamField
        # that we can potentially transform the block for
        for field_name, field in BlockExtractor._get_streamfields(page).items():
            if field.stream_block.child_blocks:  # Any StreamField with child blocks
                logger.info(f"BlockApplicator: Using field '{field_name}' as fallback")
                return field_name
                
        logger.warning("BlockApplicator: No compatible fields found")
        return None
    
    @classmethod
    def _field_accepts_block_type(cls, field: StreamField, block_type: str) -> bool:
        """
        Check if a field accepts a specific block type.
        
        Args:
            field: The StreamField
            block_type: The block type to check
            
        Returns:
            True if the field accepts this block type
        """
        try:
            if not hasattr(field, 'stream_block') or not hasattr(field.stream_block, 'child_blocks'):
                logger.warning(f"Field does not have expected StreamField attributes")
                return False
                
            result = block_type in field.stream_block.child_blocks
            logger.debug(f"Field {'accepts' if result else 'does not accept'} block type '{block_type}'")
            if not result:
                logger.debug(f"Available block types: {list(field.stream_block.child_blocks.keys())}")
            return result
        except Exception as e:
            logger.exception(f"Error checking if field accepts block type: {e}")
            return False
    
    @classmethod
    def _validate_block_compatibility(cls, field_value: StreamValue, block_data: Dict[str, Any]) -> bool:
        """
        Validate that a block is compatible with a field.
        
        Args:
            field_value: The StreamField value
            block_data: The block data
            
        Returns:
            True if compatible
        """
        # In a real implementation, this would do more thorough validation
        # including schema checks, required fields, etc.
        logger.info("BlockApplicator: Validating block compatibility")
        
        try:
            block_type = block_data.get('block_type')
            if not block_type:
                logger.error("No block_type in block data")
                return False
                
            # Check if the block type is allowed in this field
            stream_block = field_value.stream_block
            if block_type not in stream_block.child_blocks:
                logger.error(f"Block type '{block_type}' not allowed in this field")
                logger.debug(f"Allowed block types: {list(stream_block.child_blocks.keys())}")
                return False
                
            # Check if the value structure matches what's expected
            value = block_data.get('value')
            if not isinstance(value, (dict, list)):
                logger.error(f"Block value is not a dict or list: {type(value)}")
                return False
                
            return True
            
        except Exception as e:
            logger.exception(f"Error validating block compatibility: {e}")
            return False
    
    @classmethod
    def _apply_block_to_field(
        cls,
        page: Model,
        field_name: str,
        field_value: StreamValue,
        block_data: Dict[str, Any],
        position: int = -1
    ) -> bool:
        """
        Apply a block to a specific field.
        
        Args:
            page: The page model
            field_name: Name of the field
            field_value: The field value
            block_data: Block data to apply
            position: Position to insert at
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"POSITION DEBUG: BlockApplicator - Applying block to field '{field_name}' at position {position}")
            
            # Convert field_value to list if it isn't already
            blocks_list = list(field_value)
            logger.info(f"POSITION DEBUG: Current field has {len(blocks_list)} blocks")
            
            # Prepare the block for insertion
            block_type = block_data.get('block_type')
            if not block_type:
                logger.error("No block_type in block data")
                return False
                
            block_value = block_data.get('value')
            if block_value is None:
                logger.error("No value in block data")
                return False
            
            # Process the block_value to restore RichText objects
            processed_block_value = cls._process_block_value(block_value)
            
            # Use custom encoder to ensure RichText objects are handled in logs
            try:
                json_data = json.dumps(processed_block_value, cls=WagtailJSONEncoder, indent=2)
                logger.debug(f"BlockApplicator: Inserting block of type '{block_type}'")
                logger.debug(f"BlockApplicator: Block value (processed): {json_data[:500]}...")
            except Exception as json_err:
                logger.warning(f"Could not log processed block value as JSON: {json_err}")
            
            # Insert at the specified position, or append at the end
            if position < 0 or position >= len(blocks_list):
                logger.info(f"POSITION DEBUG: Position {position} is out of range (0-{len(blocks_list)-1 if blocks_list else 0}), appending block at the end")
                blocks_list.append((block_type, processed_block_value))
            else:
                logger.info(f"POSITION DEBUG: Inserting block at position {position} out of {len(blocks_list)} blocks")
                blocks_list.insert(position, (block_type, processed_block_value))
            
            # Update the field
            stream_block = field_value.stream_block
            
            # Create a new StreamValue (simple constructor method)
            new_stream_value = StreamValue(stream_block, blocks_list)
            logger.info(f"POSITION DEBUG: Created new StreamValue with {len(new_stream_value)} blocks after inserting at position {position}")
            
            # Set the new value on the page
            setattr(page, field_name, new_stream_value)
            
            # Save the page
            logger.info("POSITION DEBUG: Saving page with updated StreamField")
            page.save()
            revision = page.save_revision()
            logger.info(f"POSITION DEBUG: Created revision {revision.id} after inserting at position {position}")
            
            return True
            
        except Exception as e:
            logger.exception(f"Error applying block to field {field_name}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    @classmethod
    def _process_block_value(cls, block_value: Any) -> Any:
        """
        Process block values to restore RichText objects and other special types.
        
        Args:
            block_value: The serialized block value
            
        Returns:
            The processed block value with objects restored
        """
        try:
            # If this is a dict, process it
            if isinstance(block_value, dict):
                result = {}
                
                # Check if this dict has marked rich text fields
                rich_text_fields = block_value.pop('_rich_text_fields', [])
                
                # Process each key-value pair
                for key, value in block_value.items():
                    if key in rich_text_fields or cls._looks_like_rich_text(value):
                        # Convert string back to RichText
                        logger.debug(f"BlockApplicator: Converting field '{key}' back to RichText")
                        result[key] = RichText(value)
                    elif isinstance(value, str) and value.startswith('__image__'):
                        # Handle image references
                        try:
                            # Extract the image ID from the reference
                            image_id = int(value.replace('__image__', ''))
                            logger.debug(f"BlockApplicator: Converting reference to Image with ID {image_id}")
                            # Fetch the image by ID
                            image = Image.objects.get(id=image_id)
                            result[key] = image
                        except (ValueError, Image.DoesNotExist) as e:
                            logger.error(f"Error restoring image reference '{value}': {e}")
                            # If we can't restore the image, use None instead of a string to prevent
                            # errors when Wagtail tries to access .pk on a string
                            result[key] = None
                    elif isinstance(value, str) and value.startswith('__document__'):
                        # Handle document references
                        try:
                            # Extract the document ID from the reference
                            document_id = int(value.replace('__document__', ''))
                            logger.debug(f"BlockApplicator: Converting reference to Document with ID {document_id}")
                            # Fetch the document by ID
                            document = Document.objects.get(id=document_id)
                            result[key] = document
                        except (ValueError, Document.DoesNotExist) as e:
                            logger.error(f"Error restoring document reference '{value}': {e}")
                            result[key] = None
                    elif isinstance(value, str) and value.startswith('__page__'):
                        # Handle page references
                        try:
                            # Extract the page ID from the reference
                            page_id = int(value.replace('__page__', ''))
                            logger.debug(f"BlockApplicator: Converting reference to Page with ID {page_id}")
                            # Fetch the page by ID
                            page = Page.objects.get(id=page_id)
                            result[key] = page
                        except (ValueError, Page.DoesNotExist) as e:
                            logger.error(f"Error restoring page reference '{value}': {e}")
                            result[key] = None
                    elif isinstance(value, str) and value.startswith('__datetime__'):
                        # Handle datetime references
                        try:
                            # Extract the datetime string from the reference
                            datetime_str = value.replace('__datetime__', '')
                            logger.debug(f"BlockApplicator: Converting reference to datetime: {datetime_str}")
                            # Parse the ISO format datetime
                            if 'T' in datetime_str:  # Full datetime
                                result[key] = datetime.datetime.fromisoformat(datetime_str)
                            elif ':' in datetime_str:  # Time only
                                result[key] = datetime.time.fromisoformat(datetime_str)
                            else:  # Date only
                                result[key] = datetime.date.fromisoformat(datetime_str)
                        except ValueError as e:
                            logger.error(f"Error restoring datetime reference '{value}': {e}")
                            result[key] = None
                    elif isinstance(value, str) and value.startswith('__snippet__'):
                        # Handle snippet references
                        try:
                            # Extract the snippet model and ID from the reference
                            snippet_str = value.replace('__snippet__', '')
                            model_name, snippet_id = snippet_str.rsplit('__', 1)
                            logger.debug(f"BlockApplicator: Converting reference to Snippet {model_name} with ID {snippet_id}")
                            
                            # Import the model class
                            module_path, class_name = model_name.rsplit('.', 1)
                            module = importlib.import_module(module_path)
                            model_class = getattr(module, class_name)
                            
                            # Fetch the snippet by ID
                            snippet = model_class.objects.get(id=int(snippet_id))
                            result[key] = snippet
                        except (ValueError, AttributeError, ImportError) as e:
                            logger.error(f"Error restoring snippet reference '{value}': {e}")
                            result[key] = None
                    elif isinstance(value, (dict, list)):
                        # Recursively process nested structures
                        result[key] = cls._process_block_value(value)
                    else:
                        # Keep as is
                        result[key] = value
                        
                return result
                
            # If this is a list, process each item
            elif isinstance(block_value, list):
                return [cls._process_block_value(item) for item in block_value]
                
            # Check for special reference strings
            elif isinstance(block_value, str):
                # Image reference
                if block_value.startswith('__image__'):
                    try:
                        image_id = int(block_value.replace('__image__', ''))
                        logger.debug(f"BlockApplicator: Converting reference to Image with ID {image_id}")
                        return Image.objects.get(id=image_id)
                    except (ValueError, Image.DoesNotExist) as e:
                        logger.error(f"Error restoring image reference '{block_value}': {e}")
                        return None
                
                # Document reference
                elif block_value.startswith('__document__'):
                    try:
                        document_id = int(block_value.replace('__document__', ''))
                        logger.debug(f"BlockApplicator: Converting reference to Document with ID {document_id}")
                        return Document.objects.get(id=document_id)
                    except (ValueError, Document.DoesNotExist) as e:
                        logger.error(f"Error restoring document reference '{block_value}': {e}")
                        return None
                
                # Page reference
                elif block_value.startswith('__page__'):
                    try:
                        page_id = int(block_value.replace('__page__', ''))
                        logger.debug(f"BlockApplicator: Converting reference to Page with ID {page_id}")
                        return Page.objects.get(id=page_id)
                    except (ValueError, Page.DoesNotExist) as e:
                        logger.error(f"Error restoring page reference '{block_value}': {e}")
                        return None
                
                # Datetime reference
                elif block_value.startswith('__datetime__'):
                    try:
                        datetime_str = block_value.replace('__datetime__', '')
                        logger.debug(f"BlockApplicator: Converting reference to datetime: {datetime_str}")
                        if 'T' in datetime_str:  # Full datetime
                            return datetime.datetime.fromisoformat(datetime_str)
                        elif ':' in datetime_str:  # Time only
                            return datetime.time.fromisoformat(datetime_str)
                        else:  # Date only
                            return datetime.date.fromisoformat(datetime_str)
                    except ValueError as e:
                        logger.error(f"Error restoring datetime reference '{block_value}': {e}")
                        return None
                
                # Snippet reference
                elif block_value.startswith('__snippet__'):
                    try:
                        snippet_str = block_value.replace('__snippet__', '')
                        model_name, snippet_id = snippet_str.rsplit('__', 1)
                        logger.debug(f"BlockApplicator: Converting reference to Snippet {model_name} with ID {snippet_id}")
                        
                        # Import the model class
                        module_path, class_name = model_name.rsplit('.', 1)
                        module = importlib.import_module(module_path)
                        model_class = getattr(module, class_name)
                        
                        # Fetch the snippet by ID
                        return model_class.objects.get(id=int(snippet_id))
                    except (ValueError, AttributeError, ImportError) as e:
                        logger.error(f"Error restoring snippet reference '{block_value}': {e}")
                        return None
                
            # Otherwise, return as is
            return block_value
            
        except Exception as e:
            logger.exception(f"Error processing block value: {e}")
            # Return the original to avoid breaking everything
            return block_value
    
    @classmethod
    def _looks_like_rich_text(cls, value: Any) -> bool:
        """
        Check if a value looks like it contains HTML markup from a RichText field.
        
        Args:
            value: The value to check
            
        Returns:
            True if the value appears to be rich text
        """
        if not isinstance(value, str):
            return False
            
        # Check for common HTML tags or patterns
        html_pattern = re.compile(r'<[a-z][^>]*>(.*?)</[a-z]>', re.IGNORECASE)
        wagtail_pattern = re.compile(r'data-block-key=["\']\w+["\']')
        
        return bool(html_pattern.search(value) or wagtail_pattern.search(value))


class BlockClipboardService:
    """
    Service for managing the block clipboard.
    """
    
    @classmethod
    def copy_to_clipboard(
        cls,
        user: User,
        page_id: int,
        block_id: str,
        label: str = ''
    ) -> Optional[int]:
        """
        Copy a block to the user's clipboard.
        
        Args:
            user: The user copying the block
            page_id: ID of the source page
            block_id: ID of the block to copy
            label: Optional label for the clipboard item
            
        Returns:
            ID of the clipboard item or None if failed
        """
        try:
            logger.info(f"BlockClipboardService: Copying block {block_id} from page {page_id} to clipboard")
            
            # Extract the block
            block_data = BlockExtractor.extract_block(page_id, block_id)
            if not block_data:
                logger.error(f"BlockClipboardService: Failed to extract block {block_id}")
                return None
                
            logger.info(f"BlockClipboardService: Successfully extracted block of type: {block_data.get('block_type', 'unknown')}")
            
            # Log the value structure
            try:
                # Use our custom encoder to ensure RichText objects are handled
                json_data = json.dumps(block_data.get('value', {}), cls=WagtailJSONEncoder, indent=2)
                logger.debug(f"BlockClipboardService: Block value: {json_data[:500]}...")
            except Exception as json_err:
                logger.warning(f"Could not log block value as JSON: {json_err}")
            
            # Create clipboard item
            try:
                # Make sure we serialize any RichText objects before saving to the database
                serialized_block_data = json.loads(json.dumps(block_data, cls=WagtailJSONEncoder))
                
                clipboard_item = BlockClipboard.objects.create(
                    user=user,
                    block_type=serialized_block_data.get('block_type', ''),
                    block_data=serialized_block_data,
                    source_page=page_id,
                    source_app='',  # Would determine this in a real implementation
                    label=label or f"Block from page {page_id}",
                    wagtail_version='.'.join(str(v) for v in WAGTAIL_VERSION),
                    schema_version='1.0',  # Would determine this in a real implementation
                    source_instance=''  # Would set this for cross-instance
                )
                
                logger.info(f"BlockClipboardService: Created clipboard item with ID {clipboard_item.id}")
                return clipboard_item.id
            except Exception as db_error:
                logger.exception(f"Error creating clipboard item: {db_error}")
                # Use our custom encoder to ensure proper error logging
                json_data = json.dumps(block_data, cls=WagtailJSONEncoder, default=str)
                logger.error(f"Block data: {json_data[:500]}...")  # Log first 500 chars
                raise
            
        except Exception as e:
            logger.exception(f"Error copying block to clipboard: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    @classmethod
    def paste_from_clipboard(
        cls,
        clipboard_id: int,
        page_id: int,
        field_name: Optional[str] = None,
        position: int = -1
    ) -> bool:
        """
        Paste a block from the clipboard to a page.
        
        Args:
            clipboard_id: The ID of the clipboard item
            page_id: The ID of the page to paste to
            field_name: Optional name of field to paste to (auto-detect if None)
            position: Position to insert the block at (-1 for append)
            
        Returns:
            True if the block was pasted successfully, False otherwise
        """
        try:
            # Get the clipboard item
            clipboard_item = BlockClipboard.objects.get(id=clipboard_id)
            
            # Apply the block to the page
            return BlockApplicator.apply_block_to_page(
                page_id,
                clipboard_item.block_data,
                field_name,
                position
            )
        except Exception as e:
            logger.exception(f"Error pasting block from clipboard: {e}")
            return False
    
    @classmethod
    def get_clipboard_for_user(cls, user: User) -> List[Dict[str, Any]]:
        """
        Get all clipboard items for a user.
        
        Args:
            user: The user
            
        Returns:
            List of serialized clipboard items
        """
        items = BlockClipboard.objects.filter(user=user).order_by('-timestamp')
        
        # Collect all page IDs to fetch in a single query
        page_ids = [item.source_page for item in items if item.source_page]
        pages_dict = {}
        
        if page_ids:
            # Fetch all pages in one query to avoid multiple DB hits
            pages = Page.objects.filter(id__in=page_ids)
            for page in pages:
                pages_dict[page.id] = page
        
        result = []
        for item in items:
            # Add basic preview info
            preview = cls._generate_block_preview(item.block_data)
            
            # Get page title if available
            page_title = None
            if item.source_page and item.source_page in pages_dict:
                page_title = pages_dict[item.source_page].title
            
            # Convert block_type to sentence case for display
            block_type_display = item.block_type.replace('_', ' ').capitalize()
            
            result.append({
                'id': item.id,
                'block_type': item.block_type,
                'block_type_display': block_type_display,
                'label': item.label or f"{block_type_display} block copied from {page_title or 'page'} {item.source_page}",
                'timestamp': item.timestamp.isoformat(),
                'source_page': item.source_page,
                'source_page_title': page_title,
                'preview': preview
            })
            
        return result
    
    @classmethod
    def _generate_block_preview(cls, block_data: Dict[str, Any]) -> str:
        """
        Generate a simple preview of a block.
        
        Args:
            block_data: The block data
            
        Returns:
            Preview text
        """
        # In a real implementation, this would generate a more useful preview
        block_type = block_data.get('block_type', 'Unknown')
        
        value = block_data.get('value', {})
        if isinstance(value, dict):
            # For simple StructBlocks, try to extract a title or name
            if 'title' in value:
                return f"{block_type}: {value['title']}"
            elif 'heading' in value:
                return f"{block_type}: {value['heading']}"
            elif 'name' in value:
                return f"{block_type}: {value['name']}"
            elif 'main_content' in value:
                content = value['main_content']
                if isinstance(content, str) and content:
                    return f"{block_type}: {content[:50]}..."
                
        return f"{block_type} block" 