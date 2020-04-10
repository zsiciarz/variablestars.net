import time


def jd_now():
    """
    Returns Julian Date at the current moment.
    """
    return 2440587.5 + time.time() / 86400.0


def normalize_star_name(name):
    """
    Normalize star name with GCVS names, for example: V339 -> V0339.
    """
    digits = "123456789"
    if name[0] == "V" and name[1] in digits and name[4] not in digits:
        name = "V0" + name[1:]
    return name


def dict_to_observation(row, observer):
    from .models import Observation
    from stars.models import Star

    name = normalize_star_name(row["name"])
    star = Star.objects.get(name=name)
    fainter_than = "<" in row["magnitude"]
    magnitude = float(row["magnitude"].replace("<", ""))
    jd = float(row["date"])
    # TODO: use get_or_create with defaults
    try:
        observation = Observation.objects.get(observer=observer, star=star, jd=jd,)
    except Observation.DoesNotExist:
        observation = Observation(observer=observer, star=star, jd=jd,)
    observation.magnitude = magnitude
    observation.fainter_than = fainter_than
    observation.comp1 = row["comp1"]
    observation.comp2 = row.get("comp2", "")
    observation.chart = row["chart"]
    observation.comment_code = row["comment_code"]
    observation.notes = row["notes"]
    return observation
