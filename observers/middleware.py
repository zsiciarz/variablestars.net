from .models import Observer


def observer_middleware(get_response):
    """
    Attaches an observer instance to every request coming from an
    authenticated user.
    """
    def middleware(request):
        assert hasattr(request, 'user'), "observer_middleware requires auth middleware to be installed."
        if request.user and request.user.is_authenticated:
            request.observer = Observer.objects.get(user=request.user)
        else:
            request.observer = None
        return get_response(request)
    return middleware
