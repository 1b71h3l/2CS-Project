import time
import threading
from flask import Flask, request, Response
from scapy.all import sniff
from scapy.layers.dns import DNS
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether

app = Flask(__name__)

dns_packets = []
dns_packets_lock = threading.Lock()
stop_event = threading.Event()  # Event to signal the program to stop
start_time = time.time()  # Start time for capturing packets
duration = 10  # Duration in seconds


# Capture the packets and filter only DNS ones
def capture_dns_packets():
    print("Capturing DNS packets...")
    # while time.time() - start_time < duration and not stop_event.is_set():
    while not stop_event.is_set():
        packet = sniff(filter="udp port 53", iface="eth0", count=1)
        if packet and DNS in packet[0]:
            dns_packet = packet[0][DNS]
            if dns_packet.qr == 0:  # Check if it's a query packet
                source_ip = packet[0][IP].src
                domain_name = dns_packet.qd.qname.decode('utf-8')
                with dns_packets_lock:
                    dns_packets.append((source_ip, domain_name))

@app.route('/receive_dns_packets')
def receive_dns_packets():
    def event_stream():
        while not stop_event.is_set():
            with dns_packets_lock:
                if dns_packets:
                    packet = dns_packets.pop(0)
                    source_ip, domain_name = packet
                    yield f"{source_ip}, {domain_name}\n\n"
            time.sleep(1)  # Adjust the sleep duration as per your needs
    return Response(event_stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    capture_thread = threading.Thread(target=capture_dns_packets)
    capture_thread.start()

    try:
        app.run(host='0.0.0.0', port="8082", threaded=True, debug=True)
    except KeyboardInterrupt:
        stop_event.set()
        print("Stopping the application...")

    capture_thread.join()  # Wait for the capture thread to finish

    print("Application stopped.")
