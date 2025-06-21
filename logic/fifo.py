def fifo_scheduling(bookings):
    bookings.sort(key=lambda x: x.arrival_time)
    
    current_time = 0
    scheduled = []
    
    for booking in bookings:
        if current_time < booking.arrival_time:
            current_time = booking.arrival_time
        
        booking.start_time = current_time
        booking.end_time = current_time + booking.duration
        scheduled.append(booking)
        current_time += booking.duration
    
    return scheduled