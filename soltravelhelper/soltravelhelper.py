import astropy.coordinates as ac
import astropy.time as at
import astropy.units as au
import datetime as dt
import logging as lg

logger = lg.getLogger('travellogbook')


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


def velocity_after_time(acceleration, time):
    """Calculate velocity after accelerating for a given time.

    Args:
        acceleration: Acceleration in m/s^2.
        time: Time in seconds or as dt.timedelta.

    Returns:
        Velocity in m/s.
    """

    if type(time) == dt.timedelta:
        time = time.total_seconds()
    return acceleration * time


class Traveler:
    """Class to represents a traveling group / spaceship."""

    def __init__(self, position='earth', date=None):
        """Class constructor.

        Args:
            position: Starting planet (defaults to earth).
            date: Starting date (defaults to current time).
        """
        if not date:
            date = dt.datetime.now()
        self.date = date
        self.current_position = position
        logger.info('Started journey on {} on {}'.format(
            self.current_position, self.date.strftime('%Y-%m-%d at %H:%M:%S')))

    def idle_hours(self, hours):
        """Wait for a given number of hours (add them to date).

        Args:
            hours: Hours the group / spaceship idles.
        """
        self.date += dt.timedelta(hours=hours)
        logger.info('Idled on {} until {}'.format(
            self.current_position, self.date.strftime('%Y-%m-%d at %H:%M:%S')))

    def travel_constant_acceleration(self, destination, acceleration):
        """Travel to the given planet using the constant acceleration method.

        Args:
            destination: Destination of the journey.
            acceleration: Acceleration in m/s^2.
        """
        self.date += time_constant_acceleration(self.current_position, destination,
                                                acceleration, self.date)
        self.current_position = destination
        logger.info('Arrived on {} on {}'.format(
            self.current_position, self.date.strftime('%Y-%m-%d at %H:%M:%S')))

    def travel_constant_velocity(self, destination, velocity):
        """Travel to the given planet using the constant velocity method.

        Args:
            destination: Destination of the journey.
            velocity: Velocity in m/s^2.
        """
        self.date += time_constant_velocity(self.current_position, destination,
                                            velocity, self.date)
        self.current_position = destination
        logger.info('Arrived on {} on {}'.format(
            self.current_position, self.date.strftime('%Y-%m-%d at %H:%M:%S')))
