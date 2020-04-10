def star_filter_middleware(get_response):
    """
    Stores star filter data in user's session.
    """

    def middleware(request):
        assert hasattr(
            request, "session"
        ), "star_filter_middleware requires session middleware to be installed."
        limiting_magnitude = request.GET.get("limiting_magnitude")
        if limiting_magnitude:
            if limiting_magnitude == "None":
                limiting_magnitude = None
            request.session["limiting_magnitude"] = limiting_magnitude
        stars_with_observations = request.GET.get("stars_with_observations")
        if stars_with_observations:
            if stars_with_observations == "True":
                stars_with_observations = True
            else:
                stars_with_observations = False
            request.session["stars_with_observations"] = stars_with_observations
        return get_response(request)

    return middleware
