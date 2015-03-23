from .models import Observer


class ObserverMiddleware(object):
    """
    Attaches an observer instance to every request coming from an
    authenticated user.
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), "ObserverMiddleware requires auth middleware to be installed."
        if request.user and request.user.is_authenticated():
            request.observer = Observer.objects.get(user=request.user)
        else:
            request.observer = None
