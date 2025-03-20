import os
import struct

class TileMatrix:
    def __init__(self, map_id, uo_directory):
        self.map_id = map_id
        self.uo_directory = uo_directory
        self.tile_data = self.load_tile_data()

    def load_tile_data(self):
        map_file = os.path.join(self.uo_directory, f"map{self.map_id}.mul")
        if not os.path.exists(map_file):
            raise FileNotFoundError(f"Missing map file: {map_file}")

        tile_data = {}
        with open(map_file, "rb") as f:
            while True:
                block = f.read(196)  # Each block is 196 bytes
                if not block:
                    break
                for i in range(64):  # 8x8 tiles per block
                    tile_id, altitude = struct.unpack("<Hh", block[i * 3 : i * 3 + 3])
                    tile_data[i] = (tile_id, altitude)
        return tile_data

    def get_tile_info(self, x, y):
        return self.tile_data.get((x, y), (0, 0))  # Default to empty tile
