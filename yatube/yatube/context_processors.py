import datetime as dt


def current_year(request):
    year = dt.datetime.now().year
    return {'year': year}
