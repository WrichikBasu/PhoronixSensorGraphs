################################################################################
# Copyright (C) 2022  Wrichik Basu (basulabs.developer@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
################################################################################

import os
import platform
import pwd

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import xmltodict


class PhoronixSensorGraphs:
    r"""
    This class allows you plot the sensor data recorded by Phoronix Test Suite (PTS) during a
    stress run. Requires Python >= 3.10.

    Attributes
    ----------
    res_file : str
    res_path : str
    plt_layout : str | tuple
    """

    def __init__(self):

        self.__memo = {}

        self._res_path: str = "/home/" + pwd.getpwuid(
            os.getuid()).pw_name + "/.phoronix-test-suite/test-results/"

        self._res_file: str = "composite.xml"

        self._plt_layout: str | tuple = "auto"

        if platform.system() == 'Windows' or platform.system() == 'Darwin':
            print("CAUTION!")
            print("This program is designed to work on Linux. Please set the results directory and "
                  "file name if using in some other OS.")

    @property
    def res_path(self):
        """
        The path to the result directory.

        **Type:** `str`

        **Default:** `"/home/<user_name>/.phoronix-test-suite/test-results/"`

        You can set a custom result directory using

            psg.res_path = "/path/to/result/directory"

        The result directory must have the following structure:

            psg.res_path (i.e. the result directory)
             |
             +--- <Test_result_name>
                   |
                   +--- psg.res_file (i.e. the result file)

        The program will throw an error if this directory structure is violated.
        """
        return self._res_path

    @res_path.setter
    def res_path(self, value: str):
        self._res_path = value
        print("New results directory set.")

    @property
    def res_file(self):
        """
        The file name for the data file.

        **Type:** `str`

        **Default:** `"composite.xml"`

        File type must be `.xml`.

        You can set a custom file name for the data file using

            psg.res_file = "custom_filename.xml"


        """
        return self._res_file

    @res_file.setter
    def res_file(self, new_filename: str):

        if os.path.splitext(new_filename)[1] != ".xml":
            raise ValueError("File not of type `.xml`.")

        self._res_file = new_filename
        print("New result filename set.")

    @property
    def plt_layout(self):
        """
        The layout of the subplots.

        **Type:** `str` or `tuple`

        **Default:** `"auto"`

        Set a custom layout of the subplots using:

            psg.plt_layout = (nrows, ncols)


        where `nrows` is the number of rows, and `ncols` is the number of columns. Note that
        `nrows`*`ncols` MUST be >= no. of subplots expected. Without this, the program will throw an
        error. The default new_filename is "auto", which allows the program to automatically
        determine the best layout.


        """
        return self._plt_layout

    @plt_layout.setter
    def plt_layout(self, value: str | tuple):
        self._plt_layout = value
        print("New plot layout set.")

    def __dp(self, n, left) -> tuple:  # returns tuple (cost, [factors])
        """
        A function to get a specific no. of factors of a natural number.
        COURTESY: https://stackoverflow.com/a/28062998/8387076
        """

        if (n, left) in self.__memo:
            return self.__memo[(n, left)]

        if left == 1:
            return n, [n]

        i = 2
        best = n
        best_tuple = [n]
        while i * i <= n:
            if n % i == 0:
                rem = self.__dp(n / i, left - 1)
                if rem[0] + i < best:
                    best = rem[0] + i
                    best_tuple = [i] + rem[1]
            i += 1

        self.__memo[(n, left)] = (best, best_tuple)
        return self.__memo[(n, left)]

    def __is_prime(self, num) -> bool:
        for i in range(2, num):
            if num % i == 0:
                return False

        return True

    def plot_sensor_data(self, res_name: str, sensors: tuple, cpu_usage_summary_only: bool = True,
                         cpu_usage_separate_plots: bool = False):
        """
        Plots the sensor data recorded by Phoronix Test Suite.

        Does NOT support the sensors `cpu.freq`, `cpu.peak-freq` and `gpu.freq` as of now. See
        this issue: <a url="https://github.com/phoronix-test-suite/phoronix-test-suite/issues/680
        ">https://github.com/phoronix-test-suite/phoronix-test-suite/issues/680</a>

        Parameters
        ----------
        res_name : str
            The test result name.
        sensors : tuple
            The sensors to be potted; eg. `('cpu.temp', 'gpu.usage')`. Note that some sensors,
            like cpu.usage, have entries for each core as well as a summary. By
            default, only the summary is plotted. To plot data for each and every core,
            see `cpu_usage_summary_only` and `cpu_usage_separate_plots` parameters.
        cpu_usage_summary_only : bool, optional
            Used only if `sensors` contains `cpu.usage`. If `True`, only the CPU Usage Summary data
            will be plotted, otherwise per-CPU usage data will also be plotted.
        cpu_usage_separate_plots : bool, optional
            Used only if `cpu_usage_summary_only = True`. If set to `True`, CPU Usage data for
            each CPU core/thread will be plotted in separate sub-plots.
        """

        if platform.system() == 'Windows':
            file = self._res_path + res_name + "\\" + self._res_file
            if "/" in file:
                raise ValueError("File path not set properly on Windows.")
        else:
            file = self._res_path + res_name + "/" + self._res_file

        with open(file) as fd:
            doc = xmltodict.parse(fd.read())  # Read the xml file

        results = doc['PhoronixTestSuite']['Result']

        ##########################################################################
        # NO SUPPORT FOR `cpu.freq`, `cpu.peak-freq` and `gpu.freq` as of now.
        ##########################################################################
        if 'cpu.freq' in sensors:
            new_sensors = list(sensors)
            new_sensors.remove('cpu.freq')
            sensors = tuple(new_sensors)
            print("NO SUPPORT FOR `cpu.freq`. Please see documentation.")
        if 'cpu.peak-freq' in sensors:
            new_sensors = list(sensors)
            new_sensors.remove('cpu.peak-freq')
            sensors = tuple(new_sensors)
            print("NO SUPPORT FOR `cpu.peak-freq`. Please see documentation.")
        if 'gpu.freq' in sensors:
            new_sensors = list(sensors)
            new_sensors.remove('gpu.freq')
            sensors = tuple(new_sensors)
            print("NO SUPPORT FOR `gpu.freq`. Please see documentation.")

        def get_cpu_cores() -> int:
            """
            Count the number of CPU cores (actually threads).

            Returns
            -------
            int
                The number of CPUs.
            """

            hardware = doc['PhoronixTestSuite']['System']['Hardware']
            ind = hardware.find('/') + 2

            no_of_cpu = ""

            while hardware[ind] != ' ':
                no_of_cpu += hardware[ind]
                ind += 1

            return int(no_of_cpu)

        def count_plots() -> int:
            """
            Counts the number of plots.

            Returns
            -------
            int
                The number of subplots.
            """

            num = len(sensors)

            if 'cpu.usage' in sensors:
                if not cpu_usage_summary_only:
                    if cpu_usage_separate_plots:
                        num += get_cpu_cores()
                    else:
                        num += 1

            return num

        def get_plot_layout() -> tuple:
            """
            Compute the layout of the subplots.

            Returns
            -------
            tuple
                The layout of the subplots in the form (nrow, ncol).
            """

            num_plots: int = count_plots()

            if num_plots == 1:
                return 1, 1
            if num_plots == 2:
                return 2, 1
            elif num_plots == 3 or num_plots == 4:
                return 2, 2
            else:
                if self.__is_prime(num_plots):
                    num_plots += 1
                factors: tuple = self.__dp(num_plots, 2)[1]
                return factors[0], int(factors[1])

        # Set the layout:
        if self._plt_layout == "auto":
            plt_layout: tuple = get_plot_layout()
        else:
            if type(self._plt_layout) == tuple:
                plt_layout: tuple = self._plt_layout
            else:
                raise ValueError(
                    "Error in plt_layout: Should be a tuple, got some other type instead.")

        colour_list = sns.color_palette("viridis", n_colors=count_plots())

        count = 1
        i = 0

        def get_data(result):
            y_val = np.asarray(
                list(map(float, list(result['Data']['Entry'][-1]['Value'].split(",")))))
            x_val = np.asarray([10 * (j + 2) for j in range(len(y_val))])
            return y_val, x_val

        fig, axs = plt.subplots(plt_layout[0], plt_layout[1], sharex='all')

        while i < len(results):

            res = results[i]
            arg = res['Arguments']
            title = res['Title']

            # Skip sensors that are not in the list
            if arg not in sensors:
                i += 1
                continue

            if arg == 'cpu.usage':

                #######################################################################
                # If cpu_usage_summary_only = True and the current data is
                # not for the CPU usage summary, then continue to next iteration.
                #######################################################################
                if cpu_usage_summary_only and title != 'CPU Usage (Summary) Monitor':
                    i += 1
                    continue

                ###################################################################################
                # Here, cpu_usage_summary_only = False, which means we have to plot graphs for
                # each core/thread. We have to separately deal the case where we have to plot
                # all the cores on one plot.
                # If we are plotting each core on a separate plot, the normal plotting code will
                # do the work, and we skip this section.
                ###################################################################################
                if not cpu_usage_summary_only and not cpu_usage_separate_plots:

                    clrs = sns.color_palette('rocket_r', n_colors=get_cpu_cores() + 2)

                    plt.subplot(plt_layout[0], plt_layout[1], count)  # All cores on one subplot

                    cpu_count = 0

                    #############################################################################
                    # When we exit from this while loop, the `res` variable will have the data
                    # for the CPU Usage (Summary). This is based on the fact that Phoronix Test
                    # Suite places the summary data after listing the data for cores separately.
                    ##############################################################################

                    while title != 'CPU Usage (Summary) Monitor':
                        # Get data and plot for the current new_filename of `res`
                        data_y, data_x = get_data(res)
                        lab = "CPU" + str(cpu_count)

                        line = plt.plot(data_x, data_y, '.-', label=lab)
                        line[0].set_color(clrs[cpu_count])

                        # Initialise `res` to next new_filename in the `results` list
                        i += 1
                        cpu_count += 1
                        res = results[i]
                        title = res['Title']

                    plt.title("CPU per-core usage")
                    plt.gca().yaxis.grid(True)
                    plt.ylabel(res['Scale'])
                    plt.tick_params(axis='x', which='both', bottom=False, top=False,
                                    labelbottom=False)
                    plt.legend(loc="lower right", ncol=2)
                    count += 1

            data_y, data_x = get_data(res)

            plt.subplot(plt_layout[0], plt_layout[1], count)
            line = plt.plot(data_x, data_y, '.-')
            line[0].set_color(colour_list[count - 1])

            plt.title(title.replace(" Monitor", ""))

            # Remove ticks and labels from x-axis as they are arbitrary.
            # Courtesy: https://stackoverflow.com/a/12998531/8387076
            plt.tick_params(axis='x',  # changes apply to the x-axis
                            which='both',  # both major and minor ticks are affected
                            bottom=False,  # ticks along the bottom edge are off
                            top=False,  # ticks along the top edge are off
                            labelbottom=False)  # labels along the bottom edge are off

            # Switch on grid for the y-axis ONLY.
            # Adapted from: https://stackoverflow.com/a/25799781/8387076
            plt.gca().yaxis.grid(True)

            plt.ylabel(res['Scale'])
            count += 1
            i += 1

        plt.suptitle(doc['PhoronixTestSuite']['Generated']['Title'], fontweight='bold')

        # Delete subplot(s) which do not have any plot
        # Adapted from: https://stackoverflow.com/a/69886723/8387076
        try:  # Necessary because if we have to plot one parameter, axs.flat will throw an
            # exception.
            for ax in axs.flat:
                if not bool(ax.has_data()):
                    fig.delaxes(ax)  # delete if nothing is plotted in the ax object
        except TypeError:
            pass

        plt.tight_layout()

        # Ensure tight layout even when the window size is changed by handling window resize event.
        # Courtesy: https://stackoverflow.com/a/47838687/8387076
        def on_resize(_):
            fig.tight_layout()
            fig.canvas.draw()

        _ = fig.canvas.mpl_connect('resize_event', on_resize)

        plt.show()
