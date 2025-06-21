from collections import deque

def round_robin_scheduling(bookings, time_quantum):
    if not bookings:
        return [], []

    bookings.sort(key=lambda x: x.arrival_time)

    queue = deque()
    current_time = bookings[0].arrival_time
    index = 0
    scheduled = []
    execution_log = []
    remaining_time = {b.id: b.duration for b in bookings}
    first_start = {}

    while index < len(bookings) and bookings[index].arrival_time <= current_time:
        queue.append(bookings[index])
        index += 1

    while queue:
        current_booking = queue.popleft()

        if current_booking.id not in first_start:
            current_booking.start_time = current_time
            first_start[current_booking.id] = True

        time_slice = min(time_quantum, remaining_time[current_booking.id])
        start_exec = current_time
        current_time += time_slice
        end_exec = current_time
        remaining_time[current_booking.id] -= time_slice

        execution_log.append({
            'id': current_booking.id,
            'name': current_booking.name,
            'nim': current_booking.nim,
            'start': start_exec,
            'end': end_exec,
            'duration': time_slice
        })

        while index < len(bookings) and bookings[index].arrival_time <= current_time:
            queue.append(bookings[index])
            index += 1

        if remaining_time[current_booking.id] > 0:
            queue.append(current_booking)
        else:
            current_booking.end_time = current_time
            scheduled.append(current_booking)

    return scheduled, execution_log