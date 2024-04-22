import importlib
import json
from django.utils.timezone import now

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from prices.models import DataSources


def create_or_update_price_tasks():
    for source in DataSources.objects.all():
        # Construct the task module and function name strings
        module_name = f'prices.jobs.{source.key.lower()}'
        job_function_name = 'fetch_data'  # Assuming a consistent function name across modules

        try:
            # Attempt to import the module
            module = importlib.import_module(module_name)
            # Check if the task function exists in the module
            if not hasattr(module, job_function_name):
                raise AttributeError(f"The job function '{job_function_name}' was not found in '{module_name}'.")

            # Proceed to create or update the periodic task
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=source.frequency,
                period=IntervalSchedule.MINUTES,
            )

            # Use the consistent function name for the task
            task_path = f'{module_name}.{job_function_name}'
            task, created = PeriodicTask.objects.update_or_create(
                name=f'{source.key}_fetch_task',
                defaults={
                    'task': task_path,
                    'interval': schedule,
                    'args': json.dumps([source.id]),
                    'start_time': now(),  # Starts From Now

                }
            )
        except ModuleNotFoundError:
            print(f"The module '{module_name}' does not exist.")
        except AttributeError as e:
            print(e)
