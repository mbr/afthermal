Command-line utilities
======================

To install the command-line utility ``afthermal``, ensure the ``[tools]`` option is active::

  $ pip install 'afthermal[tools]'


Calibration
~~~~~~~~~~~

The printer should be calibrated each time it is connected to a different power source, as it supports a wide variety of voltages. The ``calibrate`` command of ``afthermal`` can be used for this::

  $ afthermal calibrate
  Connecting to printer /dev/ttyAMA0
  About to calibrate your printer. [...]

Follow the instructions to determine optimum settings for printing.