from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import Flight, Booking
from django.http import HttpResponse


def payment(request, flight_id):

    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == "POST":
        messages.success(request, "Payment Successful!")
        return redirect("confirmation")

    return render(request, "payment.html", {
        "flight": flight
    })


def download_ticket(request):
    from reportlab.pdfgen import canvas

    booking = Booking.objects.last()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, 800, "AeroReserve Ticket")

    p.setFont("Helvetica", 12)

    p.drawString(50, 750, f"Passenger : {booking.passenger_name}")
    p.drawString(50, 730, f"Flight : {booking.flight.airline}")
    p.drawString(50, 710, f"Flight No : {booking.flight.flight_number}")
    p.drawString(50, 690, f"Route : {booking.flight.source} → {booking.flight.destination}")
    p.drawString(50, 670, f"Seat : {booking.seat_number}")
    p.drawString(50, 650, f"Departure : {booking.flight.departure_time}")
    p.drawString(50, 630, f"Arrival : {booking.flight.arrival_time}")
    p.drawString(50, 610, f"Fare : ₹{booking.flight.price}")

    p.save()

    return response




def home(request):

    flights = Flight.objects.all()

    source = request.GET.get("source")
    destination = request.GET.get("destination")

    if source and destination:
        flights = flights.filter(
            source__icontains=source,
            destination__icontains=destination
        )

    return render(request, "flight.html", {
        "flights": flights
    })


def login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(request, "Registration Successful")
            return redirect("login")

    return render(request, "register.html")


@login_required(login_url='login')
def booking(request, flight_id):

    flight = Flight.objects.get(id=flight_id)

    booked_seats = Booking.objects.filter(
        flight=flight
    ).values_list("seat_number", flat=True)

    all_seats = [
        "A1", "A2", "A3", "A4",
        "B1", "B2", "B3", "B4",
        "C1", "C2", "C3", "C4"
    ]

    available_seats = [
        seat for seat in all_seats
        if seat not in booked_seats
    ]

    if request.method == "POST":

        passenger_name = request.POST["passenger_name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        seat_number = request.POST["seat_number"]

        if not passenger_name or not email or not phone or not seat_number:
            messages.error(request, "All fields are required.")
            return render(request, "booking.html", {
                "flight": flight,
                "available_seats": available_seats
            })

        Booking.objects.create(
            user=request.user,
            flight=flight,
            passenger_name=passenger_name,
            email=email,
            phone=phone,
            seat_number=seat_number
        )

        messages.success(request, "Flight Booked Successfully!")
        return redirect("payment", flight_id=flight.id)

    return render(request, "booking.html", {
        "flight": flight,
        "available_seats": available_seats
    })


def confirmation(request):

    booking = Booking.objects.last()

    return render(request, "confirmation.html", {
        "booking": booking
    })


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url='login')
def my_bookings(request):

    bookings = Booking.objects.filter(user=request.user)

    return render(request, "mybookings.html", {
        "bookings": bookings
    })


@login_required(login_url='login')

def cancel_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    booking.delete()

    return redirect("my_bookings")


@login_required(login_url='login')
def profile(request):

    total_bookings = Booking.objects.filter(
        user=request.user
    ).count()

    return render(request, "profile.html", {
        "total_bookings": total_bookings
    })


def flight_status(request, flight_id):

    flight = Flight.objects.get(id=flight_id)

    return render(request, "flight_status.html", {
        "flight": flight
    })