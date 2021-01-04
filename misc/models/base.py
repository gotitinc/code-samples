import json
import logging
from datetime import datetime


class TimestampMixin(object):
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# Used to track modifications for the after_commit hook. See the comments on after_commit
class TrackChangesMixin:
    def reset_tracked_changes(self):
        self.__tracked_changes__ = set()

    def track_change(self, prop):
        self.__tracked_changes__.add(prop)

    def get_tracked_changes(self):
        return self.__tracked_changes__

    def initialize_tracked_changes(self):
        if not hasattr(self, '__tracked_changes__'):
            self.__tracked_changes__ = set()


class MetaDataMixin:
    _meta_data = db.Column('meta_data', db.Text)

    @property
    def meta_data(self):
        try:
            return json.loads(self._meta_data) or {}
        except Exception as e:
            logging.exception(str(e))
            return {}

    @meta_data.setter
    def meta_data(self, value):
        if value is not None:
            self._meta_data = json.dumps(value)
