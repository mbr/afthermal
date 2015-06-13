Hardware
========

``afthermal`` currently supports only one piece of hardware: Cashino A2 thermal
printer, also sold by `Adafruit <https://www.adafruit.com/products/597>`_.
Specifically, it deals with the serial port version of the printer.


Raspberry Pi
~~~~~~~~~~~~

One way of using the printer is connecting it to a `Raspberry Pi
<https://www.raspberrypi.org/>`_. While this is in no means required as any
serial connection will work, since it is a popular way to setting things up,
here is a short how-to:

1. Connect the RX wire on the printer to pin 8 on the Raspberry Pi
   (GPIO14/UART0_TXD)
2. Connect the TX wire on the printer to pin 10 on the Raspberry Pi
   (GPIO15/UART0_RXD).
3. Connect the printer to a 5-9 V or a 12V power source.
4. Make sure there is no serial console enabled (via ``/boot/cmdline.txt``) on
   ``/dev/ttyAMA0``.

If everything is connected correctly, the serial port should be accessible as
``/dev/ttyAMA0``.
