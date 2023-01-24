# Quickstart

## Installation

**1.** Clone the repository:

```bash
# Get the latest tag (https://stackoverflow.com/a/67404585/8387076)
tag=$( curl --silent  "https://api.github.com/repos/WrichikBasu/PhoronixSensorGraphs/tags" | jq -r '.[0].name' )

# Clone the specific tag (https://stackoverflow.com/a/65397613/8387076)
git clone --depth 1 --branch $tag git@github.com:WrichikBasu/PhoronixSensorGraphs.git

cd PhoronixSensorGraphs/ 
```
    
**2.** Install/upgrade the libraries required:

```bash
python3 -m pip install --upgrade -r requirements.txt
```

## Usage

If you are on a Linux system, and have executed a stress test as a non-root user, you can quickly get the plots using:

```bash
>>> from PhoronixSensorGraphs import *
>>> psg = PhoronixSensorGraphs()
>>> psg.plot_sensor_data('Test_result_name', ('cpu.temp', 'gpu.temp', 'cpu.usage',  'gpu.usage', 'memory.usage', 'sys.temp'))
```

Don't forget to replace `Test_result_name` with the name of the stress test.