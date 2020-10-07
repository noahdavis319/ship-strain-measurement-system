# ship-strain-measurement-system

# Requirements
 - Python 3
 - OpenCV (headless)
 - PyQt5
 - imutils

These requirements will be installed automatically for you if you use the `create-dev-environment` script, as described how below.

# Installation
 1. Clone the repository to your machine.
 2. Add executable permissions to `create-dev-environment` with `chmod +x create-dev-environment`
 3. Run the `create-dev-environment` script with `source create-dev-environment`
    - The PyCharm IDE integration files will be created.
    - A virtual environment will be created in `venv/`
    - The virtual environment will be sourced/activated for you.
    - The project will be built and installed to your path.
        - You can manually do this in the future with `pyb -v install`

# Usage
 1. Run the project `ssms run`
    - You can also use `ssms list` to detect available webcams.
    - Use `ssms --help` to show the help message.
        - Not all valid commands will be disabled. The help message is a work in progress.

