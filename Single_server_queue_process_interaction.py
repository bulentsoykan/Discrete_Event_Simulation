import random
import simpy

class SingleServerQueue:
    def __init__(self, env, arrival_rate, service_rate):
        self.env = env
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate

        self.server = simpy.Resource(env, capacity=1)  # Single server
        self.total_customers = 0
        self.served_customers = 0
        self.total_wait_time = 0

    def generate_customers(self):
        while True:
            # Interarrival time
            yield self.env.timeout(random.expovariate(self.arrival_rate))
            self.total_customers += 1
            self.env.process(self.customer(self.total_customers))

    def customer(self, customer_id):
        arrival_time = self.env.now

        # Request the server
        with self.server.request() as request:
            yield request  # Wait until the server is available
            wait_time = self.env.now - arrival_time
            self.total_wait_time += wait_time

            # Service time
            service_time = random.expovariate(self.service_rate)
            yield self.env.timeout(service_time)
            self.served_customers += 1

def run_simulation(arrival_rate, service_rate, simulation_time):
    env = simpy.Environment()
    queue = SingleServerQueue(env, arrival_rate, service_rate)

    # Start the customer arrival process
    env.process(queue.generate_customers())

    # Run the simulation
    env.run(until=simulation_time)

    # Print statistics
    avg_wait_time = queue.total_wait_time / queue.served_customers if queue.served_customers > 0 else 0
    print(f"Total customers served: {queue.served_customers}")
    print(f"Average wait time: {avg_wait_time:.2f}")
    print(f"Total customers arrived: {queue.total_customers}")

# Main execution
if __name__ == "__main__":
    run_simulation(arrival_rate=2, service_rate=1, simulation_time=10)
