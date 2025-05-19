import time
import  psutil
from datetime import datetime

def get_network_packets():
    net_io = psutil.net_io_counters()
    packets_sent = net_io.packets_sent
    packets_recv = net_io.packets_recv
    return {
        "packet_sent": packets_sent/10000000,
        "packet_recv": packets_recv/10000000
    }

def getNetSpeed(interval):
    # Đo thông tin ban đầu (số byte đã truyền và nhận)
    net_io_1 = psutil.net_io_counters()
    bytes_sent_1 = net_io_1.bytes_sent
    bytes_recv_1 = net_io_1.bytes_recv

    # Đợi trong khoảng thời gian xác định
    time.sleep(interval)

    # Đo lại thông tin sau khoảng thời gian đã đợi
    net_io_2 = psutil.net_io_counters()
    bytes_sent_2 = net_io_2.bytes_sent
    bytes_recv_2 = net_io_2.bytes_recv

    # Tính lưu lượng mạng đã sử dụng
    sent_speed = (bytes_sent_2 - bytes_sent_1) / interval / 1024  # KB/s
    recv_speed = (bytes_recv_2 - bytes_recv_1) / interval / 1024  # KB/s
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #print(f"Tốc độ tải lên (Upload): {sent_speed:.2f} KB/s")
    #print(f"Tốc độ tải xuống (Download): {recv_speed:.2f} KB/s")

    # Đo lưu lượng mạng liên tục

    #print("Đang theo dõi lưu lượng mạng. Nhấn Ctrl+C để dừng.")

    return {
        "timestamp": timestamp,
        "sent_speed": sent_speed,
        "recv_speed": recv_speed
    }