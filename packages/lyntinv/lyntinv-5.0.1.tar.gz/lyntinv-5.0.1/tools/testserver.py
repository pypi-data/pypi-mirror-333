#!/usr/bin/env python
#######################################################################
# This file is part of Lyntin.
# copyright (c) Free Software Foundation 2001
#
# Lyntin is distributed under the GNU General Public License license.  See the
# file LICENSE for distribution details.
# $Id: testserver.py,v 1.2 2005/01/07 14:50:40 glasssnake Exp $
#######################################################################
"""
This new test-server is a patchwork of stuff from the existing test server
and code I wrote for the Varium mud server way back when.  It is actually
a functional mini-mud now.
"""
import socket, sys, queue, select, textwrap

import connection

my_world = None

class Event:
  def __init__(self):
    pass

  def execute(self, world):
    pass

  def __str__(self):
    return ""

class InputEvent(Event):
  def __init__(self, conn, input):
    super().__init__()
    self._conn = conn
    self._input = input

  def __str__(self):
    return f'"{self._input}" for "{self._conn}"'

  def execute(self, world):
    self._conn.handleInput(world, self._input)

class HeartbeatEvent(Event):
  def __init__(self, source):
    super().__init__()
    self._source = source

  def execute(self, world):
    self._source.heartbeat(world)

class NPC:
  def __init__(self, world):
    self._world = world
    self._name = "Joe"
    self._desc = "A regular looking NPC."

    from random import Random
    self._random = Random()

  def blab(self):
    self._world.spamroom(self._name + " looks fidgety.\n")

class Neil(NPC):
  def __init__(self, world):
    NPC.__init__(self, world)
    self._name = "Neil"
    self._desc = "Neil is the bartender at this little mini-tavern."

  def heartbeat(self, world=None):
    g = (self._random.random() * 10)
    if (g < 2):
      self._world.spamroom(self._name + " flicks a bug off his bar.\n")
    elif (g < 4):
      self._world.spamroom(self._name + " scrubs some glasses with his dishrag.\n")
    elif (g < 5):
      self._world.spamroom(self._name + " says, \"Mighty fine morning, isn't it?\"\n")

class World:
  def __init__(self, options):
    self._event_queue = queue.Queue(0)
    self._worker = None
    self._options = options
    self._ms = None

    temp = ("Welcome to Neil's Pub--a small tavern of unusual candor.  " +
            "In many ways, this is a dream come true for Neil and it shows " +
            "in the care he gives to the place.  The tavern is both " +
            "infinitely large and terribly small.  There are no exits.  " +
            "Only a long bar and a series of barstools for folks to show " +
            "up, take a load off, and socialize.")

    self._desc = textwrap.fill(temp, width=70)

    self._npcs = []

    self._npcs.append(Neil(self))

  def enqueue(self, ev):
    self._event_queue.put(ev)

  def startup(self):
    from threading import current_thread
    self._worker = current_thread()

    # launch the server
    self._ms = MasterServer(self, self._options)
    self._ms.startup()

    do_heartbeat = self._options.get("heartbeat")
    beat = 0

    # this is our main loop thingy!
    while True:
      if do_heartbeat == "yes":
        beat += 1
        if beat % 30 == 0:
          beat = 0
          self.heartbeat()

      self._ms.networkLoop()

      # Handle events
      try:
        event = self._event_queue.get(block=False)
        es = str(event)
        event.execute(self)
      except queue.Empty:
        pass  # No events to process
      except Exception as e:
        print(f"Exception while executing event: {e}")

  def heartbeat(self):
    """Triggers NPC heartbeats when players are connected."""
    if self._ms and hasattr(self._ms, "_conns") and len(self._ms._conns) > 1:
      for npc in self._npcs:
        self.enqueue(HeartbeatEvent(npc))

  def disconnect(self, conn):
    """Handles player disconnection."""
    print("DEBUG: 'disconnect' function has been called.")
    if self._ms and hasattr(self._ms, "_conns") and conn in self._ms._conns:
      print(f"About to close and remove: {self._ms._conns(conn)}")
      self._ms._conns.remove(conn)
      self._ms._conns.close()

    if hasattr(conn, '_name'):
      self.spamroom(f"{conn._name} has left the game.\n")

    print(f"Goodbye {getattr(conn, '_name', 'Unknown Player')}")

  def look(self, conn, item):
    if item:
      for mem in self._npcs:
        if item == mem._name.lower():
          return mem._desc + "\n"

      for mem in self._ms._conns:
        if item == mem._name.lower():
          return mem._desc + "\n"

    else:
      out = self._desc + "\n\n"

      # Convert the map object to a list
      names = [x._name for x in self._ms._conns]

      # Append additional names from self._npcs
      names.extend(mem._name for mem in self._npcs)

      # Join the names with ', ' as a separator
      out += textwrap.fill(', '.join(names), 70)

      out += "\n"

      return out

    return "That does not exist.\n"

  def spamroom(self, data):
    for mem in self._ms._conns:
      try:
        if hasattr(mem, 'write'):
          mem.write(data) #connection still alive here.
        else:
          print(f"Skipping invalid connection: {mem}")
      except Exception as e:
        print(f"Error writing to {mem}: {e}")

  def shutdown(self):
    if self._ms:
      self._ms.closedown()
    print("Shutting down.")

