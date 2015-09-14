afthermal
=========

.. note:: afthermal is currently in alpha status. This is a snapshot release of
          the development branch. While it is used productively, some features
          may be unfinished or undocumented.

``afthermal`` is a driver/library for the popular `Adafruit
<https://www.adafruit.com/products/597>`_ (originally Cashino
A2) thermal printer [1]_.

Partially, it is inspired by previous efforts:

* https://github.com/adafruit/Adafruit-Thermal-Printer-Library
* https://github.com/adafruit/Python-Thermal-Printer/
* https://github.com/luopio/py-thermal-printer/

``afthermal`` try to be more pythonic and efficient than previous efforts,
which have mostly been 1:1 ports from other languages.
Additionally it is not focused on education but rather on being a
reliable library for handling this kind of hardware.

Features include:

* Comfortable handling of text formatting
* Adapters to print images from PIL_ / Pillow_ as well as OpenCV_
* A fast Floyd-Steinberg_ implementation to dither OpenCV_ images.
* Command-line utilities for calibrating the printer for optimum speed and
  quality, as well as other capabilities
* Support for printing QR codes via PyQRCode_ without having to render them
  into images first

.. [1] Specification is available at http://www.adafruit.com/datasheets/CSN-A2%20User%20Manual.pdf

.. _PyQRCode: https://pypi.python.org/pypi/PyQRCode
.. _OpenCV: https://opencv-python-tutroals.readthedocs.org
.. _Pillow: http://pillow.readthedocs.org
.. _PIL: http://www.pythonware.com/products/pil/
.. _Floyd-Steinberg: https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering


Installation
------------

``afthermal`` is installable from ``pip``. It supports an extra feature named
``tools``, installing it will include cli tools for calibrating the
printer, printing test images or other tasks:

.. code-block:: sh

   $ pip install 'afthermal[tools]'

It includes a C extension for Floyd-Steinberg_ dithering, since OpenCV_ does
not ship with a dithering function. For this reason C-modules must be
compileable when installing ``afthermal``.


Full docs
---------

The complete documentation is housed at http://pythonhosted.org/afthermal.
