from seatsurfing.booking import Bookings


class Client:
    """Client to interact with Seatsurfing."""

    def __init__(self, base_url: str, username: str, password: str):
        self.booking = Bookings(base_url, username=username, password=password)
