Command-line utilities
======================

To install the command-line utility ``afthermal``, ensure the ``[tools]``
option is active::

  $ pip install 'afthermal[tools]'

All commands support a multitude of options as command line arguments, see the
``--help`` option for each command for details.


Calibration
~~~~~~~~~~~

The printer should be calibrated each time it is connected to a different power
source, as it supports a wide variety of voltages. The ``calibrate`` command of
``afthermal`` can be used for this::

  $ afthermal calibrate
  Connecting to printer /dev/ttyAMA0
  About to calibrate your printer. [...]

Follow the instructions to determine optimum settings for printing.


Testing
~~~~~~~

To test if your printer is working correctly, the ``test`` command can be
used::

  $ afthermal test

This will print a few lines and a famous test image.


Printing images and QR-codes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To allow testing with your own settings/information, it is also possible to
print individual images and QR codes::

  $ afthermal print-qrcode 'Hello, Lena!'
  $ afthermal print-image some_image_on_your_harddrive.jpg
