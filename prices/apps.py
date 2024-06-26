from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class PricesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prices'

    def ready(self):
        # Connect using the class and static method
        post_migrate.connect(self.post_migration_setup, sender=self)

    @staticmethod
    @receiver(post_migrate)
    def post_migration_setup(sender, **kwargs):
        try:
            from prices.jobs.commands.sync_price_tasks import create_or_update_price_tasks
            create_or_update_price_tasks()
        except Exception as e:
            logger.error(f'Error during post_migration_setup: {str(e)}')
