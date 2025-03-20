import os
import io
import struct
from PIL import Image
import numpy as np
from uopython.settings import ultima_file_path

class Map:
    """
    Class to handle loading and displaying map data from Ultima Online.
    
    This class provides methods to:
    - Load map data from UO client files
    - Retrieve map tile information at specific coordinates
    - Generate images for map regions
    - Support different map facets (e.g., Felucca, Trammel)
    """
    
    def __init__(self):
        """Initialize the Map with default settings."""
        self.maps = {}
        self.map_dimensions = {
            0: (7168, 4096),  # Felucca/Trammel
            1: (7168, 4096),  # Felucca/Trammel
            2: (2304, 1600),  # Ilshenar
            3: (2560, 2048),  # Malas
            4: (1448, 1448),  # Tokuno
            5: (1280, 4096)   # TerMur
        }
        self.statics = {}
        self.loaded_facets = set()
        
    def load_map(self, facet=0):
        """
        Load map data for a specific facet.
        
        Args:
            facet (int): The facet number to load (0=Felucca, 1=Trammel, etc.)
            
        Returns:
            bool: True if map was loaded successfully, False otherwise
        """
        if facet in self.loaded_facets:
            return True
            
        try:
            map_path = ultima_file_path(f"map{facet}.mul")
            statics_path = ultima_file_path(f"statics{facet}.mul")
            staidx_path = ultima_file_path(f"staidx{facet}.mul")
            
            if not os.path.exists(map_path):
                print(f"Map file for facet {facet} not found at {map_path}")
                return False
                
            # Store the paths for later use
            self.maps[facet] = map_path
            
            if os.path.exists(statics_path) and os.path.exists(staidx_path):
                self.statics[facet] = (statics_path, staidx_path)
            
            self.loaded_facets.add(facet)
            return True
            
        except Exception as e:
            print(f"Error loading map facet {facet}: {e}")
            return False
    
    def get_map_dimensions(self, facet=0):
        """
        Get the dimensions of a specific map facet.
        
        Args:
            facet (int): The facet number
            
        Returns:
            tuple: (width, height) of the map in tiles
        """
        return self.map_dimensions.get(facet, (0, 0))
    
    def read_map_tile(self, x, y, facet=0):
        """
        Read map tile data at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            facet (int): Map facet
            
        Returns:
            dict: Tile data with keys 'id', 'z', and 'verified'
        """
        if facet not in self.loaded_facets:
            if not self.load_map(facet):
                return None
        
        map_path = self.maps.get(facet)
        if not map_path:
            return None
            
        width, height = self.map_dimensions.get(facet, (0, 0))
        if x < 0 or y < 0 or x >= width or y >= height:
            return None
            
        try:
            with open(map_path, 'rb') as f:
                # Each tile is 4 bytes: 2 bytes for ID, 1 byte for Z, 1 byte for verified
                offset = (x * height + y) * 4
                f.seek(offset)
                tile_data = f.read(4)
                
                if len(tile_data) != 4:
                    return None
                    
                tile_id = struct.unpack("<H", tile_data[0:2])[0]
                z = struct.unpack("<b", tile_data[2:3])[0]
                verified = struct.unpack("<B", tile_data[3:4])[0]
                
                return {
                    'id': tile_id,
                    'z': z,
                    'verified': verified
                }
                
        except Exception as e:
            print(f"Error reading map tile at ({x}, {y}): {e}")
            return None
    
    def get_map_image(self, x, y, width, height, facet=0, scale=1.0):
        """
        Generate an image of a map region.
        
        Args:
            x (int): Starting X coordinate
            y (int): Starting Y coordinate
            width (int): Width of the region in tiles
            height (int): Height of the region in tiles
            facet (int): Map facet
            scale (float): Scale factor for the image
            
        Returns:
            PIL.Image: Image of the map region
        """
        if facet not in self.loaded_facets:
            if not self.load_map(facet):
                return None
                
        # Create an array for our map image
        map_width = width
        map_height = height
        
        # RGB image (3 channels)
        image_data = np.zeros((map_height, map_width, 3), dtype=np.uint8)
        
        # Basic heightmap-based coloring, can be enhanced
        for i in range(map_width):
            for j in range(map_height):
                tile = self.read_map_tile(x + i, y + j, facet)
                if tile:
                    # Basic coloring based on tile ID and Z
                    # Water tiles (IDs from 0 to around 200)
                    if tile['id'] < 200:
                        color = (0, 0, 150 + tile['id'] % 100)  # Blue for water
                    # Land tiles
                    else:
                        # Use z value to create a heightmap effect
                        z_val = tile['z'] + 128  # Z is signed, shift to positive
                        
                        # Desert/sandy
                        if 500 <= tile['id'] < 1000:
                            color = (210, 190, 140)
                        # Grass/forest
                        elif 1000 <= tile['id'] < 1500:
                            color = (0, 100 + (z_val % 100), 0)
                        # Mountains/hills
                        elif 1500 <= tile['id'] < 2000:
                            color = (120 + (z_val % 100), 100, 80)
                        # Snow
                        elif 2000 <= tile['id'] < 2500:
                            color = (220 + (z_val % 30), 220 + (z_val % 30), 230)
                        # Default land
                        else:
                            # Terrain heightmap coloring
                            green = 100 + (z_val % 100)
                            color = (100, green, 50)
                            
                    image_data[j, i] = color
        
        # Create PIL image from numpy array
        img = Image.fromarray(image_data, 'RGB')
        
        # Resize if scale != 1.0
        if scale != 1.0:
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.NEAREST)
            
        return img
    
    def get_map_region(self, x, y, width, height, facet=0, format='PNG'):
        """
        Get a map region as an image byte stream.
        
        Args:
            x (int): Starting X coordinate
            y (int): Starting Y coordinate
            width (int): Width of the region in tiles
            height (int): Height of the region in tiles
            facet (int): Map facet
            format (str): Image format (PNG, JPEG, etc.)
            
        Returns:
            bytes: Image data as bytes
        """
        img = self.get_map_image(x, y, width, height, facet)
        if img is None:
            return None
            
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=format)
        return img_byte_arr.getvalue()
    
    def get_valid_facets(self):
        """
        Return a list of valid facets that have map files.
        
        Returns:
            list: List of facet numbers that have valid map files
        """
        valid_facets = []
        for facet in range(6):  # Check facets 0-5
            map_path = ultima_file_path(f"map{facet}.mul")
            if os.path.exists(map_path):
                valid_facets.append(facet)
        return valid_facets
    def get_map_count(self):
        """
        Get the number of available maps.
        
        Returns:
            int: Number of available map facets
        """
        return len(self.get_valid_facets())
    
    def get_map_section(self, facet=0, x=0, y=0, width=100, height=100, scale=1.0):
        """
        Get a specific section of the map as an image.
        
        Args:
            facet (int): Map facet to use
            x (int): Starting X coordinate
            y (int): Starting Y coordinate
            width (int): Width of the section in tiles
            height (int): Height of the section in tiles
            scale (float): Scale factor for the image
            
        Returns:
            bytes: PNG image data as bytes
        """
        img = self.get_map_image(x, y, width, height, facet, scale)
        if img is None:
            return None
            
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        return img_byte_arr.getvalue()
    
    def get_map_regions(self, facet=0):
        """
        Get information about predefined regions in the map.
        
        Args:
            facet (int): Map facet to query
            
        Returns:
            list: List of dictionaries containing region information
        """
        # This is a placeholder for actual region data
        # In a real implementation, this would be loaded from a configuration file
        # or extracted from the UO client files
        
        # Define some common regions for Felucca/Trammel (facet 0/1)
        felucca_trammel_regions = [
            {"name": "Britain", "x": 1400, "y": 1600, "width": 300, "height": 300},
            {"name": "Trinsic", "x": 1800, "y": 2800, "width": 250, "height": 250},
            {"name": "Moonglow", "x": 4400, "y": 1200, "width": 200, "height": 200},
            {"name": "Jhelom", "x": 1300, "y": 3650, "width": 200, "height": 200},
            {"name": "Yew", "x": 600, "y": 1000, "width": 250, "height": 250},
            {"name": "Minoc", "x": 2500, "y": 400, "width": 200, "height": 200},
            {"name": "Cove", "x": 2200, "y": 1200, "width": 150, "height": 150},
            {"name": "Vesper", "x": 2900, "y": 800, "width": 200, "height": 200},
            {"name": "Buccaneer's Den", "x": 2700, "y": 2100, "width": 150, "height": 150},
            {"name": "Magincia", "x": 3700, "y": 2100, "width": 200, "height": 200}
        ]
        
        # Define some regions for Ilshenar (facet 2)
        ilshenar_regions = [
            {"name": "Compassion", "x": 1100, "y": 1100, "width": 200, "height": 200},
            {"name": "Honesty", "x": 800, "y": 650, "width": 150, "height": 150},
            {"name": "Valor", "x": 500, "y": 1100, "width": 150, "height": 150},
            {"name": "Justice", "x": 950, "y": 1400, "width": 150, "height": 150}
        ]
        
        # Define some regions for Malas (facet 3)
        malas_regions = [
            {"name": "Luna", "x": 1000, "y": 1000, "width": 200, "height": 200},
            {"name": "Umbra", "x": 1800, "y": 1000, "width": 200, "height": 200}
        ]
        
        # Define some regions for Tokuno (facet 4)
        tokuno_regions = [
            {"name": "Zento", "x": 700, "y": 1200, "width": 150, "height": 150},
            {"name": "Isamu-Jima", "x": 1000, "y": 800, "width": 200, "height": 150},
            {"name": "Makoto-Jima", "x": 700, "y": 700, "width": 150, "height": 150},
            {"name": "Homare-Jima", "x": 400, "y": 400, "width": 200, "height": 200}
        ]
        
        # Return appropriate regions based on facet
        if facet in [0, 1]:
            return felucca_trammel_regions
        elif facet == 2:
            return ilshenar_regions
        elif facet == 3:
            return malas_regions
        elif facet == 4:
            return tokuno_regions
        else:
            return []

# Backward compatibility alias
UOMap = Map  # Allows existing code using UOMap to continue working
