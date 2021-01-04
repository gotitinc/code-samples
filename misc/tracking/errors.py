class EventTrackingServiceException(Exception):
    def __init__(self, message, data=None):
        super(EventTrackingServiceException, self).__init__(message)
        self.data = data
        self.message = message

    def __str__(self):
        return '<EventTrackingServiceException: {}, data={}>'.format(self.message, self.data)
