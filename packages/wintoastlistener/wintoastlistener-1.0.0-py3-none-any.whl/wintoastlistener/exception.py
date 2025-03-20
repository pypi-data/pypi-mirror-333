class ToastParserException(Exception):
    """
    Toast xml parser exception
    """

    def __init__(self, message):
        super(ToastParserException, self).__init__(message)
        self.message = message


class ToastEvtSubscribeActionError(Exception):
    """
    Toast event subscribe action error exception
    """

    def __init__(self, message):
        super(ToastEvtSubscribeActionError, self).__init__(message)
        self.message = message


class ToastEvtSubscribeActionUnknown(Exception):
    """
    Toast event subscribe action unknown exception
    """

    def __init__(self, message):
        super(ToastEvtSubscribeActionUnknown, self).__init__(message)
        self.message = message


class ToastNotificationsDBNotExist(Exception):
    """
    Toast notifications db does not exist check.
    """

    def __init__(self, message):
        super(ToastNotificationsDBNotExist, self).__init__(message)
        self.message = message
