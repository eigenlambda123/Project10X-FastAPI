from celery import shared_task

@shared_task
def fake_long_task(x):
    # Simulate a long task
    import time
    time.sleep(5)
    return x * 2