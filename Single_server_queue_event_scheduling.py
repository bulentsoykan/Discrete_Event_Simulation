import heapq
import random

class Event:
    def __init__(self, time, event_type):
        self.time = time
        self.event_type = event_type

    def __lt__(self, other):
        return self.time < other.time  # For priority queue


class DiscreteEventSimulation:
    ARRIVAL = "ARRIVAL"
    DEPARTURE = "DEPARTURE"

    def __init__(self, arrival_rate, service_rate, simulation_time):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.simulation_time = simulation_time

        self.current_time = 0
        self.event_list = []  # Future event list (priority queue)
        self.queue = []       # Customer queue
        self.server_busy = False

        # Statistics
        self.served_customers = 0
        self.total_wait_time = 0
        self.total_customers = 0

    def schedule_event(self, event):
        heapq.heappush(self.event_list, event)

    def generate_interarrival_time(self):
        return random.expovariate(self.arrival_rate)

    def generate_service_time(self):
        return random.expovariate(self.service_rate)

    def handle_arrival(self, event):
        # Schedule next arrival
        next_arrival_time = self.current_time + self.generate_interarrival_time()
        if next_arrival_time < self.simulation_time:
            self.schedule_event(Event(next_arrival_time, self.ARRIVAL))
        
        # Add customer to the queue
        self.total_customers += 1
        if self.server_busy:
            self.queue.append(event.time)
        else:
            # Start serving immediately
            self.server_busy = True
            service_time = self.generate_service_time()
            self.schedule_event(Event(self.current_time + service_time, self.DEPARTURE))

    def handle_departure(self, event):
        self.served_customers += 1
        if self.queue:
            # Serve the next customer
            arrival_time = self.queue.pop(0)
            self.total_wait_time += self.current_time - arrival_time
            service_time = self.generate_service_time()
            self.schedule_event(Event(self.current_time + service_time, self.DEPARTURE))
        else:
            self.server_busy = False

    def run(self):
        # Schedule the first arrival
        self.schedule_event(Event(0, self.ARRIVAL))

        while self.event_list:
            event = heapq.heappop(self.event_list)
            self.current_time = event.time

            if event.event_type == self.ARRIVAL:
                self.handle_arrival(event)
            elif event.event_type == self.DEPARTURE:
                self.handle_departure(event)

        self.print_statistics()

    def print_statistics(self):
        avg_wait_time = self.total_wait_time / self.served_customers if self.served_customers > 0 else 0
        print(f"Total customers served: {self.served_customers}")
        print(f"Average wait time: {avg_wait_time:.2f}")
        print(f"Total customers arrived: {self.total_customers}")


# Main execution
if __name__ == "__main__":
    simulation = DiscreteEventSimulation(arrival_rate=2, service_rate=1, simulation_time=10)
    simulation.run()
