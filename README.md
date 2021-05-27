# ROS Parameter Server GUI

Edit ROS Parameters live using an interactive GUI (no more repetitive commands in terminal!)

## Dependencies

This package is tested on Python 2.7.17

First, install `tkinter`:

    pip install tk

Then, clone this package:

    git clone https://github.com/aaronzberger/ROS_Param_GUI

To execute:

    python src/main.py *[NAMESPACES]*

Replace *`[NAMESPACES]`* with any number of namespaces of the ROS Params you want to change.

To get a list of your current ROS params, use:

    rosparam list