from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from booking.models import User, Booking, Concert
from django.db.models import Sum


class ArtistSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_artist = True
        if commit:
            user.save()
        return user


class UserSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_user = True
        if commit:
            user.save()
        return user


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields= ['concert','seat_type','no_of_seat', 'payment_type', 'amount']

    def clean(self):
        # data from the form is fetched using super function
        super(BookingForm, self).clean()
        
        # extract the username and text field from the data
        no_of_seat = self.cleaned_data.get('no_of_seat')
        seat_type = self.cleaned_data.get('seat_type')
        concert = self.cleaned_data.get('concert')
        try:
            # Booking.objects.aggregate(all_sum=Sum('price'))
            concert_modal = Concert.objects.get(id = concert.id)
            for p in concert_modal.seat.all():
                if p.seat_type == seat_type and int(no_of_seat) > int(p.no_of_seat):
                    self._errors['no_of_seat'] = self.error_class([
                    'The numbers of seat are unavailable at the moment'])

        except Exception as ex:
            print(ex)
            self._errors['concert'] = self.error_class([
                'Please select the concert'])


        return self.cleaned_data

        # def save(self, commit=True):
        #     user = super().save(commit=False)
        #     user.is_user = True
        #     if commit:
        #         user.save()
        #     return user