from PhoronixSensorGraphs import PhoronixSensorGraphs

if __name__ == '__main__':
    # Create an instance of the class:
    psg = PhoronixSensorGraphs()

    # Optionally set the path of results directory:
    # psg.res_path = "/path/to/results/directory"

    # Optionally set the name of the result .xml file:
    # psg.res_file = "composite.xml"

    # Optionally set the layout of the subplots:
    # psg.plt_layout = "auto"

    # Call the function:
    psg.plot_sensor_data('Test_result_name', ('cpu.temp', 'gpu.temp', 'cpu.usage', 'gpu.usage',
                                              'memory.usage', 'sys.temp'))
