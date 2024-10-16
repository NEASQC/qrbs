# Quantum Rule-Based System (QRBS) software library

This is the repository for the Quantum Rule-Based System (QRBS) library of NEASQC project (WP6). Quantum Rule-Based Systems (QRBS) are defined as those Rule-Based Systems (RBS) that use the formalism of Quantum Computing (QC) for representing knowledge and for making inferences. Inaccurate knowledge is one of the fundamental problems of AI. In particular, it is one of the essential problems of RBS, and at the same time one of the most complex to deal with. We propose the use of QRBS to model this inaccurate knowledge and manage it.

## Licence

The `LICENCE` file contains the default licence statement as specified in the proposal and partner agreement.

## Building and installing

For simplicity, an example of `setup.py` file is provided in this template.

## Repository structure

The _neasqc_qrbs_ package is structured in two main modules:

- **knowledge_rep**: conformed by the classes that allow us to encode knowledge into the system.
- **qrbs**: conformed by the classes that manage the encoded knowledge and extract utility from it.

## Jupyter Notebooks

A series of Jupyter notebooks have been developed in the misc/notebooks directory as tutorials. These notebooks explain the functionality of the various packages and modules within the library, as well as demonstrate how to utilize them to model RBSs and manage inaccurate knowledge with them.

These notebooks provide extra functionalities beyond those offered by the _neasqc_qrbs_ package, and their source can be found under the misc/ directoy.

## Documentation

The documentation for this software can be accessed at: https://neasqc.github.io/qrbs
