class Notification:
    def __init__(self, text, ):
        self.text = text


class LikeProjectNotification(Notification):
    def __init__ (self):
        super.__init__(self)