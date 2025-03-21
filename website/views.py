from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import ComputerBooking, PrinterBooking, LaserBooking, User  # Update this line
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/booking/computer', methods=['GET', 'POST'])
@login_required
def booking_computer():
    if request.method == 'POST':
        try:
            # Get form data
            date_str = request.form.get('booking_date')
            start_time_str = request.form.get('booking_start_time')
            end_time_str = request.form.get('booking_end_time')
            booking = request.form.get('booking')
            
            if not all([date_str, start_time_str, end_time_str, booking]):
                return jsonify({'success': False, 'error': 'Missing required fields'})

            # Convert strings to datetime objects
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').strftime('%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M').strftime('%H:%M')

            new_booking = ComputerBooking(
                computer_number=booking,
                booking_date=booking_date,
                booking_start_time=start_time,
                booking_end_time=end_time,
                user_id=current_user.id
            )
            
            db.session.add(new_booking)
            db.session.commit()
            return jsonify({'success': True})

        except ValueError as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': f'Invalid date or time format: {str(e)}'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            db.session.remove()

    return render_template("bookingCom.html", user=current_user)

@views.route('/booking/3d', methods=['GET', 'POST'])
@login_required
def booking_3d():
    if request.method == 'POST':
        try:
            # Get form data
            date_str = request.form.get('booking_date')
            start_time_str = request.form.get('booking_start_time')
            end_time_str = request.form.get('booking_end_time')
            booking = request.form.get('booking')
            printer_number = request.form.get('printer_number')

            if not all([date_str, start_time_str, end_time_str, booking]):
                raise ValueError("Missing required fields")

            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').strftime('%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M').strftime('%H:%M')

            new_booking = PrinterBooking(
                printer_model=booking,
                printer_number=printer_number,
                booking_date=booking_date,
                booking_start_time=start_time,
                booking_end_time=end_time,
                user_id=current_user.id
            )
            
            db.session.add(new_booking)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            db.session.remove()

    return render_template("booking3D.html", user=current_user)

@views.route('/booking/laser', methods=['GET', 'POST'])
@login_required
def booking_laser():
    if request.method == 'POST':
        try:
            date_str = request.form.get('booking_date')
            start_time_str = request.form.get('booking_start_time')
            end_time_str = request.form.get('booking_end_time')
            booking = request.form.get('booking')
            laser_number = request.form.get('laser_number')

            if not all([date_str, start_time_str, end_time_str, booking]):
                raise ValueError("Missing required fields")

            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').strftime('%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M').strftime('%H:%M')

            new_booking = LaserBooking(
                laser_model=booking,
                laser_number=laser_number,
                booking_date=booking_date,
                booking_start_time=start_time,
                booking_end_time=end_time,
                user_id=current_user.id
            )
            
            db.session.add(new_booking)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            db.session.remove()

    return render_template("bookingLaser.html", user=current_user)

@views.route('/debug/bookings')
@login_required
def debug_bookings():
    bookings = ComputerBooking.query.all()
    return render_template(
        "debug_bookings.html",
        bookings=bookings,
        user=current_user
    )

@views.route('/get-computer-bookings')
@login_required
def get_computer_bookings():
    today = datetime.now().date()
    bookings = ComputerBooking.query.filter(
        ComputerBooking.booking_date >= today
    ).order_by(ComputerBooking.booking_date, ComputerBooking.booking_start_time).all()
    
    bookings_list = []
    for booking in bookings:
        user = User.query.get(booking.user_id)
        bookings_list.append({
            'username': user.userName if user else 'Unknown',  # Changed from username to userName
            'computer': booking.computer_number,
            'date': booking.booking_date.strftime('%Y-%m-%d'),
            'time_start': booking.booking_start_time,
            'time_end': booking.booking_end_time
        })
    return jsonify(bookings_list)

@views.route('/get-printer-bookings')
@login_required
def get_printer_bookings():
    today = datetime.now().date()
    bookings = PrinterBooking.query.filter(
        PrinterBooking.booking_date >= today
    ).order_by(PrinterBooking.booking_date, PrinterBooking.booking_start_time).all()
    
    bookings_list = []
    for booking in bookings:
        user = User.query.get(booking.user_id)
        bookings_list.append({
            'username': user.userName if user else 'Unknown',
            'printer': booking.printer_model,
            'number': booking.printer_number,
            'date': booking.booking_date.strftime('%Y-%m-%d'),
            'time_start': booking.booking_start_time,
            'time_end': booking.booking_end_time
        })
    return jsonify(bookings_list)

@views.route('/get-laser-bookings')
@login_required
def get_laser_bookings():
    today = datetime.now().date()
    bookings = LaserBooking.query.filter(
        LaserBooking.booking_date >= today
    ).order_by(LaserBooking.booking_date, LaserBooking.booking_start_time).all()
    
    bookings_list = []
    for booking in bookings:
        user = User.query.get(booking.user_id)
        bookings_list.append({
            'username': user.userName if user else 'Unknown',
            'laser_model': booking.laser_model,
            'laser_number': booking.laser_number,
            'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
            'booking_start_time': booking.booking_start_time,
            'booking_end_time': booking.booking_end_time
        })
    return jsonify(bookings_list)