.. Ship Strain Measurement System documentation master file, created by
   sphinx-quickstart on Sun Oct 11 06:24:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ship Strain Measurement System
==============================

The Ship Strain Measurement System (SSMS) is a command-line tool designed to perform strain measurement calculations
using computer vision and a range sensor, such as a LIDAR device.

SSMS uses OpenCV to find a target board in a frame and performs various filters and measurements to calculate the
difference in position. The difference in pixels :code:`Δ` is then multiplied by a calculated pixel-per-inch ratio to
determine the :code:`Δ` in millimeters which is the axial strain being exerted.

By utilizing the LIDAR sensor SSMS can also calculate the amount of compression or stretching that a ship is currently
undergoing. In conjunction with the computer vision this distance measurement allows the end user to measure four
degrees of axial strain.

.. toctree::
   :maxdepth: 3
   :caption: Introduction:

   newuser

.. toctree::
   :caption: Developing

   building

.. toctree::
   :caption: Modules:

   SSMS Module <ssms>

Index and search
==================

* :ref:`genindex`
* :ref:`search`
