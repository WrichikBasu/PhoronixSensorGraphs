import os
import pwd
import matplotlib.pyplot as plt
import xmltodict
import numpy as np

memo = {}


def __dp__(n, left):  # returns tuple (cost, [factors])
    """
    A function to get a specific no. of factors of a natural number.
    COURTESY: https://stackoverflow.com/a/28062998/8387076

    Parameters
    ----------
    n : int
        The number whose factors are to be found out.
    left : int
        The number of factors needed.

    Returns
    -------
    tuple : (cost, [factors])
        [factors] is the list of factors of the number `left`.
    """
    if (n, left) in memo:
        return memo[(n, left)]

    if left == 1:
        return n, [n]

    i = 2
    best = n
    best_tuple = [n]
    while i * i <= n:
        if n % i == 0:
            rem = __dp__(n / i, left - 1)
            if rem[0] + i < best:
                best = rem[0] + i
                best_tuple = [i] + rem[1]
        i += 1

    memo[(n, left)] = (best, best_tuple)
    return memo[(n, left)]


def plot_phoronix_result(res_name, sensors, plt_layout,
                         res_path="/home/" + pwd.getpwuid(os.getuid()).pw_name + "/.phoronix-test-suite/test-results/",
                         res_file="composite.xml", cpu_usage_summary_only=True, cpu_usage_separate_plots=False):
    """
    A function to plot the results created by Phoronix Test Suite.

    Parameters
    ----------
    res_name : str
        The test result name.
    sensors : tuple
        The sensors to be potted; eg. (cpu.temp, gpu.usage). Note that some sensors, like cpu.usage and cpu.freq,
        have entries for each core as well as a summary. By default, only the summary graph is plotted. To plot
        data for each and every core, see `cpu_usage_summary_only` and `cpu_usage_separate_plots` parameters
        for sensor cpu.usage.
    plt_layout : tuple
        The layout of the subplots. The tuple should be of the form (nrows, ncols), which means that there will be
        'nrows' number of rows and 'ncols' number of columns in the subplot. The value (nrows * ncols) should always
        be the smallest composite number >= the number of plots you expect. For example, if you expect 5 plots, then
        'plt_layout' can be (2, 3) or (3, 2) but NOT (2, 2).
    res_path : str, optional
        The path to the directory of the result file.
    res_file : str, optional
        The name of the result file.
    cpu_usage_summary_only : boolean, optional
        Used only if plt_args contains 'cpu.usage'. If true, only the CPU Usage Summary data will be plotted, otherwise
        per-CPU usage data will also be plotted.
    cpu_usage_separate_plots : boolean, optional
        Used only if cpu_usage_summary_only = True. If true, CPU Usage data for each CPU core/thread will be plotted in
        separate graphs.
    """

    file = res_path + res_name + "/" + res_file
    with open(file) as fd:
        doc = xmltodict.parse(fd.read())  # Read the xml file

    results = doc['PhoronixTestSuite']['Result']

    count = 1
    i = 0

    def get_data(result):
        y_val = np.asarray(list(map(float, list(result['Data']['Entry'][-1]['Value'].split(",")))))
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

            ####################################################################
            # If cpu_usage_summary_only = True and the current data is
            # not for the CPU usage summary, then continue to next iteration.
            ####################################################################
            if cpu_usage_summary_only and title != 'CPU Usage (Summary) Monitor':
                i += 1
                continue

            ####################################################################################################
            # Here, cpu_usage_summary_only = False, which means we have to plot graphs for each core/thread.
            # We have to separately deal the case where we have to plot all the cores on one plot.
            # If we are plotting each core on a separate plot, the normal plotting code will do the work,
            # and we skip this section.
            ####################################################################################################
            if not cpu_usage_summary_only and not cpu_usage_separate_plots:

                plt.subplot(plt_layout[0], plt_layout[1], count)  # All cores on one subplot

                cpu_count = 0

                ############################################################################################
                # When we exit from this while loop, the `res` variable will have the data for the
                # CPU Usage (Summary). This is based on the fact that Phoronix Test Suite places the
                # summary data after listing the data for cores separately.
                ############################################################################################
                while title != 'CPU Usage (Summary) Monitor':
                    # Get data and plot for the current value of `res`
                    data_y, data_x = get_data(res)
                    lab = "CPU" + str(cpu_count)

                    plt.plot(data_x, data_y, '.-', label=lab)

                    # Initialise `res` to next value in the `results` list
                    i += 1
                    cpu_count += 1
                    res = results[i]
                    title = res['Title']

                plt.title("CPU per-core usage")
                plt.gca().yaxis.grid(True)
                plt.ylabel(res['Scale'])
                plt.tick_params(axis='x', which='both', labelbottom=False)
                plt.legend(loc="lower right", ncol=2)
                count += 1

        data_y, data_x = get_data(res)

        plt.subplot(plt_layout[0], plt_layout[1], count)
        plt.plot(data_x, data_y, '.r-')

        plt.title(title.replace(" Monitor", ""))

        # Remove ticks and labels from x-axis as they are arbitrary.
        # Courtesy: https://stackoverflow.com/a/12998531/8387076
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            # bottom=False,  # ticks along the bottom edge are off
            # top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off

        # Switch on grid for the y-axis ONLY.
        # Adapted from: https://stackoverflow.com/a/25799781/8387076
        plt.gca().yaxis.grid(True)

        plt.ylabel(res['Scale'])
        count += 1
        i += 1

    plt.suptitle(doc['PhoronixTestSuite']['Generated']['Title'], fontweight='bold')
    plt.tight_layout()

    # Delete subplot(s) which do not have any plot
    # Courtesy: https://stackoverflow.com/a/69886723/8387076
    for ax in axs.flat:
        if not bool(ax.has_data()):
            fig.delaxes(ax)  # delete if nothing is plotted in the ax object

    # Ensure tight layout even when the window size is changed by handling window resize event.
    # Courtesy: https://stackoverflow.com/a/47838687/8387076
    def on_resize(_):
        fig.tight_layout()
        fig.canvas.draw()

    _ = fig.canvas.mpl_connect('resize_event', on_resize)

    plt.show()


plot_phoronix_result("b6dfb1240a59bc2e9ebba504", ('cpu.temp', 'cpu.usage', 'gpu.usage', 'gpu.temp',
                                                  'sys.temp', 'memory.usage', 'cpu.freq', 'gpu.freq'), (4, 4),
                     cpu_usage_summary_only=False, cpu_usage_separate_plots=True)
