import heapq

def sjf_scheduling(bookings):
    bookings.sort(key=lambda x: x.arrival_time)
    
    current_time = 0
    scheduled = []
    ready_queue = []
    index = 0
    
    while index < len(bookings) or ready_queue:
        while index < len(bookings) and bookings[index].arrival_time <= current_time:
            heapq.heappush(ready_queue, (bookings[index].duration, index, bookings[index]))
            index += 1
        
        if ready_queue:
            _, _, shortest = heapq.heappop(ready_queue)
            shortest.start_time = current_time
            shortest.end_time = current_time + shortest.duration
            scheduled.append(shortest)
            current_time += shortest.duration
        else:
            if index < len(bookings):
                current_time = bookings[index].arrival_time
    
    return scheduled