# SavePip

A tool to install and save clean package dependencies for both pip and conda environments.

## Installation

```bash
pip install savepip
```

## Usage
```bash
# Install packages with pip
savepip install pandas numpy

# Install packages with conda
savepip -m conda numpy pandas

# Save current environment
savepip save

# Upgrade packages
savepip -u requests pandas

# Save to custom file
savepip -o custom_requirements.txt requests pandas
 ```

## Features
- Supports both pip and conda package managers
- Cleans up dependency specifications
- Preserves existing dependencies
- Sorts dependencies alphabetically
- Removes build hashes and unnecessary information
