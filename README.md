# Ship Strain Measurement System

# Requirements
 - Python 3
 - OpenCV (headless)
 - PyQt5
 - imutils

# Installation
 1. Clone the repository to your machine and move into it.  
    `$ git clone https://github.com/noahdavis319/ship-strain-measurement-system.git ssms`  
    `$ cd ssms`
 2. Build the project using `make`  
    `$ make all`  
    - We use `make all` here since it is our first time.  
    A virtual environment will be made in `venv/` and all dependencies defined in `requirements.txt` will be installed 
    via `pip`.  
    In the future we can just use `make build` to build the wheel file and generate documentation,  
        or we can run `make install` to build the wheel file, generate documentation, and install the script.
 3. The project wheel file is built and placed in `dist/`
 4. The project documentation files are built and placed in `docs/build/html/`

# Usage
 1. Run the project `ssms run`
    - You can also use `ssms list` to detect available webcams.
    - Use `ssms --help` to show the help message.
        - Not all valid commands will be disabled. The help message is a work in progress.
        
# Development
 1. Make changes to the `ssms` python module as needed.
 2. Add any new Python package dependencies to `requirements.txt`
 3. Run `make all` to delete the current virtual environment and perform the build pipeline, ensuring all dependencies 
    are installed correctly.
 4. See [Usage](#Usage) for how to run the project.

