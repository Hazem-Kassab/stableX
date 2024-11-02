from src.stablex import Structure
from src.stablex.visualization import visual_element_factory, plt


def plot_structure(structure: Structure, scale):
    # x_coordinates = [node.x for node in structure.nodes]
    # y_coordinates = [node.y for node in structure.nodes]
    # x_min = min(x_coordinates)
    # y_min = min(y_coordinates)
    # x_max = max(x_coordinates)
    # y_max = max(y_coordinates)
    # x_range = x_max - x_min
    # y_range = y_max - y_min
    # plt.axis((x_min - 1.1 * x_range/2,
    #           x_max + 1.1 * x_range/2,
    #           y_min - 1.1 * y_range/2,
    #           y_max + 1.1 * y_range/2))
    for element in structure.elements:
        vse = visual_element_factory.create_visual_element(element)
        vse.plot_element()
        vse.plot_global_displacement(scale)
    plt.show()


def plot(array_1, array_2, array_1_label, array_2_label):
    plt.close()
    fig = plt.figure()
    axs = fig.add_subplot()
    axs.plot(array_1, array_2)
    plt.xlabel(array_1_label)
    plt.ylabel(array_2_label)
    plt.grid()
    plt.show()
