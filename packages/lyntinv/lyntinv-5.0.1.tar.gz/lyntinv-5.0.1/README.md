# Lyntin V

***
## Name
Lyntin V

## Description
Why Lyntin V
==========

Lyntin V is a "hard fork," and/or "rebranding" of Lyntin. A
great project, that has been abandoned for 15 or so years. But,
I have now decided to take over, update, and further maintain it.
The last major release was Lyntin 4.2, and since the code base
has been updated from python 2.7 to python 3+, I have changed
the name to Lyntin 5.0, or simply "Lyntin V."

Lyntin V is written entirely in Python--a nicely written and very 
portable programming language.  Thusly, Lyntin V is platform 
independent.  Lyntin V exposes the Python interpreter allowing 
more freedom than mere 'if you see this then send this' aliases 
and triggers.

This can include Python functions which do anything 
from setting a variable to forking a web spider.  In addition, 
your code can interface with Lyntin V's code.  

Lyntin V is great if:

1. you want a mud client that you can see the source code to
   and adjust it to suit your needs
2. you want a mud client that has a sophisticated API for 
   enhancing and building bots/agents/triggers more advanced than
   "if you see this then do this"
3. you want a mud client that works on all your machines,
   has a text ui, a tk gui, and can also work over ssh/telnet

Lyntin V is not great if:

1. you prefer wizards and menus to the command line
2. you hate Python
3. you want fancy bells and whistles in the ui

Operating System Notes
======================

Lyntin V works in most environments we can think of, but it has some
caveats with the various operating systems due to differences 
between them.

Windows
-------

Windows users should use either ``\`` or ``/`` to denote directory 
separaters.

Examples::

   #write c:\commandfile
   #write c:/commandfile


RedHat Linux
------------

Depending on which version of RedHat Linux you have, you will have 
to install the Python RPM as well as the Python Tkinter RPM.  If 
you don't install the Tkinter RPM, then you won't be able to use 
the Tk ui and it'll complain that it's missing a library when you 
try.


Mac OSX
-------

Lyntin V works perfectly fine on MacOS X. Python already comes 
installed, so no additional steps are required.


Other Notes
-----------

If you encounter other operating system issues, let us know both 
the problem and the solution so we can add them here.

Getting Started
===============

Type ``#help help`` for help on how to use the in-game help system.

Read through the ``#help readme`` topics.  These will help as they 
will walk you through how Lyntin works, how to get additional 
help, where to go for answers, and what to do if you find a bug.  
These are also exported into the ``README`` file.

You should read through the topics in ``#help commands`` for all 
the currently registered Lyntin commands.

Each user interface has its own help topic--these will be on the 
top level of the help structure.

To start, the ``#session`` command will allow you to start a 
session.  When you're done, ``#end`` will close Lyntin.

All documentation that comes with Lyntin is also available on the
Lyntin web-site.  If you find problems with the documentation or
have fixes for it, let us know on the lyntin-devl mailing list.

Lyntin V Command Handling
=======================

Lyntin V uses Lyntin commands to allow you to manipulate the Lyntin 
client and setup your session with aliases, variables, actions, 
and such.  Commands start with the command character--by default 
this is ``#``.  It can be changed with the ``#config`` command.  The 
command character can also do some other special things:

1. You can execute commands in another session by typing the 
   command character and then the sesion name then the command.
   Example::

      #3k say hello       - will say hello in session 3k
      #a #info            - will run the #info command in session a

2. You can switch to another session by typing the command 
   character and then the session name.  Examples::

      #a                  - will switch to session a (if it exists)
      #3k                 - will switch to session 3k (if it exists)

3. You can execute a command in all sessions by typing the 
   command character then all.  Examples::

      #all say hello      - will run "say hello" in all sessions

4. You can execute a command a number of times by typing the 
   command character then a number, then the command.  Examples::

      #5 say hello        - will run "say hello" 5 times
      

Commands are separated by the semicolon.  Semicolons can be 
escaped with the ``\`` character.  Examples::

   say hello;wave         - will run "say hello" then "wave"
   say hi!  \;)           - will run "say hi!  ;)"


Command arguments can be enclosed with ``{`` ``}``.  This enables you to 
specify arguments that have spaces in them.  Examples::

   #alias a b             - executes #alias with args "a" and "b"
   #alias {a} {b}         - executes #alias with args "a" and "b"
   #alias {a} {say hi}    - executes #alias with args "a" and "say hi"
   #alias a say hi        - executes #alias with args "a", "say", 
                            and "hi" which will kick up an error
                            (since the #alias command doesn't accept
                            a third string argument)


``{``, ``}`` and ``\`` can all be escaped with the ``\`` character: 
``\{``, ``\}``, and ``\``.


Variable Evaluation
===================

Variables get evaluated according to a new methodology we developed
after disliking the Tintin way of doing things.  This new methodology
provides maximum flexibility and provides for some things that
the Tintin variable evaluation did not provide for.

* Variables and placement variables with a single ``$`` or ``%`` are
  evaluated/expanded.  One layer of ``$``s or ``%``s is then stripped 
  off when this evaluation occurs.

* Variables are matched by length of name.  So if you have two
  variables ``a`` and ``ab``, we'll test to see if the variable is
  ``ab`` before ``a``.  We also handle bracing of variable names
  like ``${a}`` and ``${ab}`` which will guarantee unambiguosity.

