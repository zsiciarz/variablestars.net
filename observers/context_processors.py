def get_current_observer(request):
    return {
        'current_observer': getattr(request, 'observer', None),
    }
