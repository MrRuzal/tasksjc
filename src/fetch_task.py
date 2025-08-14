from django.db import transaction
from .models import TaskQueue


def fetch_task():
    with transaction.atomic():
        task = (
            TaskQueue.objects.select_for_update(skip_locked=True)
            .filter(status='pending')
            .order_by('created_at')
            .first()
        )

        if not task:
            return None

        task.status = 'in_progress'
        task.save(update_fields=['status', 'updated_at'])
        return task
