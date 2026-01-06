# Unisteg_tool_final

Use python 3.13.7 also install exiftool and rename the exiftool(-k).exe file to exiftool.exe then use the full path to the exe file in the subprocess.run() method in the metadata code.
## Install dependencies
```bash
pip install numpy python-magic-bin opencv-python pillow
```
## Usage Instructions
1.first cd to the folder where unisteg_project lives. <br>
2.type the following command to see the list of available commands and other information
```bash
python -m unisteg_project.cli -help
```
3.In order to analyze a file(run all the relevant stego algos)
```bash
python -m unisteg_project.cli analyze <path\to\your\file>
```
4.In order to analyze a file forcefully with a specific plugin
```bash
python -m unisteg_project.cli analyze-with <plugin_name> <path\to\your\file>
```
5.In order to encode the payload in a file using a specific plugin
```bash
python -m universal_steg.cli encode <plugin_name> <destination_file> <payload> <original_file>
```
6.In order to see the list of available pluggins(algorithms)
```bash
python -m universal_steg.cli list-pluggins
```
7. In order to add a new pluggin file we just need to add the file in the pluggins folder and it should include an analyzer class that should subclass the base analyzer and make sure to include the encode, decode functions and specify the supported mime types.
# Project report 
## Solution overview
This project implements a Universal Steganography Tool that detects and performs steganography on multiple file types (images, audio, video, and text) using a plugin‑based architecture. The core engine dynamically discovers analysis plugins at runtime, registers them in a central registry, and routes each input file to the appropriate algorithms based on its type or MIME information. Each plugin encapsulates a specific stego technique such as appended‑data hiding, simple metadata‑based storage, or text‑based schemes, and exposes a common interface for encoding and decoding.<br>
The tool provides a command‑line interface built with argparse supporting subcommands like analyze, analyze-with, encode, and list-plugins, enabling users to either automatically run all applicable plugins or explicitly select a particular algorithm for a given file. The design separates concerns clearly: core.py handles plugin loading and orchestration, individual plugin modules implement steganography logic, and cli.py manages user interaction, argument parsing, and result presentation. This structure makes it easy to add new algorithms or support additional formats without modifying the core<br>
For the metadata analysis, I used an external tool(exiftool).The project deepened understanding of Python plugin systems by using importlib to discover modules in a plugins/ package, enforcing a shared abstract base class, and maintaining a registry of available analyzers. 
## Challenges faced
1.One major challenge was correctly detecting file types and matching them to plugins using consistent identifiers; early versions mixed extensions and MIME strings, and even forgot to call the detector function, which led to the “No suitable plugins for this file type” problem until the matching logic and supported_mimes values were aligned. This highlighted how brittle plugin routing can be when type detection and plugin metadata are not strictly coordinated<br>
2.Another major issue was that sometimes the pluggins could only decode the files it itself encoded as it is not possible to always know how a random file is always encoded for example in the case of an lsb we cannot determine the delimiter(marking the end of the data) for sure and in some files do not have a fixed termination condition like IEND for PNG data so it is dificult to encode appended data structures in them. 
