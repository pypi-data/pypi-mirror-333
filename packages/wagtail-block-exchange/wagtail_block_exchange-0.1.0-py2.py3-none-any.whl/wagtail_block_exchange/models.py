from django.db import models
from django.conf import settings
from wagtail.admin.panels import FieldPanel


class BlockClipboard(models.Model):
    """
    Temporary storage for blocks that are being exchanged.
    This allows for copying blocks between editing sessions and instances.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='block_clipboard_items',
        help_text="The user who copied this block"
    )
    
    block_type = models.CharField(
        max_length=255,
        help_text="The type of block (StreamBlock name)"
    )
    
    block_data = models.JSONField(
        help_text="The serialized block data"
    )
    
    source_page = models.IntegerField(
        null=True,
        blank=True,
        help_text="ID of the page the block was copied from"
    )
    
    source_app = models.CharField(
        max_length=255,
        blank=True,
        help_text="The app that contains the source block"
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="When the block was copied"
    )
    
    label = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional label for this clipboard item"
    )
    
    # Add metadata for version compatibility
    wagtail_version = models.CharField(
        max_length=50,
        blank=True,
        help_text="Wagtail version at time of copying"
    )
    
    schema_version = models.CharField(
        max_length=50,
        blank=True,
        help_text="Schema version of the block"
    )
    
    # For cross-instance paste
    source_instance = models.CharField(
        max_length=255,
        blank=True,
        help_text="URL or identifier of source Wagtail instance"
    )
    
    class Meta:
        verbose_name = "Block Clipboard Item"
        verbose_name_plural = "Block Clipboard Items"
        ordering = ['-timestamp']
    
    panels = [
        FieldPanel('label'),
        FieldPanel('block_type'),
        FieldPanel('source_page'),
        FieldPanel('timestamp'),
        FieldPanel('source_instance'),
    ]
    
    def __str__(self):
        if self.label:
            return f"{self.label} ({self.block_type})"
        return f"{self.block_type} from page {self.source_page}" 