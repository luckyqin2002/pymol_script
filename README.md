# PyMOL Scripts Collection

This repository contains a set of utility scripts designed to assist protein structure visualization and analysis tasks in PyMOL.

## Scripts

### 1. color_by_residue_type.py
- **Purpose**: 
  Color amino acid residues based on their chemical properties (hydrophobic, polar, positively charged, negatively charged).
- **Usage**:
  - Load the script in PyMOL:
    ```
    run path/to/color_by_residue_type.py
    ```
  - Apply coloring to a structure:
    ```
    color_by_residue_type selection
    ```
  - Default target: `all`.

---

### 2. find-target-sesq.py
- **Purpose**:
  Identify and locate specific target residues or motifs within protein sequences.
- **Usage**:
  - Designed to parse input sequences and find specified patterns.
  - Detailed usage instructions can be added after script customization.

---

### 3. load_batch_pdb_py3.py
- **Purpose**:
  Load a batch of relaxed PDB models and align each to a fixed native structure for comparative analysis.
- **Usage**:
  - Load the script in PyMOL:
    ```
    run path/to/load_batch_pdb_py3.py
    ```
  - Initialize batch loading:
    ```
    load_batch_pdb_with_fixed_native(relax_dir="/path/to/relax", native_path="/path/to/native.pdb", chain="A", delete_all=True, backbone_only=False)
    ```
  - Browse through models:
    ```
    load_next_with_fixed_native()
    load_previous_with_fixed_native()
    ```

---

## Requirements
- PyMOL 2.x or newer
- Python 3 environment

## License
This project is licensed under the MIT License.

## Author
LuckyQin (luckyqin2002)
