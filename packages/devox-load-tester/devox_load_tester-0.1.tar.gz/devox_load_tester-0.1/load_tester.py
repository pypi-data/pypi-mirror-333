import socket
import threading
import time

class LoadTester:
    def __init__(self, target_url, num_threads=100):
        self.target_url = target_url
        self.domain = target_url.replace("https://", "").replace("http://", "").split('/')[0]
        self.num_threads = num_threads
        self.port = 80

        try:
            self.target_ip = socket.gethostbyname(self.domain)
            print(f"Resolved IP: {self.target_ip}")
        except socket.gaierror as e:
            print(f"Error resolving {self.domain}: {e}")
            exit()

    def send_request(self):
        """ Sends a simple GET request to measure response time. """
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((self.target_ip, self.port))

                http_request = f"GET / HTTP/1.1\r\nHost: {self.domain}\r\nUser-Agent: LoadTester/1.0\r\nConnection: close\r\n\r\n"
                s.sendall(http_request.encode('ascii'))

                start_time = time.time()
                response = s.recv(1024)
                end_time = time.time()

                response_time = end_time - start_time
                print(f"Response time: {response_time:.4f} seconds")

                s.close()

            except Exception as e:
                print(f"Error: {e}")

    def start_test(self):
        """ Launch multiple threads to test server performance. """
        print(f"Starting load test on {self.target_url} with {self.num_threads} threads.")
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.send_request)
            thread.daemon = True
            thread.start()

        time.sleep(60)  # Run test for 1 minute

