import socket

class SmartphoneSensor:
    def __init__(self, ip="0.0.0.0", port=2055):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind((self.ip, self.port))
            self.sock.setblocking(False) 
            print(f"📡 Sensor UDP ouvindo em {self.ip}:{self.port}")
        except Exception as e:
            print(f"❌ Erro ao configurar socket: {e}")

    def receive_data(self):
        try:
            data, addr = self.sock.recvfrom(1024)
            message_list = data.decode('utf-8').strip().split(',')
            return message_list, addr
        
        except BlockingIOError:
            return None, None
        except Exception as e:
            print(f"⚠️ Erro na recepção: {e}")
            return None, None

    def close(self):
        self.sock.close()