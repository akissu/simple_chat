#!/usr/bin/python
import os
import sys
from simple_chat_module import SimpleChatServer as server

LOG_DB = []

def main(argv):
  if(len(argv) > 0): 
    if(argv[0] == '-?'):
      print 'usage: simple_chat_main [\"PORT\"]'
      sys.exit(0)
    if(isinstance(argv[0], int)):
      srv = server(port=argv[0], DB=LOG_DB)
  else:
    srv = server(DB=LOG_DB)
  srv.run()

if __name__ == "__main__":
  main(sys.argv[1:])
