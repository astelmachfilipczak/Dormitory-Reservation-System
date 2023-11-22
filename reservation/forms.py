"""
Module containing Django forms for room reservations in the application.

Forms:
- RoomReservationForm: A form for handling room reservation submissions.

The RoomReservationForm is a ModelForm associated with the RoomReservation model. It includes customization to
limit the number of people based on the selected dormitory room. The form uses date widgets for the check-in
and check-out date fields.

Author: [ASF]
Creation Date: [13.11.2023]
"""

from django import forms
from .models import RoomReservation, DormRoom
from django.core.exceptions import ValidationError

class RoomReservationForm(forms.ModelForm):
    """
        Form for handling room reservation submissions.

        Attributes:
        - room (ModelChoiceField): Dropdown field for selecting a dormitory room.
        - check_in_date (DateField): Date input field for the reservation start date.
        - check_out_date (DateField): Date input field for the reservation end date.
        - number_of_people (IntegerField): Field for entering the number of people for the reservation.

        Methods:
        - __init__(self, *args, **kwargs): Initializes the form and sets dynamic constraints based on the selected room.
        - clean(self): Custom form validation method to check if the check-out date is after the check-in date.
        """

    class Meta:
        model = RoomReservation
        fields = ['room', 'check_in_date', 'check_out_date', 'number_of_people']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(RoomReservationForm, self).__init__(*args, **kwargs)
        if 'room' in self.fields:
            room_id = kwargs.get('initial', {}).get('room')

            if room_id:
                self.room = DormRoom.objects.get(id=room_id)
                max_people = self.room.get_beds()
                self.fields['number_of_people'].widget.attrs['min'] = 1
                self.fields['number_of_people'].widget.attrs['max'] = max_people
                self.fields['number_of_people'].label = f'Number of People (max {max_people})'

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        number_of_people = cleaned_data.get('number_of_people')


        if check_in_date and check_out_date and check_out_date < check_in_date:
            self.add_error('check_out_date', "Check-out date must be after check-in date")

        if hasattr(self, 'room') and number_of_people and number_of_people > self.room.get_beds():
            self.add_error('number_of_people', "Number of people exceeds the room capacity")

        return cleaned_data