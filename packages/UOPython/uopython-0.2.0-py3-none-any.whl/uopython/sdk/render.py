import numpy as np
import os
import matplotlib.pyplot as plt
from radarcol import RadarCol
from map import Map

class MapRenderer:
    def __init__(self, map_id, uo_directory):
        self.map = Map(map_id, uo_directory)
        self.radarcol = RadarCol(uo_directory)

    def render_map(self, save_path=None):
        height, width = 512, 512  # Temporary size for demo
        img = np.zeros((height, width, 3), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                tile_id, _ = self.map.read_map_tile(x, y)
                img[y, x] = self.radarcol.get_color(tile_id)

        plt.imshow(img)
        plt.axis("off")

        if save_path:
            plt.imsave(save_path, img)
        else:
            plt.show()
