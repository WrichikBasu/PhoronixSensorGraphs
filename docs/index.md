## Welcome!

`PhoronixSensorGraphs` helps you to easily visualize the sensor readings recorded by the Phoronix Test Suite (PTS)
during a stress test.

PTS itself comes with a result viewer, that you can start from the terminal
using `phoronix-test-suite start-result-viewer`. There is, however, an issue with the viewer: all the data points from
the sensor are not plotted in the graphs.

This class reads the data recorded by PTS and plots it using `matplotlib`, making sure to include each and every data
point.

Hop on to Quickstart from the left panel. The repo also comes with a `main.py` file so that you can directly edit and
run it without much fuss.