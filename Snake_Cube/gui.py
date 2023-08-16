
import matplotlib.pyplot as plt
import numpy as np
sample = {
    "coordinates": [
        [-5, 2, -6],
        [-5, 2, -5],
        [-5, 2, -4],
        [-4, 2, -4],
        [-3, 2, -4],
        [-3, 2, -3],
        [-3, 2, -2],
        [-2, 2, -2],
        [-1, 2, -2],
        [-1, 2, -1],
        [0, 2, -1],
        [0, 2, 0],
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0],
        [2, 0, 1],
        [3, 0, 1],
        [3, 0, 2],
        [3, 0, 3],
        [4, 0, 3],
        [4, 0, 4],
        [4, 0, 5],
        [5, 0, 5],
        [5, 0, 6],
        [6, 0, 6],
        [7, 0, 6],
    ],
    "sticky_cubes": [[5, 6], [12, 13], [14, 15], [15, 16], [18, 19]],
}


class Graphic():
    def __init__(self) -> None:
        pass

    def display(self, coordinates):

        voxelarray = np.zeros([25, 25, 25])
        for coor in coordinates:
            x, y, z = coor[0], coor[1], coor[2]
            x += 15
            y += 15
            z += 15
            voxelarray[x, y, z] = True
            

        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(voxelarray, edgecolor='k')

        plt.show()


# graphic = Graphic()

# graphic.display(sample_11["coordinates"])
