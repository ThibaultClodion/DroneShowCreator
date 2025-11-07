Don't use directly the Location Exporter Add-on into Blender, as recommended by Blender, create a symbolic link instead

Windows : mklink /D "C:\BlenderAddons\LocationExporter" "PathTo\LocationExporter"

Then go on Blender>Edit>Preferences>Get Extensions and go to the Repositories settings to add your local repository "C:\BlenderAddons\LocationExporter"