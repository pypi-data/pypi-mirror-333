import struct
import os

class RadarCol:
    def __init__(self, uo_directory):
        self.colors = {}
        self.load_radarcol(uo_directory)

    def load_radarcol(self, uo_directory):
        radarcol_path = os.path.join(uo_directory, "radarcol.mul")
        if not os.path.exists(radarcol_path):
            raise FileNotFoundError(f"Missing radarcol.mul at {radarcol_path}")

        with open(radarcol_path, "rb") as f:
            for tile_id in range(0x10000):  # 65,536 entries
                color_data = f.read(2)
                if not color_data:
                    break
                color_value = struct.unpack("<H", color_data)[0]  # Little-endian ushort
                self.colors[tile_id] = self.convert_to_rgb(color_value)

    def convert_to_rgb(self, color_value):
        r = ((color_value >> 10) & 0x1F) * 8
        g = ((color_value >> 5) & 0x1F) * 8
        b = (color_value & 0x1F) * 8
        return (r, g, b)

    def get_color(self, tile_id):
        return self.colors.get(tile_id, (0, 0, 0))  # Default to black if missing
