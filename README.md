# Phoronix Sensor Graphs

![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/WrichikBasu/PhoronixSensorGraphs/mkdocs_build_upload_ci.yml?branch=main&label=mkdocs%20build&style=plastic)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/WrichikBasu/PhoronixSensorGraphs/deploy_gh-pages.yml?branch=main&label=push%20to%20gh-pages&style=plastic)
![GitHub deployments](https://img.shields.io/github/deployments/WrichikBasu/PhoronixSensorGraphs/github-pages?label=deploy%20to%20Github%20Pages)

![GitHub last commit](https://img.shields.io/github/last-commit/WrichikBasu/PhoronixSensorGraphs)
![GitHub Release Date](https://img.shields.io/github/release-date/WrichikBasu/PhoronixSensorGraphs)

![GitHub](https://img.shields.io/github/license/WrichikBasu/PhoronixSensorGraphs?label=licence)

**PhoronixSensorGraphs** helps you to easily visualize the sensor readings recorded by the Phoronix Test Suite (PTS) during a stress test.

PTS itself comes with a result viewer, that you can start from the terminal using `phoronix-test-suite start-result-viewer`. There is, however, an [issue](https://github.com/phoronix-test-suite/phoronix-test-suite/issues/509) with the viewer: all the data points from the sensor are not plotted in the graphs.

This class reads the data recorded by PTS and plots it using matplotlib, making sure to include each and every data point.

## Quickstart

See here: https://wrichikbasu.github.io/PhoronixSensorGraphs/quick_usage_guide/

The repo also comes with a `main.py` file so that you can directly edit and run it without much fuss.

## Documentation

See here: https://wrichikbasu.github.io/PhoronixSensorGraphs/documentation/

