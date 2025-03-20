import logging
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from django.apps import apps

logger = logging.getLogger(__name__)

@receiver(post_migrate)
def create_initial_structure(sender, **kwargs):
    """
    Create the necessary structure for the block exchange app after migrations.
    """
    # Only run for our app
    if sender.name != 'wagtail_block_exchange':
        return
        
    # Run any necessary setup
    logger.info("Setting up wagtail_block_exchange app...")
    
    # Create static directories, etc.
    try:
        pass  # Additional setup would go here
    except Exception as e:
        logger.exception(f"Error setting up wagtail_block_exchange: {e}") 