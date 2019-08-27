from celery.schedules import crontab
from .tasks.tasks import *
from .tasks.celery_conf import app


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, add(1,2), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(15.0, add(5,6), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        add(15, 16),
    )

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'result.tasks.tasks.add',
        'schedule': 50.0,
        'args': (16, 16)
    },
    'handle_feed_report_all': {
        'task': 'result.tasks.tasks.add',
        'schedule': crontab(hour='*/1', minute='10')
    },
}


def on_raw_message(body):
    print(body)


add.apply_async((1,6), queue="celery_func_add")
add.apply_async((2,3), queue="celery_func_add")
add.apply_async((4,6), queue="celery_func_add")
