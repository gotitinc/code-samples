import os
import event_bus


@app.after_request
def execute_delayed_deferred(response):
    if os.getenv('ENVIRONMENT') == 'test':
        return response
    for task in getattr(g, 'delayed_tasks', []):
        event_bus.send_task(task)
    return response