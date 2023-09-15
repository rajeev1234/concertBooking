from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.forms import BookingForm
from django.shortcuts import redirect

# Create your views here.
from .models import Concert
from django.http import Http404
def concert_list(request):
    concert_list = Concert.objects.all().order_by('popularity_index')
    top_concert = Concert.objects.all().order_by('popularity_index')[:3]
    return render(request, 'booking.html', {'concert_list': concert_list,'top_concert': top_concert})

@login_required
def concert_details(request, booking_id):
	form = BookingForm(request.POST)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.paid_by = request.user
		instance.save()
		return redirect('user_concert_list')
	try:
		concert_info = Concert.objects.get(pk=booking_id)
		concert_list = Concert.objects.all()
	except Concert.DoesNotExist:
		raise Http404("Page does not exist")
	return render(request, 'template/user/booking_details.html',
		{'concert_info': concert_info, 'concert_list': concert_list, 'form': form})