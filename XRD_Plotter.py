import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def ASC(filename):
    x = []
    y = []
    tally = 0  # keeps track of the line number before the data begins
    line_num = 0

    with open(filename, 'r') as file:
        line = file.readline()
        Theta_range = []
        while line:
            if tally == 4:
                line.strip()
                beg_list = list(line.split("="))
                Theta_range.append(beg_list[1])
            elif tally == 5:
                line.strip()
                end_list = list(line.split("="))
                Theta_range.append(end_list[1])
            elif tally == 14:  # this is so the metadata does not get plotted
                line_num = 1
            if line_num == 1:
                line = line.strip()
                line.split("	      ")
                if line == "@END":
                    break
                else:
                    x.append(float(line[0:8].strip()))
                    y.append((float(line[10:].strip())))
            line = file.readline()
            tally += 1
    return [x, y, Theta_range]


def xy(filename):
    x = []
    y = []

    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            line = line.split()
            x.append(float((line[0]).strip()))
            y.append(float((line[1]).strip()))
            line = file.readline()
    return [x, y]


def format_my_plot():  # Function given to me by PI for desired formatting.
    plt.gcf().set_size_inches(6, 6)
    plt.rcParams.update({'axes.linewidth': 1.2})
    plt.locator_params(axis='y', nbins=6)
    plt.tick_params(axis='y', left=1, right=1, direction='in', length=13, width=1.2)
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))
    plt.tick_params(which='minor', direction='in', left=1, right=1, length=7, width=1.2)
    plt.tick_params(axis='x', bottom=1, top=1, direction='in', length=13, width=1.2)
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))
    plt.tick_params(which='minor', direction='in', bottom=1, top=1, length=7, width=1.2)
    plt.gca().set_aspect(1./plt.gca().get_data_ratio())
    plt.rcParams.update({'font.size': 14})


def format_my_legend():  # Function given to me by PI for desired formatting.
    leg = plt.legend(framealpha=1, reverse=True)  # Legend order matches the order of the offset graphs (reverse)
    leg.get_frame().set_edgecolor('black')
    leg.get_frame().set_facecolor('white')
    leg.get_frame().set_linewidth(1.1)
    leg.get_frame().set_boxstyle('Round', pad=0.1, rounding_size=-0.0001)


def flatten_nested_list(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten_nested_list(item))
        else:
            flat_list.append(item)
    return flat_list


plt.figure()  # create the figure so we can add stuff to it later
cmap = plt.get_cmap('Reds')  # >>>SET COLOR SCALE HERE<<<

"""A Red gradient is a surpisingly acessible plot theme color for color blind people as it allows
them to distinguish between different plots well. Personally, I am Red-Green color blind and I find
the red color scheme to still work well for me with enough shading differece between plots."""

plotname = input("NAME OF PLOT> ")  # User input for plot, it also sets the name for the file that is output.
num_files = int(input("NUMBER OF FILES> "))  # Number of files that the user will input
filetype = []  # Initializing lists that will be need in the for loop below
files = []
legend = []
for i in range(num_files):
    filename = input("FILE> ")
    legend_label = input("DATA LABEL> ")  # The data label of the data set in the graph legend
    filename = filename.strip()
    files.append(filename)  # Add file to the index of files
    z = filename.split(".")  # Create a list to determine the file type
    filetype.append(z[1])
    legend.append(legend_label)

xlimit = float(input("X-AXIS LIMIT> "))
offset_mult = float(input("OFFSET MULTIPLIER> "))
clr = float(2.20)  # initial color value for the color gradient

x_all = []
y_all = []
x_range = []
for i in range(len(files)):
    if filetype[i] == "ASC":
        x_y = ASC(files[i])  # have the function output to a list for efficiency's sake
        x_all.append(x_y[0])
        y_all.append(x_y[1])
        x_range.append(x_y[2])

    if filetype[i] == "xy":
        x_y = xy(files[i])
        x_all.append(x_y[0])
        y_all.append(x_y[1])

x_range = flatten_nested_list(x_range)
# theta_min = str(min(x_range)).replace("\n", '')
# theta_max = str(max(x_range)).replace("\n", '')

for i in range(len(files)):
    min_y = min(y_all[i])
    max_y = max(y_all[i])
    y_all[i] = [(y-min_y) / (max_y-min_y) for y in y_all[i]]  # normalize data in terms of itself

max_y = 0

for i in range(len(files)):
    max_y = max(y_all[i])
    y_all[i] = list(map(lambda y: y + (max_y * i * offset_mult), y_all[i]))
    plt.plot(x_all[i], y_all[i], color=cmap(clr % 1), label=legend[i])
    clr += 0.2  # Update color value so the graphs look different

plt.xlim(right=xlimit)  # Set X-limit from user input
plt.xlabel("2"+'\u03B8'+" (" + '\u00B0'+', CuK' + '\u03B1'+')', fontsize=14)  # Unicode symbols not on keyboard.
# CuK(alpha) is the x-ray beam emitter.
plt.ylabel("Peak Intensity (a.u.)", fontsize=14)
plt.title("")  # My research professor does not like plot titles.
# If I were to put this figure on a poster or in a research paper, the legend is all that is really necessary.
plt.legend()  # Create a new legend with the reversed order
format_my_plot()  # format plot such that it makes a good research figure, proper tick marks etc.
format_my_legend()  # same thing here instead for the legend positioning etc.
# print(f"Your 2\u03B8 data range from inputted files: {theta_min}\u00B0-{theta_max}\u00B0")
# ^^ So user is aware of available emperical data.
plt.savefig(f"{plotname}.pdf", dpi=900)  # for research applications dpi > 300 is required
plt.show()
