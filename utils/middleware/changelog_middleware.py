from utils.singletone import Singleton


class LoggedInUser(Singleton):
    """Синглтон для хранения пользователя, от имени которого выполняется запрос"""
    __metaclass__ = Singleton

    request = None
    user = None

    def set_data(self, request):
        self.request = id(request)
        if request.user.is_authenticated:
            self.user = request.user

    @property
    def current_user(self):
        return self.user

    @property
    def have_user(self):
        return self.user is not None


class LoggedInUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Инициализирует синглтон LoggedInUser
        """
        logged_in_user = LoggedInUser()
        logged_in_user.set_data(request)

        response = self.get_response(request)

        return response
