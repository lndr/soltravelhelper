import astropy.coordinates as ac
import astropy.time as at
import astropy.units as au
import datetime as dt


def distance(position, destination, date=None):
    """Calculate the distance between two planets.

    Args:
        position: Planet the journey starts at.
        destination: Destination of the journey.
        date: Date the journey is started (defaults to current time).

    Returns:
        Distance in m.
    """

    if not date:
        date = dt.datetime.now()
    time = at.Time(date)
    return (ac.get_body_barycentric(position, time) -
            ac.get_body_barycentric(destination, time)).norm().to(au.m).value


def time_constant_acceleration(position, destination, acceleration, date=None):
    """Predict travel time when accelerating constantly for the first half of the journey,
    that slowing down at the same rate for the second half.

    Args:
        position: Planet the journey starts at.
        destination: Destination of the journey.
        acceleration: Acceleration in m/s^2.
        date: Date the journey is started (defaults to current time).

    Returns:
        Travel time as dt.timedelta.
    """

    return dt.timedelta(seconds=2 * (distance(position, destination, date) / acceleration) ** 0.5)


def time_constant_velocity(position, destination, velocity, date=None):
    """Predict travel time with constant velocity.

    Args:
        position: Planet the journey starts at.
        destination: Destination of the journey.
        velocity: Velocity in m/s.
        date: Date the journey is started (defaults to current time).

    Returns:
        Travel time as dt.timedelta.
    """

    return dt.timedelta(seconds=distance(position, destination, date) / velocity)
