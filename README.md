# DroneShowCreator

A Blender add-on for creating drone shows for Microsoft Flight Simulator 2024. This tool allows you to export animated mesh data from Blender to be played back in MSFS 2024 using the [DroneShowFS24Player](https://github.com/djpadbit/DroneShowFS24Player) add-on.

---

## Installation

### Prerequisites

- **Blender 4.2.0 or higher**

### Installation Steps

1. Download this repository as a ZIP file (or clone it)
2. Open Blender
3. Go to `Edit > Preferences > Add-ons`
4. Click `Install...` and select the ZIP file
5. Enable the add-on by checking the box next to "Drone Show Creator"
6. The add-on panel will appear in the 3D Viewport sidebar under the "Drone Show" tab

### Alternative: Development Installation (Symbolic Link)

For easier development and updates, create a symbolic link instead:

**Windows:**
```powershell
mklink /D "C:\Users\YourName\AppData\Roaming\Blender Foundation\Blender\4.2\scripts\addons\DroneShowCreator" "C:\Path\To\DroneShowCreator"
```

**Linux/macOS:**
```bash
ln -s /path/to/DroneShowCreator ~/.config/blender/4.2/scripts/addons/DroneShowCreator
```

---

## Usage Guide

### 1. Prepare Your Scene

1. Create or import your 3D models in Blender
2. Organize your animated meshes into a **Collection**
3. Animate the objects in the timeline
   - **Position**: Animate object transforms (location, rotation)
   - **Color**: Use materials with textures or base colors
     - Colors are extracted from UV-mapped image textures
     - Or from Principled BSDF Base Color

### 2. Open the Drone Show Panel

1. In the 3D Viewport, press `N` to open the sidebar
2. Click on the **Drone Show** tab

### 3. Configure Export Settings

#### Collection Settings
- **Target Collection**: Select the collection containing your drone show objects

#### Decimation Settings
- **Decimation Ratio**: Reduce vertex count to optimize file size
  - `1.0` = Keep all vertices (no decimation)
  - `0.5` = Keep 50% of vertices
  - `0.1` = Keep 10% of vertices (maximum optimization)
- **Keep Decimated Collection**: Check to keep the decimated collection in your scene after export (useful for preview)

#### Export Format
- **Binary**: Optimized format for MSFS 2024 (recommended for production)
- **JSON**: Human-readable format (useful for debugging)

#### Output Settings
- **File Path**: Directory where the file will be saved (e.g., `C:\Users\YourName\Downloads\`)
- **File Name**: Name of the export file (extension `.bin` or `.json` added automatically)

### 4. Export Your Drone Show

1. Set your timeline range (`Animation Start` and `Animation End` frames)
2. Click the **Export Data** button
3. Wait for the export to complete
4. Your file will be saved to the specified location

The exported `.bin` file can now be used with the DroneShowFS24Player add-on in Microsoft Flight Simulator 2024.

## Tips & Best Practices

### Optimization
- **Use decimation**: Large vertex counts create huge files - use decimation to optimize
- **Keep it simple**: Start with simple animations before creating complex shows
- **Test frame ranges**: Use shorter frame ranges for testing

### Materials & Colors
- **Texture-based**: Use UV-mapped image textures for best color control
- **Material-based**: Set Base Color in Principled BSDF for solid colors
- **Default**: Objects without materials will be white

### Animation
- **Frame range**: Set your timeline start/end frames to match your animation
- **FPS**: The exporter uses your scene's render FPS setting
- **World coordinates**: Positions are exported in world space coordinates

### Organization
- **Use collections**: Keep all show objects in one collection for easy export
- **Name your objects**: Use clear naming conventions for easier debugging
- **Preview decimation**: Enable "Keep Decimated Collection" to preview the decimated result

## Credits

```
    [---]           [---]   >>      MADE BY       <<
       \  DroneShow  /      >>  Thibault Clodion  <<
        \___________/       >> Pablo Couprie-Diaz <<
        /           \       >>     Peizhe Liu     <<
       /  MFSM2024   \      >>  Jounaïd Boudefar  <<
    [---]           [---]   >>    Iwan Derouet    <<
```

## License

This project is licensed under GPL-3.0-or-later.

---

## Related Projects

- [DroneShowFS24Player](https://github.com/djpadbit/DroneShowFS24Player) - MSFS 2024 add-on for playing drone shows in the simulator
