# FBX Processing Tool

A python-based tool for batch processing FBX assets. Built with PySide6 and Python FBX SDK, the tool is designed to automate common asset pipeline tasks such as analysis, mesh extraction, batch export, renaming, and axis conversion.


## Features
- Load and process multiple `.fbx` files at once  
- Analyze FBX scene hierarchy  
- Extract mesh objects  
- Batch export meshes to separate FBX files  
- Automatic renaming of exported files  
- Axis conversion (Maya, OpenGL, DirectX)



# Analyze .fbx Files

Loads all '.fbx' files from a selected folder and displays their full scene hierarchy.

## Find Meshes

The 'Find Meshes' option detects and lists all mesh objects contained in each FBX file.

## Export Single Mesh

The 'Export Single Mesh' option exports the first mesh found in each fbx file to a separate file.

## Export all/Rename

Exports all mesh objects from each FBX file.  
  
Output files are automatically renamed using:  
- Source file name  
- Mesh name  
- Index (to avoid duplicates)

## Axis Swap

Converts the coordinate system of FBX files to match different DCC tools:  
  
- Maya (Y-Up)  
- OpenGL (Z-Up)  
- DirectX  
  
Useful for ensuring compatibility between different pipelines.



## Usage  
  
1. Select a folder containing `.fbx` files  
2. Choose a processing option from the dropdown  
3. Set an output folder (if required)  
4. Click **Confirm**


## Download  
  
You can download the executable version from the Releases section.
