#!/usr/bin/env python
#######################################################################
# This file is part of Lyntin.
# copyright (c) Free Software Foundation 2001
#
# Lyntin is distributed under the GNU General Public License license.  See the
# file LICENSE for distribution details.
# $Id: connection.py,v 1.2 2005/01/07 14:50:40 glasssnake Exp $
#######################################################################
"""
This new test-server is a patchwork of stuff from the existing test server
and code I wrote for the Varium mud server way back when.  It is actually
a functional mini-mud now.
"""
import testserver, toolsutils
from toolsutils import color, wrap_text


class Connection:
    def __init__(self, world, newsock, newaddr=''):
        self._world = world
        self._sock = newsock
        self._sock.setblocking(0)  # non-blocking
        self._buffer = []
        self._addr = newaddr
        self._name = "spirit"
        self._desc = "A regular user."

        self._dir = [item for item in dir(self.__class__) if
                     item.startswith("handle_") and callable(getattr(self, item))]

    def __str__(self):
        return repr(self._addr)

    def killConn(self):
        """Shuts down the socket for the Connection object."""
        if not self._sock:
            return

        try:
            print(f"DEBUG: Closing down socket: {self._sock.fileno()} ")
            self._sock.shutdown(2)
            self._sock.close()
        except OSError as e:
            print(f"DEBUG: Error shutting down socket: {e}")

        self._sock = None
        if self in self._world._ms._conns:
            self._world._ms._conns.remove(self)  # Remove from connection list safely
        self._world.disconnect(self)

    def write(self, data):
        """
        Sends a string or byte data to the socket.
        """
        if not self._sock:
            return

        # Check if socket is already closed
        if self._sock.fileno() == -1:
            print("DEBUG: Checking is socket is closed before write()")
            self._sock = None  # Ensure cleanup
            return

        if not data:
            print("DEBUG: write() failed - Data is empty")
            return

        # Ensure data is bytes before sending
        if isinstance(data, str):
            data = data.replace("\n", "\r\n")  # Convert \n to \r\n for telnet/MUD clients
            data = data.encode('utf-8')

        try:
            self._sock.send(data)
        except (BrokenPipeError, ConnectionResetError):
            self._sock.close()
            self._sock = None
        except OSError as e:
            self._sock.close()
            self._sock = None
        except Exception as e:
            print(f"DEBUG: Unexpected error: {e}. Closing socket...")
            self._sock.close()
            self._sock = None

    def color(self, data, fc=37, bc=40, bold=0):
        """Formats text with ANSI escape codes."""
        escape = "\033"
        if bold == 1:
            return f"{escape}[1;{fc};{bc}m{data}{escape}[0m"
        else:
            return f"{escape}[{fc};{bc}m{data}{escape}[0m"

    def sockid(self):
        if self._sock:
            return self._sock    # Explicitly return None if the socket is invalid

    def handleNetworkData(self, new_data):
        for c in new_data:
            if c in (chr(8), chr(127)):
                if self._buffer:
                    self._buffer = self._buffer[:-1]
                continue
            elif c == "\n":
                self._world.enqueue(testserver.InputEvent(self, "".join(self._buffer)))
                self._buffer = []
                continue
            elif c in ("\r", chr(0)):
                pass
            else:
                self._buffer.append(c)

    def handleInput(self, world, input):
        comm = input.split(" ", 1)[0]

        # Look for the method in self
        method_name = "handle_" + comm
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(world, input)
        else:
            # Handle invalid command
            self.write(color("huh? '%s'\n" % input, 35))

        # Always display prompt
        self.write("> ")

    def handle_set(self, world, user_input):
        """ Lets you set things: (name, desc...)."""
        if " " in user_input:
            user_input = user_input.split(" ", 1)[1]
        if " " in user_input:
            name, value = user_input.split(" ", 1)

            if hasattr(self, '_%s' % name):
                self.write("Old value of %s is '%s'.\n" % (name, eval("self._%s" % name)))
            exec("self._%s = value" % name)
            self.write("Set to '%s'.\n" % value)
        else:
            self.write("Nothing to set.\n")

    def handle_say(self, world, user_input):
        """ Talk to your fellow mudders!"""
        if " " in user_input:
            text = user_input.split(" ", 1)[1]
            self.write(toolsutils.wrap_text("You say: %s" % text, 72, 5, 0) + "\n")
            world.spamroom(toolsutils.wrap_text("%s says: %s" % (self._name, text), 72, 5, 0) + "\n")
        else:
            self.write("say what?\n")

    def handle_look(self, world, user_input):
        """ Lets you look at things.  syntax: look <at thing>"""
        item = None
        if " " in user_input:
            item = user_input.split(" ", 1)[1].replace("at", "").strip().lower()

        self.write(world.look(self, item))

    def handle_quit(self, world, user_input):
        """ Quits out."""
        self.killConn()

    def handle_help(self, world, text):
        """ Prints out all the commands we understand."""
        commands = []
        for mem in self._dir:
            if mem.find("handle_") == 0:
                doc = ""
                try:
                    doc = eval("self.%s.__doc__" % mem)
                except:
                    pass

                if doc:
                    commands.append(mem[7:] + " - " + doc)
                else:
                    commands.append(mem[7:])

        self.write("\n".join(commands) + "\n")

    def handle_set_color(self, world, text):
        """ Sets the terminal text color to yellow. """
        try:
            # Write the yellow text
            self.write("\033[33m\nNow yellow.")  # \033[0m resets the color
        except Exception as e:
            # Handle exceptions and provide feedback
            self.write(f"Error setting color: {e}\n")

    def handle_colors(self, world, text):
        """ Prints out all the colors we know about. """
        try:
            response = []

            # Iterate through the range of background colors (40 to 47)
            for background in range(40, 48):
                # Iterate through the range of foreground colors (30 to 37)
                for foreground in range(30, 38):
                    # Add normal color
                    response.append(self.color(str(foreground), foreground, background))
                    # Add bold color
                    response.append(self.color(str(foreground), foreground, background, bold=1))

                # Reset colors and add a newline
                response.append("\033[0m\n")

            # Join all parts of the response and write it out
            self.write(''.join(response))

        except Exception as e:
            # Log error message if any issue occurs
            self.write(f"Error while handling colors: {e}")

    def handle_lyntin(self, world, text):
        """ Returns a paragraph, which coincidentally, is a description of Lyntin."""
        output = ("Lyntin is a mud client that is written in Python and uses " +
                  "Python as a scripting language. It strives to be functionally " +
                  "similar to TinTin++ while enhancing that functionality with " +
                  "the ability to call Python functions directly from the input " +
                  "line. It has the advantage of being platform-independent and " +
                  "has multiple interfaces as well--I use Lyntin at home with " +
                  "the Tk interface as well as over telnet using the text " +
                  "interface.\n")
        output = toolsutils.wrap_text(output, 70, 0, 0)
        self.write(output)

# Local variables:
# mode:python
# py-indent-offset:2
# tab-width:2
# End:
