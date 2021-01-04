from flask_sqlalchemy import SignallingSession
from sqlalchemy import inspect
from sqlalchemy.event import listen


class ModelOperation:
    UPDATE = 'update'
    INSERT = 'insert'

    @classmethod
    def get_list(cls):
        return [cls.UPDATE, cls.INSERT]


def _on_model_committed(model_instance, operation):
    pass


def _after_commit_handler(session):
    if hasattr(session, '_tracked_models'):
        for (model, operation) in session._tracked_models:
            _on_model_committed(model, operation)
            model.reset_tracked_changes()
        session._tracked_models.clear()


def _after_rollback_handler(session):
    if hasattr(session, '_tracked_models'):
        for (model, operation) in session._tracked_models:
            model.reset_tracked_changes()
        session._tracked_models.clear()


def _after_flush_handler(session, flush_ctx):
    if not hasattr(session, '_tracked_models'):
        session._tracked_models = set()
    for obj in session.dirty:
        if getattr(obj, 'track_change', None):
            obj.initialize_tracked_changes()
            session._tracked_models.add((obj, ModelOperation.UPDATE))
            for prop in obj.__track_changes__:
                if inspect(obj).attrs[prop].history.has_changes():
                    obj.track_change(prop)
    for obj in session.new:
        if getattr(obj, 'track_change', None):
            session._tracked_models.add((obj, ModelOperation.INSERT))
            obj.initialize_tracked_changes()
            for prop in obj.__track_changes__:
                obj.track_change(prop)


listen(SignallingSession, 'after_commit', _after_commit_handler)
listen(SignallingSession, 'after_flush', _after_flush_handler)
listen(SignallingSession, 'after_rollback', _after_rollback_handler)