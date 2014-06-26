import socket
import thread
import time

# Echo server program
'''
All Data sent over sockets are either byte strings or strings
The data requires a format of metadata pairs separated by ESC chars (0x1B):
EX:
b'type=message\1Busername=jondoe\1Btext=Hello World'
The packet is recovered using the digest function and parsing the reponse:
t[2:len(t)-1].replace(b'\'', '').split(', '):

# test client procedure
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 55555))
s.sendall(b'type=message\1Busername=brad\1Btext=Oh Hadddi')
data = s.recv(1024) #Should hang, so ^C
s.sendall(b'type=query')
data = s.recv(1024) #Should recieve conversation logs
s.close()
'''
class SimpleChatServer(object):
  def __init__(self, port=55555, DB = []):
    self.host = ''    # Symbolic name meaning all available interfaces
    self.port = port  # Arbitrary non-privileged port
    self.DB = DB
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def run(self):   #Blocking
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((self.host, self.port))
    self.sock.listen(1)
    while 1:
      conn, addr = self.sock.accept()
      thread.start_new_thread(self.spawn_conn_handler, (conn, self.DB))

  def start_recv_data(self, conn):
    rawdata = conn.recv(1024)
    return self.digest(rawdata)
      
  def digest(self, data):
    msg = {}
    parsed_fields = data.split(b'\1B')
    for field in parsed_fields:
      key = field.split('=')[0]
      val = field.split('=')[1]
      msg[key] = val
    return msg

  def start_send_data(self, conn, data):
    if(conn):
      conn.sendall(data)
  
  def spawn_conn_handler(self, conn, DB):
    while 1:
      msg = self.start_recv_data(conn)
      if(not msg):
        continue
      if(msg['type'] == 'message'):
        DB.append('[{}] {}: {}'.format(time.strftime("%H:%M:%S"), msg['username'], \
          msg['text']))
      elif(msg['type'] == 'query'):
        self.start_send_data(conn, str(DB))

  def kill(self):
    if(self.has_connection):
      self.conn.close()
