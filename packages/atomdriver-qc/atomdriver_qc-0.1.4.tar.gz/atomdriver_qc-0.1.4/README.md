<!--
Copyright 2018-2024 Fragment Contributors
SPDX-License-Identifier: Apache-2.0
-->
# Atom Driver

Glue for all your QC codes.

## Supported Drivers

* [Q-Chem](https://www.q-chem.com)
* [MOPAC](http://openmopac.net)
* [NWChem](https://www.nwchem-sw.org)
* [ORCA](https://orcaforum.kofo.mpg.de/app.php/portal)
* [PySCF](https://pyscf.org)
* [xTB](https://xtb-docs.readthedocs.io/en/latest/contents.html)

## Installing

Atom Driver can be installed using `pip`; however, you must install QC codes yourself.

```sh
# Install confomer
pip install atomdriver-qc
```

### Basic QC Environment

If you would like a handful of QC backends you can start a Conda environment and install xTB and PySCF and install Atom Driver on top of it [^conda]

```sh
# Add conda-forge if you haven't already
conda config --add channels conda-forge

# Create a new environment
conda create -n atomdriver python=3.11 xtb-python xtb pyscf

# Activate 
conda activate atomdriver

# Install Conformer and Atom Driver with pip **see footnote**

# USING SSH
pip install atomdriver-qc

# USING HTTP
pip install atomdriver-qc
```

[^conda]: Strickly speaking Conda and Pip should not be mixed! You can have a relativly stable environment if you install Python and a handful of dependencies with Conda and then install the pip dependencies. Do not go back and add addional Conda packages! You may have to remove and recreate the environment to make changes.

## Quick Start

For simple workflow you can run calculations with the `atomdriver.util.run`. For more complex workflows you may wish to use the `atomdriver.util.Worker` class.

```python
from atomdriver.util import run
from atomdriver.drivers.libxtb import LibxTB
from conformer.systems import System

methanol = System.from_tuples([
    ("C",    0.0000000,   -0.0107162,   -0.6532941),
    ("O",    0.0000000,   -0.0950958,    0.7424134),
    ("H",    0.9153226,    0.5105599,   -1.0084225),
    ("H",   -0.9153226,    0.5105599,   -1.0084225),
    ("H",    0.0000000,   -1.0368018,   -1.0751488),
    ("H",    0.0000000,    0.8407457,    1.0724513),
])
xtb_driver = LibxTB.from_options("xtb", calc_gradient=True, calc_charges=True)
res = run(methanol, xtb_driver)

print(res.status)
# 2 (RecordStatus.COMPLETE)

print(res.properties["total_energy"])
# -8.2243278718041

print(res.properties["partial_charges"].data)
# [[ 0.04554668]
#  [-0.42977159]
#  [ 0.02308721]
#  [ 0.02308721]
#  [ 0.05096463]
#  [ 0.28708585]]

print(res.properties["nuclear_gradient"].data)
# [[-1.52686431e-17  2.45336649e-03  1.26468951e-02]
#  [ 4.99102075e-17 -2.12577019e-02 -9.37319720e-03]
#  [ 9.54169642e-03  3.19852718e-03  4.68753733e-04]
#  [-9.54169642e-03  3.19852718e-03  4.68753733e-04]
#  [ 2.09659150e-17 -1.02904049e-02 -7.39062368e-03]
#  [-6.73798886e-18  2.26976860e-02  3.17941833e-03]]
```

![Yes it's a pun!](https://media.giphy.com/media/IcjQNoFcxRuZVBePw2/giphy.gif?cid=ecf05e47uwcshvap3ad26ivtehhprtbqlau5scu932gwhm7d&ep=v1_gifs_search&rid=giphy.gif&ct=g)