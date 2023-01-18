from PhoronixSensorGraphs import *

if __name__ == '__main__':
    # Sample usage:
    PhoronixSensorGraphs().plot_pts_sensor_data('8805d16735c38a019eec9b19',
                                                ('cpu.temp', 'gpu.temp', 'cpu.usage', 'gpu.usage', 'memory.usage', 'sys.temp'))
