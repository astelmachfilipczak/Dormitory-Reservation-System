"""
Module containing Django models for room reservations in the application.

Models:
- DormRoom: Represents a dormitory room with various attributes.
- RoomReservation: Represents a reservation made by a user for a dormitory room.

The DormRoom model includes methods to retrieve information about the room, such as the number of beds,
bathroom type, and kitchenette availability. It also provides a method to check the availability of the room
for a given date range.

The RoomReservation model is associated with a specific user and dormitory room. It includes a method to check
if the reservation is still open.

Author: [ASF]
Creation Date: [13.11.2023]
"""

from django.db import models
from django.contrib.auth.models import User


class DormRoom(models.Model):
    """
    Model representing a dormitory room.

    Attributes:
    - city (str): The city where the dormitory is located.
    - street (str): The street where the dormitory is located.
    - room_type (str): The type of the room (e.g., single, double, triple).
    - mini_kitchenette (bool): Indicates if the room has a mini kitchenette.
    - private_bathroom (bool): Indicates if the room has a private bathroom.
    - price (Decimal): The price of the room.
    - image_name (str): The filename of the room's image.

    Methods:
    - __str__(): Returns a string representation of the room.
    - get_beds(): Returns the number of beds in the room based on its type.
    - get_bathroom_type(): Returns the type of bathroom in the room (private or shared).
    - get_mini_kitchenette(): Returns "Yes" if the room has a mini kitchenette, "No" otherwise.
    - is_available(start_date, end_date): Checks if the room is available for reservation between specified dates.
    """

    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=30, default='street')
    room_type = models.CharField(max_length=10)
    mini_kitchenette = models.BooleanField()
    private_bathroom = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_name = models.CharField(max_length=100, default='room-1.jpg')

    def __str__(self):
        return f'{self.city} - Room {self.id}'

    def get_beds(self):
        if self.room_type == 'single':
            return 1
        elif self.room_type == 'double':
            return 2
        else:
            return 3

    def get_bathroom_type(self):
        if self.private_bathroom:
            return "Private"
        else:
            return "Shared"

    def get_mini_kitchenette(self):
        if self.mini_kitchenette:
            return "Yes"
        else:
            return "No"

    def is_available(self, start_date, end_date):
        reservations = RoomReservation.objects.filter(
            room=self,
            check_in_date__gte=start_date,
            check_out_date__lte=end_date
        )
        return not reservations.exists()


class RoomReservation(models.Model):
    """
       Model representing a reservation for a dormitory room.

       Attributes:
       - user (User): The user who made the reservation.
       - room (DormRoom): The dormitory room being reserved.
       - check_in_date (Date): The date when the reservation starts.
       - check_out_date (Date): The date when the reservation ends.
       - is_open (bool): Indicates whether the reservation is open or closed.
       - number_of_people (int): The number of people the reservation is for.

       Methods:
       - __str__(): Returns a string representation of the reservation.
       - is_open_reservation(): Checks if the reservation is still open.
       """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(DormRoom, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    is_open = models.BooleanField(default=True)
    number_of_people = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Reservation for {self.room.city} - Room {self.room.id}'

    def is_open_reservation(self):
        return self.is_open
