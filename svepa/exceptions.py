

class SvepaException(Exception):
    def __init__(self, message='', title=''):
        if not title:
            title = 'Unknown error'
        self.message = message
        super().__init__(f'Svepa: {title}: {message}')


class SvepaConnectionError(SvepaException):
    def __init__(self, message=''):
        super().__init__(message=message, title='Connection error')


class SvepaEventTypeNotRunningError(SvepaException):
    def __init__(self, message='', event_type=''):
        self.event_type = event_type
        super().__init__(message=message, title=f'Event type not running: {event_type}')


class SvepaNoInformationError(SvepaException):
    def __init__(self, message=''):
        super().__init__(message=message, title='Missing information')
