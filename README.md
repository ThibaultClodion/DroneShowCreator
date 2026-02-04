# DroneShowCreator

A powerful Blender add-on for creating and exporting drone show animations. This extension allows you to convert 3D animated models into optimized data formats readable by [DroneShowFS24Player](https://github.com/djpadbit/DroneShowFS24Player).

## Features

- **Collection-based Export**: Select any Blender collection to export its animation data
- **Frame-by-frame Animation**: Captures position every frame
- **Mesh Decimation**: Reduce vertex count to optimize file size without recreating models
- **Dual Export Formats**:
  - **Binary**: Optimized format for the MFSM2024 system (little-endian)
  - **JSON**: Human-readable format for debugging and analysis
- **Texture Support**: Automatically extracts colors from UV-mapped image textures
- **Material Support**: Fallback to Principled BSDF base color when no texture is present
- **Smart Keyframe Optimization**: Avoids duplicate keyframes to reduce file size
- **Intuitive UI**: Clean panel interface in the 3D Viewport sidebar

## Installation

### Using Symbolic Link (Recommended)

Don't put the add-on directly into Blender. Instead, create a symbolic link to enable easier development and updates:

**Windows:**
```powershell
mklink /D "C:\BlenderAddons\DroneShowCreator" "C:\PathToYour\DroneShowCreator"
```

**Linux/macOS:**
```bash
ln -s /path/to/your/DroneShowCreator ~/BlenderAddons/DroneShowCreator
```

Then in Blender:
1. Go to **Edit > Preferences > Get Extensions**
2. Navigate to the **Repositories** settings
3. Add your local repository: `C:\BlenderAddons\DroneShowCreator` (or your path if you dont want to use Symbolic Link)
4. Enable the "Drone Show Creator" extension

### Requirements

- Blender 4.2.0 or later
- Python 3.x (included with Blender)
- NumPy (included with Blender)

## Usage

### Quick Start

1. **Open the Panel**: In the 3D Viewport, press `N` to open the sidebar and find the "Drone Show" tab
2. **Select Collection**: Choose the collection containing your animated objects
3. **Configure Settings**:
   - Set decimation ratio (1.0 = no decimation, lower = more optimization)
   - Choose export format (Binary or JSON)
   - Set output path and filename
4. **Export**: Click the "Export Data" button

### Decimation Settings

The decimation feature allows you to reduce vertex count without manually modifying your models:

- **1.0**: Keep all vertices (no decimation)
- **0.5**: Keep 50% of vertices
- **0.1**: Keep 10% of vertices (maximum optimization)

The decimated collection can be kept visible for preview or automatically deleted after export.

### Export Format Details

#### Binary Format (`.bin`)
- Optimized for the MFSM2024 drone system
- Little-endian byte order for x86 compatibility
- Smaller file size
- Faster loading times

#### JSON Format (`.json`)
- Human-readable
- Easy debugging and analysis
- Contains complete data structure with fps, object count, and all keyframes

### Data Structure

Each exported file contains:
- **FPS**: Frame rate from render settings
- **Objects**: Array of drone objects
- **Keyframes**: For each object, frame-by-frame data including:
  - Frame number
  - Position (x, y, z in world coordinates)

## Project Structure

```
DroneShowCreator/
├── __init__.py              # Add-on registration
├── blender_manifest.toml    # Extension metadata
├── editor.py                # UI panel definition
├── editor_properties.py     # Blender property definitions
├── exporter.py             # Export logic and data processing
├── object.py               # Data structures (Vector3, KeyFrame, Object)
└── README.md               # This file
```

## Technical Details

### Color Extraction

The add-on intelligently extracts vertex colors:
1. **UV-mapped textures**: Samples colors from image textures using UV coordinates
2. **Material base color**: Falls back to Principled BSDF base color
3. **Default**: Uses white (1.0, 1.0, 1.0) if no material is present

### Performance Optimization

- Uses NumPy for fast array operations
- Caches vertex colors to avoid redundant calculations
- Duplicate keyframe detection to minimize file size
- Efficient UV coordinate mapping for texture sampling

## License

This project is licensed under the GPL-3.0-or-later license.

## Related Projects

- [DroneShowFS24Player](https://github.com/djpadbit/DroneShowFS24Player) - Player for drone show data

---

```
    [---]           [---]   >>      MADE BY       <<
       \  DroneShow  /      >>  Thibault Clodion  <<
        \___________/       >> Pablo Couprie-Diaz <<
        /           \       >>     Peizhe Liu     <<
       /  MFSM2024   \      >>  Jounaïd Boudefar  <<
    [---]           [---]   >>    Iwan Derouet    <<
```