* Variable expansion is always done on user input before 
  commands are evaluted.  This means variables can be used as 
  arguments to any commands, etc.  It also means that if you
  want the variable actually in the command, you have to prepend
  another ``$``.

* Variable expansion happens again when certain expressions are
  evaluated, such as action triggers, alias expansion, etc.
  Essentially, when any stored value gets expanded its variables
  will get expanded (typically whenever tintinmode would do its 
  sole expansion.) 

* Placement vars in actions and aliases support an expanded 
  syntax based on python array slices.  ``%0:1`` will evaluate to 
  the first and second arguments, while ``%0:`` will be all 
  arguments, and ``%:-1`` will be all but the last argument, etc.

Examples:

1. ``#action {$Myvar} {woo}``

Will trigger whenever the value ``Myvar`` holds when this is entered 
(the original value of ``Myvar`` - it will not change if ``Myvar``'s 
value changes)

2. ``#action {$$Myvar} {woo}``

Will trigger whenever the current value of ``Myvar`` passes by.

3. ``#action {$$$Myvar} {woo}``

Will trigger whenever the literal string ``$Myvar`` is seen.  Place 
more ``$``s in if you wish to trigger on more of them, the first 2 
will be stripped by the variable expansion processes. 

4. ``#alias {hello} {$moo}``

Will bind ``hello`` to ``$moo``'s current value.

5. ``#alias {hello} {$$moo}``

Will bind ``hello`` to always expand to ``moo``'s current value at 
the time of expansion.

6. ``#alias {hello} {$$$moo}``

Will bind ``hello`` to expand to the literal string ``$moo``

7. ``#alias {hello} {$${moo}}``

Will bind ``hello`` to expand to ``moo``'s current value at the time of
expansion.

Lyntin V's Regular Expression Syntax
==================================

Lyntin V allows the use of regular expressions in various arguments
for commands like ``#action``, ``#highlight``, and such.  It uses a 
specific format to trigger using raw regular expressions rather 
than having your argument get escaped so it can be compiled into 
a regular expression.  This allows you to write arguments using 
the simplest form that you can without having to adjust toggles 
and such.

For example::

   #highlight {red} {*says:}

is the same as::

   #highlight {red} {r[^.*?says:]}


The first one will undergo escaping and get transformed into 
``^.*?says\:`` (without the quotes) before being compiled into a
regular expression.

The second one gets compiled without being escaped.

If you want to pass an "ignorecase" flag, do so after the end
``]``::

   #highlight {red} {r[krynor]i}

will highlight all instances of ``krynor`` (ignoring case) as red.

For regular expression documentation, refer to the Python 
documentation at http://www.python.org/doc/current/lib/re-syntax.html .

Note: It may have moved since this was written.



Bug Reports, Questions, Comments, Curses?
=========================================

Lyntin was originally written by Lyn Headley.  Lyntin was then maintained
by Will Guaraldi (willhelm@users.sourceforge.net) from 1.3.2 to 4.0, and 
by Eugene up to 4.2? Not entirely sure the work done between 4.0 and 4.2,
and who did it.

All ported from python 2.7 to 3.0, was done by me, Drexl Spivey 
(drexl@little-beak.com).

We appreciate ALL types of feedback.

Inevitably you will either run across a bug in Lyntin or the need 
for a feature to be implemented.  When this happens, we ask you 
to provide as much information as you can:

* operating system, version of Python and version of Lyntin
  (from ``#diagnostics``)
* stacktrace (if it's a bug and kicked up a stacktrace)
* explanation of what happened vs. what should be happening
* any other pertinent information

Enter this in the bugs forum or send it to the mailing list.  Details for 
both are on the Lyntin web-site:
https://gitlab.little-beak.com/drexl/portlyntintopython3.



How To Contribute
=================

Development and maintenance is entirely managed by the maintainer 
right now.  If you're interested in sending in bug fixes, please 
feel welcome.  I'm extremely accomodating to most methods of 
sending in patches, however a ``diff -u`` against the code in cvs is
great for this sort of thing.

All patches and such things should be sent to the mailing list at
lyntin-devl@lists.sourceforge.net/ .

NOTE: Patches will not be applied unless the author either yields 
the copyright to the FSF or to me (and then I'll yield it to the 
FSF).

Please read through the web-site areas on coding conventions and 
such before sending in code.

## Authors and acknowledgment
I have forked this project from two previous engineers I never really met,
and only talked to briefly--if at all. So, full credit for any greatest
should go to Eugene and Will. Of course, all errors are my own.

Drexl Spivey has ported the entire code base from Python 2 to 3, in some
cases changing areas of code to make it compliant with Python 3+.

## License
GNU GPLv3


## Project status
======

The latest release of Lyntin is always available from
https://gitlab.little-beak.com/drexl/portlyntintopython3. Or, 
downloadable from PiPy (pip).

When communicating bugs or feature requests INCLUDE AS MUCH 
INFORMATION AS POSSIBLE.  If you don't, I'll just ask you for
it anyhow.

In-game help is accessed by typing ``#help``.  When you start 
Lyntin for the first time, type ``#help general`` and that'll 
get you started.  Read through the various help files at your 
leisure.



Enjoy!

the Lyntin V development team - me. =)

The project is in active development and debugging. It's currently in BETA
status. I have not had a chance to fine comb and test for bugs.