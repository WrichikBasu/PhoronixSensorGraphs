from PhoronixSensorGraphs import PhoronixSensorGraphs

if __name__ == '__main__':
    # Sample usage:
    psg = PhoronixSensorGraphs()
    psg.plot_sensor_data('8805d16735c38a019eec9b19',
                         ('cpu.temp', 'gpu.temp', 'cpu.usage', 'gpu.usage', 'memory.usage', 'sys.temp'))
