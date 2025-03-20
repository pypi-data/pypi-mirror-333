# RAS Commander (ras-commander)

RAS Commander is a Python library for automating HEC-RAS operations, providing a set of tools to interact with HEC-RAS project files, execute simulations, and manage project data. This library was initially conceptualized in the Australian Water School course "AI Tools for Modelling Innovation", and subsequently expanded to cover the basic functionality of the HECRASController COM32 interface using open-source python libraries.  This library uses a Test Driven Development strategy, leveraging the publicly-available HEC-RAS Example projects to create repeatable demonstration examples.  The "Commmander" moniker is inspired by the "Command Line is All You Need" approach to HEC-RAS automation that was first implemented in the HEC-Commander Tools repository. 

## Contributors:
William Katzenmeyer, P.E., C.F.M. 

Sean Micek, P.E., C.F.M. 

Aaron Nichols, P.E., C.F.M. 

(Additional Contributors Here)  

## Don't Ask Me, Ask ChatGPT! 

This repository has several methods of interaction with Large Language Models and LLM-Assisted Coding built right in: 

1. **[RAS Commander Library Assistant GPT](https://chatgpt.com/g/g-TZRPR3oAO-ras-commander-library-assistant)**: A specialized GPT model with access to the ras-commander codebase and library, available for answering queries and providing code suggestions.   You can even upload your own plan, unsteady and HDF files to inspect and help determine how to automate your workflows or visualize your results, although this ability is still limited by OpenAI's GPT frameworks and may not be useful for long conversations.

2. **[Purpose-Built Knowledge Base Summaries](https://github.com/billk-FM/ras-commander/tree/main/ai_tools/assistant_knowledge_bases)**: Up-to-date compilations of the documentation and codebase for use with large language models like Claude or GPT-4. Look in 'ai_tools/assistant_knowledge_bases/' in the repo.  The repo's codebase (without documentation and examples) has been curated to stay within the current ~200k context window limitations of frontier models, and for tasks that do not need an understanding of the underlying code, the Comprehensive Library Guide and any relevant examples from the example folder should be adequate context for leveraging the ras-commander API to complete tasks. 

3. **[Cursor IDE Integration](https://github.com/billk-FM/ras-commander/blob/main/.cursorrules)**: Custom rules(.cursorrules) for the Cursor IDE to provide context-aware suggestions and documentation.  Just open the repository folder in Cursor to recognize these instructions.  You can create your own folders "/workspace/, "/projects/", or "my_projects/" as these are already in the .gitignore, and place your custom scripts there for your projects.  This will allow easy referencing of the ras-commander documents and individual repo files, the automatic loading of the .cursorrules file.  Alternatvely, download the github repo into your projects folder to easily load documents and use cursor rules files.

5. **[RAS-Commander Library Assistant](https://github.com/billk-FM/ras-commander/blob/main/library_assistant)**: A full-featured interface for multi-turn conversations, using your own API keys and the ras-commander library for context.  The library assistant allows you to load your own scripts and chat with specific examples and/or function classes in the RAS-Commander library to effectively utilize the library's functions in your workflow.  To reduce hallucinations, a file browser is included which adds full files to the conversation to ensure grounded responses.  A dashboard shows you the total context and estimated cost of each request.  **Now with support for OpenAI's o1 and o3-mini, and Deepseek V3 and R1 models using US-based Together.ai**


## Background
The ras-commander library emerged from the initial test-bed of AI-driven coding represented by the HEC-Commander tools Python notebooks. These notebooks served as a proof of concept, demonstrating the value proposition of automating HEC-RAS operations. The transition from notebooks to a structured library aims to provide a more robust, maintainable, and extensible solution for water resources engineers.

## Features

If you've ever read the book "Breaking the HEC-RAS Code" by Chris Goodell, this library is intended to be an AI-coded, pythonic library that provides a modern alternative to the HECRASController API.  By leveraginging modern python features libraries such as pandas, geopandas and H5Py (favoring HDF data sources wherever practicable) this library builds functionality around HEC-RAS 6.2+ while maintaining as much forward compatibilty as possible with HEC-RAS 2025.  

HEC-RAS Project Management & Execution
- Multi-project handling with parallel and sequential execution
- Command-line execution integration
- Project folder management and organization
- Multi-core processing optimization
- Progress tracking and logging
- Execution error handling and recovery


  
HDF Data Access & Analysis
- 2D mesh results processing (depths, velocities, WSE)
- Cross-section data extraction
- Boundary condition analysis
- Structure data (bridges, culverts, gates)
- Pipe network and pump station analysis
- Fluvial-pluvial boundary calculations
- Infiltration and precipitation data handling

  
RAS ASCII File Operations
- Plan file creation and modification
- Geometry file parsing examples 
- Unsteady flow file management
- Project file updates and validation  

Note about support for Pipe Networks:  As a relatively new feature, only read access to Pipe Network geometry and results data has been included.  Users will need to code their own methods to modify/add pipe network data, and pull requests are always welcome to incorporate this capability.  Please note that the library has not been tested with versions prior to HEC-RAS 6.2.

## Installation

First, create a virtual environment with conda or venv (ask ChatGPT if you need help).  

#### Install via Pip

In your virtual environment, install ras-commander using pip:
```
pip install h5py numpy pandas requests tqdm scipy xarray geopandas matplotlib ipython tqdm psutil shapely fiona pathlib rtree rasterstats
pip install --upgrade ras-commander
```
If you have dependency issues with pip (especially if you have errors with numpy), try clearing your local pip packages 'C:\Users\your_username\AppData\Roaming\Python\' and then creating a new virtual environment.  
   
#### Work in a Local Copy

If you want to make revisions and work actively in your local version of ras-commander, just skip the pip install rascommander step above and clone a fork of the repo to your local machine using Git (ask ChatGPT if you need help).  Most of the notebooks and examples in this repo have a code segment similar to the one below, that works as long as the script is located in a first-level subfolder of the ras-commander repository:
```
# Flexible imports to allow for development without installation
try:
    # Try to import from the installed package
    from ras_commander import init_ras_project, RasExamples, RasCmdr, RasPlan, RasGeo, RasUnsteady, RasUtils, ras
except ImportError:
    # If the import fails, add the parent directory to the Python path
    current_file = Path(__file__).resolve()
    parent_directory = current_file.parent.parent
    sys.path.append(str(parent_directory))
    # Alternately, you can just define a path sys.path.append(r"c:/path/to/rascommander/rascommander)")
    
    # Now try to import again
    from ras_commander import init_ras_project, RasExamples, RasCmdr, RasPlan, RasGeo, RasUnsteady, RasUtils, ras
```
It is highly suggested to fork this repository before going this route, and using Git to manage your changes!  This allows any revisions to the ras-commander classes and functions to be actively edited and developed by end users. The folders "/workspace/, "/projects/", or "my_projects/" are included in the .gitignore, so users can place you custom scripts there for any project data they don't want to be tracked by git.



  

## Quick Start Guide

```
from ras_commander import init_ras_project, RasCmdr, RasPlan
```

### Initialize a project
```
init_ras_project(r"/path/to/project", "6.5")
```

### Execute a single plan
```
RasCmdr.compute_plan("01", dest_folder=r"/path/to/results", overwrite_dest=True)
```

### Execute plans in parallel
```
results = RasCmdr.compute_parallel(
    plan_numbers=["01", "02"],
    max_workers=2,
    cores_per_run=2,
    dest_folder=r"/path/to/results",
    overwrite_dest=True
)
```

### Modify a plan
```
RasPlan.set_geom("01", "02")
```

Certainly! I'll provide you with an updated Key Components section and Project Organization diagram based on the current structure of the ras-commander library.

#### Key Components

- `RasPrj`: Manages HEC-RAS projects, handling initialization and data loading
- `RasCmdr`: Handles execution of HEC-RAS simulations
- `RasPlan`: Provides functions for modifying and updating plan files
- `RasGeo`: Handles operations related to geometry files
- `RasUnsteady`: Manages unsteady flow file operations
- `RasUtils`: Contains utility functions for file operations and data management
- `RasExamples`: Manages and loads HEC-RAS example projects

#### New Components:
- `HdfBase`: Core functionality for HDF file operations
- `HdfBndry`: Enhanced boundary condition handling
- `HdfMesh`: Comprehensive mesh data management
- `HdfPlan`: Plan data extraction and analysis
- `HdfResultsMesh`: Advanced mesh results processing
- `HdfResultsPlan`: Plan results analysis
- `HdfResultsXsec`: Cross-section results processing
- `HdfStruc`: Structure data management
- `HdfPipe`: Pipe network analysis tools
- `HdfPump`: Pump station analysis capabilities
- `HdfFluvialPluvial`: Fluvial-pluvial boundary analysis
- `RasMapper`: RASMapper interface
- `RasToGo`: Go-Consequences integration
- `HdfPlot` & `HdfResultsPlot`: Specialized plotting utilities

### Project Organization Diagram

### Project Organization Diagram

```
ras_commander
├── ras_commander
│   ├── __init__.py
│   ├── _version.py
│   ├── Decorators.py
│   ├── LoggingConfig.py
│   ├── RasCmdr.py
│   ├── RasExamples.py
│   ├── RasGeo.py
│   ├── RasPlan.py
│   ├── RasPrj.py
│   ├── RasUnsteady.py
│   ├── RasUtils.py
│   ├── RasToGo.py
│   ├── RasGpt.py
│   ├── HdfBase.py
│   ├── HdfBndry.py
│   ├── HdfMesh.py
│   ├── HdfPlan.py
│   ├── HdfResultsMesh.py
│   ├── HdfResultsPlan.py
│   ├── HdfResultsXsec.py
│   ├── HdfStruc.py
│   ├── HdfPipe.py
│   ├── HdfPump.py
│   ├── HdfFluvialPluvial.py
│   ├── HdfPlot.py
│   └── HdfResultsPlot.py
├── examples
│   ├── 01_project_initialization.py
│   ├── 02_plan_operations.py
│   ├── 03_geometry_operations.py
│   ├── 04_unsteady_flow_operations.py
│   ├── 05_utility_functions.py
│   ├── 06_single_plan_execution.py
│   ├── 07_sequential_plan_execution.py
│   ├── 08_parallel_execution.py
│   ├── 09_specifying_plans.py
│   ├── 10_arguments_for_compute.py
│   ├── 11_Using_RasExamples.ipynb
│   ├── 12_plan_set_execution.py
│   ├── 13_multiple_project_operations.py
│   ├── 14_Core_Sensitivity.ipynb
│   ├── 15_plan_key_operations.py
│   ├── 16_scanning_ras_project_info.py
│   ├── 17_parallel_execution_ble.py
│   └── HEC_RAS_2D_HDF_Analysis.ipynb
├── tests
│   └── ... (test files)
├── .gitignore
├── LICENSE
├── README.md
├── STYLE_GUIDE.md
├── Comprehensive_Library_Guide.md
├── pyproject.toml
├── setup.cfg
├── setup.py
└── requirements.txt
```

### Accessing HEC Examples through RasExamples

The `RasExamples` class provides functionality for quickly loading and managing HEC-RAS example projects. This is particularly useful for testing and development purposes.  All examples in the ras-commander repository currently utilize HEC example projects to provide fully running scripts and notebooks for end user testing, demonstration and adaption. 

Key features:
- Download and extract HEC-RAS example projects
- List available project categories and projects
- Extract specific projects for use
- Manage example project data efficiently

Example usage:
from ras_commander import RasExamples

```
ras_examples = RasExamples()
ras_examples.get_example_projects()  # Downloads example projects if not already present
categories = ras_examples.list_categories()
projects = ras_examples.list_projects("Steady Flow")
extracted_paths = ras_examples.extract_project(["Bald Eagle Creek", "Muncie"])
```

### RasPrj

The `RasPrj` class is central to managing HEC-RAS projects within the ras-commander library. It handles project initialization, data loading, and provides access to project components.

Key features:
- Initialize HEC-RAS projects
- Load and manage project data (plans, geometries, flows, etc.)
- Provide easy access to project files and information

Note: While a global `ras` object is available for convenience, you can create multiple `RasPrj` instances to manage several projects simultaneously.

Example usage:
```
from ras_commander import RasPrj, init_ras_project
```

#### Using the global ras object
```
init_ras_project("/path/to/project", "6.5")
```

#### Creating a custom RasPrj instance
```
custom_project = RasPrj()
init_ras_project("/path/to/another_project", "6.5", ras_instance=custom_project)
```

### RasHdf

The `RasHdf` class provides utilities for working with HDF files in HEC-RAS projects, enabling easy access to simulation results and model data.

Example usage:

```python
from ras_commander import RasHdf, init_ras_project, RasPrj

# Initialize project with a custom ras object
custom_ras = RasPrj()
init_ras_project("/path/to/project", "6.5", ras_instance=custom_ras)

# Get runtime data for a specific plan
plan_number = "01"
runtime_data = RasHdf.get_runtime_data(plan_number, ras_object=custom_ras)
print(runtime_data)
```
This class simplifies the process of extracting and analyzing data from HEC-RAS HDF output files, supporting tasks such as post-processing and result visualization.


#### Infrastructure Analysis
```python
from ras_commander import HdfPipe, HdfPump

# Analyze pipe network
pipe_network = HdfPipe.get_pipe_network(hdf_path)
conduits = HdfPipe.get_pipe_conduits(hdf_path)

# Analyze pump stations
pump_stations = HdfPump.get_pump_stations(hdf_path)
pump_performance = HdfPump.get_pump_station_summary(hdf_path)
```

#### Advanced Results Analysis
```python
from ras_commander import HdfResultsMesh

# Get maximum water surface and velocity
max_ws = HdfResultsMesh.get_mesh_max_ws(hdf_path)
max_vel = HdfResultsMesh.get_mesh_max_face_v(hdf_path)

# Visualize results
from ras_commander import HdfResultsPlot
HdfResultsPlot.plot_results_max_wsel(max_ws)
```

#### Fluvial-Pluvial Analysis
```python
from ras_commander import HdfFluvialPluvial

boundary = HdfFluvialPluvial.calculate_fluvial_pluvial_boundary(
    hdf_path,
    delta_t=12  # Time threshold in hours
)
```

## Documentation

For detailed usage instructions and API documentation, please refer to the [Comprehensive Library Guide](Comprehensive_Library_Guide.md).

## Examples

Check out the `examples/` directory for sample scripts demonstrating various features of ras-commander.

## Future Development

The ras-commander library is an ongoing project. Future plans include:
- Integration of more advanced AI-driven features
- Expansion of HMS and DSS functionalities
- Community-driven development of new modules and features

## Related Resources

- [HEC-Commander Blog](https://github.com/billk-FM/HEC-Commander/tree/main/Blog)
- [GPT-Commander YouTube Channel](https://www.youtube.com/@GPT_Commander)
- [ChatGPT Examples for Water Resources Engineers](https://github.com/billk-FM/HEC-Commander/tree/main/ChatGPT%20Examples)


## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and suggest improvements.

## Style Guide

This project follows a specific style guide to maintain consistency across the codebase. Please refer to the [Style Guide](STYLE_GUIDE.md) for details on coding conventions, documentation standards, and best practices.

## License

ras-commander is released under the MIT License. See the license file for details.

## Acknowledgments

RAS Commander is based on the HEC-Commander project's "Command Line is All You Need" approach, leveraging the HEC-RAS command-line interface for automation. The initial development of this library was presented in the HEC-Commander Tools repository. In a 2024 Australian Water School webinar, Bill demonstrated the derivation of basic HEC-RAS automation functions from plain language instructions. Leveraging the previously developed code and AI tools, the library was created. The primary tools used for this initial development were Anthropic's Claude, GPT-4, Google's Gemini Experimental models, and the Cursor AI Coding IDE.

Additionally, we would like to acknowledge the following notable contributions and attributions for open source projects which significantly influenced the development of RAS Commander:

1. Contributions: Sean Micek's [`funkshuns`](https://github.com/openSourcerer9000/funkshuns), [`TXTure`](https://github.com/openSourcerer9000/TXTure), and [`RASmatazz`](https://github.com/openSourcerer9000/RASmatazz) libraries provided inspiration, code examples and utility functions which were adapted with AI for use in RAS Commander. Sean has also contributed heavily to 

- Development of additional HDF functions for detailed analysis and mapping of HEC-RAS results within the RasHdf class.
- Development of the prototype `RasCmdr` class for executing HEC-RAS simulations.
- Optimization examples and methods from (INSERT REFERENCE) for use in the Ras-Commander library examples

2. Attribution: The [`pyHMT2D`](https://github.com/psu-efd/pyHMT2D/) project by Xiaofeng Liu, which provided insights into HDF file handling methods for HEC-RAS outputs.  Many of the functions in the [Ras_2D_Data.py](https://github.com/psu-efd/pyHMT2D/blob/main/pyHMT2D/Hydraulic_Models_Data/RAS_2D/RAS_2D_Data.py) file were adapted with AI for use in RAS Commander. 

   Xiaofeng Liu, Ph.D., P.E.,    Associate Professor, Department of Civil and Environmental Engineering
   Institute of Computational and Data Sciences, Penn State University

3. Attribution: The[ffrd\rashdf'](https://github.com/fema-ffrd/rashdf) project by FEMA-FFRD (FEMA Future of Flood Risk Data) was incorporated, revised, adapted and extended in rascommander's RasHDF libaries (where noted). 

These acknowledgments recognize the contributions and inspirations that have helped shape RAS Commander, ensuring proper attribution for the ideas and code that have influenced its development.

4. Chris Goodell, "Breaking the HEC-RAS Code" - Studied and used as a reference for understanding the inner workings of HEC-RAS, providing valuable insights into the software's functionality and structure.

5. [HEC-Commander Tools](https://github.com/billk-FM/HEC-Commander) - Inspiration and initial code base for the development of RAS Commander.


## Official RAS Commander AI-Generated Songs:

[No More Wait and See (Bluegrass)](https://suno.com/song/16889f3e-50f1-4afe-b779-a41738d7617a)  

[No More Wait and See (Cajun Zydeco)](https://suno.com/song/4441c45d-f6cd-47b9-8fbc-1f7b277ee8ed)  

## Other Resources

Notebook version of RAS-Commander: [RAS-Commander Notebook in the HEC-Commander Tools Repository](https://github.com/billk-FM/HEC-Commander/tree/main/RAS-Commander)
Youtube Tutorials for HEC-Commander Tools and RAS-Commander: [GPT-Commander on YouTube](https://www.youtube.com/@GPT_Commander/videos)

## LICENSE

This software is released under the MIT license.


## Contact

For questions, suggestions, or support, please contact:
William Katzenmeyer, P.E., C.F.M. - heccommander@gmail.com
