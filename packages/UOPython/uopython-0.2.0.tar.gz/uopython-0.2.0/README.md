[![PyPI version](https://badge.fury.io/py/uopython.svg)](https://badge.fury.io/py/uopython)

## uopython

uopython is a python library for rendering images from the Ultima Online client files. The SDK part of the project is almost a direct 1:1 code translation of the C# Ultima SDK (used by UOFiddler, among other things).

It does not support saving back to client files, only reading.

### Why?

The C# SDK does not run with mono due to implementations being missing from the underlying libraries. Attempts to get this to run in dotnet core or using mono have never been successful. Rewriting this code in Python allows the code to be used in a linux environment, for the most part out of the box. Since Python has many available popular open source web frameworks, this library allows you to serve up images directly in code used by your web framework of choice.

It also includes some features not seen anywhere else, such as the rendering of player avatars. Items & paperdolls have been done before in PHP, but that code is difficult to read and edit, whereas this library takes a much more flexible and simple approach (the same as which is used in the C# SDK). This lib even fixes a few rendering bugs which are present in the C# SDK.

### Features
uopython can currently do the following:
* Render land, statics. This includes rendering of in game items.
* Render "animations" or single frames of animations. This includes monsters and players, though player construction is done by rendering the mount, body, hair and clothing layers in order.
* Draw text from the client (eg, ASCIIFont).
* Extract information about skills - naming, groups, indexes.
* Rendering paperdolls / individual gumps
* Load and display Ultima Online map files

### Installation
Install uopython to your project with:

`pip install uopython`

You must specify your Ultima Online client directory by any of the following methods:

* `environment.ini` - add the line `ULTIMA_FILES_DIR=/path/to/ultima `
* Django - add into settings.py: `ULTIMA_FILES_DIR=/path/to/ultima`
* Specify an environment variable `ULTIMA_FILES_DIR` with the value `/path/to/ultima`

### Settings
As above, settings can be set through any of the methods that the `ULTIMA_FILES_DIR` can be set by (`environment.ini`, Django settings, environment variable).

Currently there are only 2 settings:
* `ULTIMA_FILES_DIR`, this is the path to your Ultima Online directory. This has no default and will not read from registry.
* `ULTIMA_MOUNT_IDS`, if loaded via environment, should be a valid json list of all possible mount IDs. If set in Django, can simply be set up as a list. This has a default of mounts that are found in the 5.0.8.3 client.


### How to use uopython

Here are detailed examples for using each major component of the library:

#### Working with Art (Items and Land Tiles)

```python
from uopython.sdk.art import Art

# Render a static item (like a moongate)
moongate_item_id = 0x0F6C
art = Art.get_static(moongate_item_id, check_max_id=False)
art.save("moongate.png")

# Render a land tile
land_id = 0x3
land_tile = Art.get_land(land_id)
land_tile.save("land_tile.png")

# Get dimensions of an item
width, height = art.width, art.height
print(f"Moongate dimensions: {width}x{height}")
```

#### Working with Hues (Colors)

```python
from uopython.sdk.art import Art
from uopython.sdk.hues import Hues

# Load an item
item_id = 0x0F6C
art = Art.get_static(item_id, check_max_id=False)

# Apply different hues
red_hue = Hues.HUES[32]  # Red
blue_hue = Hues.HUES[100]  # Blue
gold_hue = Hues.HUES[53]  # Gold

# Apply hues to the item
red_item = red_hue.apply_to(art, only_grey_pixels=False)
blue_item = blue_hue.apply_to(art, only_grey_pixels=True)  # Only applies to greyscale pixels
gold_item = gold_hue.apply_to(art)

# Save the results
red_item.save("red_item.png")
blue_item.save("blue_item.png")
gold_item.save("gold_item.png")
```

#### Working with Animations

```python
from uopython.sdk.animations import Animations

# Get a specific animation
body_id = 400  # Example: human male
action = 0  # Standing
direction = 0  # Facing north
animation = Animations.get_animation(body_id, action, direction)

# Save the first frame
if animation and animation.frames:
    frame = animation.frames[0]
    frame.save("human_standing.png")
    
# Get information about the animation
if animation:
    print(f"Animation frames: {len(animation.frames)}")
    print(f"Frame dimensions: {animation.frames[0].width}x{animation.frames[0].height}")
```

#### Creating Character Avatars

```python
from uopython.sdk.animation_assembler import AnimationAssembler

# Create a mounted character
body_id = 400  # Human male
action = 0  # Standing
direction = 0  # North
mount_id = 16000  # Horse

# Define equipment
equipment = [
    (0x1411, 0),      # (Item ID for chainmail tunic, hue 0)
    (0x1413, 0),      # (Item ID for chainmail leggings, hue 0)
    (0x1414, 0),      # (Item ID for chainmail coif, hue 0)
]

# Set hair and beard styles
hair_style = 0x203C
hair_hue = 1001
beard_style = 0x203E
beard_hue = 1001

# Create the avatar
avatar = AnimationAssembler.assemble_animation(
    body_id, action, direction, mount_id=mount_id,
    equipment=equipment, hair_style=hair_style, hair_hue=hair_hue,
    beard_style=beard_style, beard_hue=beard_hue
)

# Save the avatar
if avatar:
    avatar.save("mounted_knight.png")
```

#### Working with Fonts and Text

```python
from uopython.sdk.asciifont import ASCIIFont

# Load a font
font = ASCIIFont(3)  # Font style 3

# Render text
text_image = font.get_text("Hello Ultima Online!")
text_image.save("hello_uo.png")

# Get text with a specific color (hue)
colored_text = font.get_text("Colored Text", hue=32)  # Red text
colored_text.save("colored_text.png")
```

#### Working with Skills Information

```python
from uopython.sdk.skills import Skills

# Get all skills
all_skills = Skills.SKILLS

# Print information about each skill
for skill_id, skill in enumerate(all_skills):
    if skill:
        print(f"Skill #{skill_id}: {skill.name}, Group: {skill.group}")
        
# Look up a specific skill
fishing_skill = next((s for s in all_skills if s and s.name == "Fishing"), None)
if fishing_skill:
    print(f"Fishing skill ID: {all_skills.index(fishing_skill)}")
    print(f"Fishing skill group: {fishing_skill.group}")
```

#### Working with Gumps (UI Elements)

```python
from uopython.sdk.gumps import Gumps

# Load a gump
gump_id = 0x09A8  # Example gump ID
gump = Gumps.get_gump(gump_id)

# Save the gump image
if gump:
    gump.save("gump.png")
    print(f"Gump dimensions: {gump.width}x{gump.height}")
```

#### Rendering Paperdolls

```python
from uopython.sdk.paperdoll import Paperdoll

# Get a paperdoll for a specific body type
body_type = 400  # Human male
paperdoll = Paperdoll.get(body_type)

# Save the paperdoll
if paperdoll:
    paperdoll.save("paperdoll.png")
    
# Add equipment to a paperdoll
from uopython.sdk.gumps import Gumps

body_type = 400  # Human male
paperdoll = Paperdoll.get(body_type)

# Add armor pieces (these are gump IDs)
chest_piece = Gumps.get_gump(0x1411)  # Chainmail tunic
legs_piece = Gumps.get_gump(0x1413)   # Chainmail leggings

# Composite the equipment onto the paperdoll
# (This is a simplified example - actual implementation would depend on the library internals)
# final_paperdoll = paperdoll.composite([chest_piece, legs_piece])
# final_paperdoll.save("equipped_paperdoll.png")
```

### Using the map_loader module

The map_loader module allows you to load and interact with Ultima Online map files:

```python
from uopython.map_loader import MapLoader

# Initialize the map loader for a specific map
# Maps are numbered 0-5:
# 0: Felucca, 1: Trammel, 2: Ilshenar, 3: Malas, 4: Tokuno, 5: TerMur
map_loader = MapLoader(0)  # Loads map 0 (Felucca)

# Get an image of a specific region
# Parameters: start_x, start_y, width, height
map_image = map_loader.get_image(1400, 1450, 200, 200)
map_image.save("felucca_region.png")

# Get information about a specific map cell
cell = map_loader.get_cell(1400, 1450)
print(f"Terrain ID: {cell.id}")
print(f"Altitude: {cell.altitude}")

# Get multiple cells as a 2D array
# Parameters: start_x, start_y, width, height
cells = map_loader.get_cells(1400, 1450, 10, 10)
for y in range(10):
    for x in range(10):
        print(f"Cell at ({x+1400}, {y+1450}): Terrain ID {cells[y][x].id}")

# Get static items at a specific location
statics = map_loader.get_statics(1400, 1450)
for static in statics:
    print(f"Static item: ID {static.item_id}, Z {static.z}")

# Render a map with statics included
# Parameters: start_x, start_y, width, height, include_statics (boolean)
full_map_image = map_loader.get_image(1400, 1450, 200, 200, include_statics=True)
full_map_image.save("felucca_with_statics.png")

# Render a map centered on specific coordinates
# Parameters: center_x, center_y, radius (in cells)
centered_map = map_loader.get_centered_image(1400, 1450, 100)
centered_map.save("centered_map.png")
```

The map_loader provides comprehensive access to the Ultima Online map data, allowing you to:
* Render map regions with or without static items
* Get terrain and altitude information for specific locations
* Analyze static items at any location
* Create custom map visualizations for different purposes
