"""
Module containing Django tests for form of room reservation in the application.

Tests:
- RoomReservationFormTest: Test case for the RoomReservationForm class, covering form validation scenarios.

Author: [ASF]
Creation Date: [13.11.2023]
"""

from django.test import TestCase
from datetime import date
from .models import DormRoom
from .forms import RoomReservationForm


class RoomReservationFormTest(TestCase):
    """
    Test case for the RoomReservationForm class.

    Methods:
    - setUp(self): Initializes common data used in multiple tests.
    - test_valid_form(self): Test if the form is valid with correct data.
    - test_invalid_check_out_before_check_in(self): Test if the form is invalid with check-out date before check-in date.
    - test_invalid_number_of_people(self): Test if the form is invalid with the number of people exceeding room capacity.
    - test_dynamic_constraints_update(self): Test if dynamic constraints are updated based on the selected room.
    """

    def setUp(self):
        self.room = DormRoom.objects.create(city='TestCity', room_type='triple', mini_kitchenette=True,
                                            private_bathroom=True, price=500.00)

    def test_valid_form(self):
        data = {
            'room': self.room.id,
            'check_in_date': date(2023, 11, 15),
            'check_out_date': date(2023, 11, 20),
            'number_of_people': 2,
        }
        form = RoomReservationForm(data=data, initial={'room': self.room.id})
        self.assertTrue(form.is_valid())

    def test_invalid_check_out_before_check_in(self):
        data = {
            'room': self.room.id,
            'check_in_date': date(2023, 11, 20),
            'check_out_date': date(2023, 11, 15),
            'number_of_people': 2,
        }
        form = RoomReservationForm(data=data, initial={'room': self.room.id})
        self.assertFalse(form.is_valid())
        self.assertIn('check_out_date', form.errors)

    def test_invalid_number_of_people(self):
        data = {
            'room': self.room.id,
            'check_in_date': date(2023, 11, 15),
            'check_out_date': date(2023, 11, 20),
            'number_of_people': 5,
        }
        form = RoomReservationForm(data=data, initial={'room': self.room.id})

        self.assertFalse(form.is_valid())
        self.assertIn('number_of_people', form.errors)

    def test_dynamic_constraints_update(self):
        room_2 = DormRoom.objects.create(city='TestCity', room_type='double', mini_kitchenette=True,
                                         private_bathroom=True, price=400.00)

        initial_data = {'room': room_2.id}
        form = RoomReservationForm(initial=initial_data)

        self.assertEqual(form.fields['number_of_people'].widget.attrs['min'], 1)
        self.assertEqual(form.fields['number_of_people'].widget.attrs['max'], room_2.get_beds())
        self.assertEqual(form.fields['number_of_people'].label, f'Number of People (max {room_2.get_beds()})')
