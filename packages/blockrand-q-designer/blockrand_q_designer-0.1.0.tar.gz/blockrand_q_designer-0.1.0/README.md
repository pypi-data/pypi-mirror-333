# Block randomized queue designer for LCMS experiments

[![DOI](https://zenodo.org/badge/DOI/your_doi_here.svg)](https://doi.org/10.5281/zenodo.15019270)

## Overview

**Block randomized queue designer** is a Python utility to automatically generate an optimal acquisition queue for sequential experiments such as LCMS experiments run on a single instrument. It accepts any full factorial experimental design with arbitrary number of factors, each of which can have a different number of levels, and an independently chosen block size. Given these tools, the tool will provide users with a block-randomized queue that respects the following constraints. For factors with a number of levels equal to the block size, it will perform strict blocking (each and all levels will be present in each block). For factors with less levels than block size, it will allocate levels so that, for any two levels, the difference between the number of samples holding those levels is at most one. For factors with more levels than the block size, it will enforce that no level be repeated in a block. Should the total number of samples not be divisible by the block size, the remaining samples at the end of the procedure will make up the last block, with relaxed constraints. An intra-block reshuffling method optimizes the position of samples in each block to make sure levels across factors are evenly spread across intra-block positions, and to minimize cases in which two or more samples with the same level of the same factor are aquired one after the other.

## Installation

You can install the package using pip:

```bash
pip install blockrand_q_designer
```
Alternatively you can clone the repository and install it locally

```bash
git clone https://github.com/nar-g/blockrand_q_designer.git
cd blockrand_q_designer
pip install .
```

```bash
conda install -c conda-forge blockrand_q_designer
```

## Usage example

A simple example of how to use this tool:

```python

from blockrand_q_designer import LCMSQueueDesign

# Define experimental parameters
factors = ['Fraction', 'Treatment', 'Replicate']
levels = [3, 2, 4]
block_size = 3

# Create a design instance
design = LCMSQueueDesign(factors, levels, block_size, base_name="GN01_01_", starting_index=1)

# Optionally, define labels for better readability
design.labels = {
    "Fraction": ("f1", "f2", "f3"),
    "Treatment": ("Nocodazole", "Control"),
    "Replicate": (1, 2, 3, 4)
}

# Print the generated blocks
design.print_blocks_pretty()

# Save the design to a CSV file
design.save_to_csv("queue_design.csv")

```

## Contributing
Contributions are welcome! 

## License
This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Contact
For questions, suggestions, or feedback, please contact guido.narduzzi@bc.biol.ethz.ch