class MasterServer:
  def __init__(self, world, options):
    super().__init__()
    self._args = args
    self._master = None
    self._conns = []
    self._shutdown = 0
    self._options = options
    self._world = world

  def startup(self):
    host = self._options["host"]
    port = int(self._options["port"])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    print(f"Socket bound to {host}:{port}")
    s.listen(5)
    print("Socket is listening for incoming connections...")

    print(f"Test server starting up: {host}:{port}")
    self._master = connection.Connection(self._world, s, "MASTER")
    self._master._name = "Igor"
    self._master._desc = "A very busy old man."

    self._conns = []
    self._conns.append(self._master)

  def networkLoop(self):
    # Prepare the list of socket objects from the connections
    #fns = [conn.sockid() for conn in self._conns]  # Use list comprehension instead of map
    fns = [conn.sockid() for conn in self._conns if conn.sockid() and hasattr(conn.sockid(), "fileno")]
    #print("DEBUG: fns =", fns)  # Should only contain socket objects!

    fi = select.select(fns, [], [], 0.1)[0]  # Get the readable sockets
    allconns = [conn for conn in self._conns if conn.sockid() in fi]  # Use list comprehension instead of filter

    for conn in allconns:
      if conn._addr == "MASTER":
        # Accept a new connection
        try:
          newsock, newaddr = conn._sock.accept()
          newconn = connection.Connection(self._world, newsock, newaddr)
          newconn.write("Welcome to Neil's Pub! Type \"help\" if you're lost.\n")
          self._conns.append(newconn)
        except Exception as e:
          print(f"Error accepting new connection: {e}")

      else:
        # Handle existing connections
        try:
          new_data = conn._sock.recv(1024)
          if new_data:
            new_data = new_data.decode('utf-8')
        except Exception as e:
          print(f"Exception: {e}")
          if conn in self._conns:
            self._conns.remove(conn)
          if conn._sock:  # Only call killConn() if the socket still exists
            conn.killConn()
          continue

        if new_data:
          conn.handleNetworkData(new_data)
        else:
          if conn in self._conns:
            #self._conns.remove(conn)
            conn.killConn()

  def closedown(self):
    print("DEBUG: Closing the socket.")
    #try:
      #if self._master.sockid() != -1:
          #self._master._sock.close()
    #except Exception as e:
      #print(f"Closing down master socket failed: '{e}'")

    for mem in self._conns[:]:  # Iterate over a copy of the list
      try:
        if mem._addr != "MASTER":
          mem.write("Server shutting down.\n")
        mem.killConn()
      except Exception as e:
        print(f"Error closing connection for {mem._addr}: {e}")

def print_syntax(message=""):
  print("testserver.py [--help] [options]")
  print("    -h|--host <hostname> - sets the hostname to bind to")
  print("    -p|--port <port>     - sets the port to bind to")
  print("    --heartbeat <yes|no> - sets whether or not to execute heartbeats")
  print()
  if message:
    print(message)

if __name__ == '__main__':
  import testserver, signal, traceback, logging

  # parse out arguments
  args = sys.argv[1:]
  i = 0
  optlist = []
  while (i < len(args)):

    if args[i][0] == "-":
      if (i+1 < len(args)):
        if args[i+1][0] != "-":
          optlist.append((args[i], args[i+1]))
          i = i + 1
        else:
          optlist.append((args[i], ""))
      else:
        optlist.append((args[i], ""))

    else:
      optlist.append(("", args[i]))

    i = i + 1

  options = {"host": "localhost", "port": "3000", "heartbeat":"yes"}
  print("Handling arguments.")
  for mem in optlist:
    if mem[0] == "--host" or mem[0] == "-h":
      if mem[1]:
        options["host"] = mem[1]
      else:
        print_syntax("error: Host was not specified.")
        sys.exit(1)

    elif mem[0] == "--help":
      print_syntax()
      sys.exit(1)

    elif mem[0] == "--port" or mem[0] == "-p":
      if mem[1] and mem[1].isdigit():
        options["port"] = mem[1]
      else:
        print_syntax("error: Port needs to be a number.")
        sys.exit(1)

    elif mem[0] == "--heartbeat":
      if mem[1].lower() == "yes" or mem[1].lower() == "no":
        options["heartbeat"] = mem[1].lower()
      else:
        print_syntax("error: Valid heartbeat settings are 'yes' or 'no'.")
        sys.exit(1)

  print(f"Host: {options['host']}")
  print(f"Port: { options['port']}")

  # Setup logging
  logging.basicConfig(level=logging.ERROR, filename="server_error.log", filemode="a",
                      format="%(asctime)s - %(levelname)s - %(message)s")

  # Create the world
  testserver.my_world = World(options)

  try:
    testserver.my_world.startup()
  except KeyboardInterrupt:
    print("Server interrupted by user. Shutting down...")
  except ValueError as ve:
    print(f"ValueError: {ve}")
    logging.error("ValueError occurred", exc_info=True)
  except OSError as oe:
    print(f"OS error: {oe}")
    logging.error("OS error occurred", exc_info=True)
  except Exception as e:
    print(f"Outer loop exception: {e}")
    logging.error("Unhandled exception", exc_info=True)
    traceback.print_exc()  # Print full stack trace to console
  finally:
    testserver.my_world.shutdown()
    print("Server shut down gracefully.")

# Local variables:
# mode:python
# py-indent-offset:2
# tab-width:2
# End:
