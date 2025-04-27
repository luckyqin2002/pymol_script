from pymol import cmd
import os
import glob

'''
--------------------------
Usage Instructions:
--------------------------

1. Load this script into PyMOL, for example:
   PyMOL> run path/to/this_script.py

2. Initialize the session by specifying the relax directory and the native structure:
   PyMOL> load_batch_pdb_with_fixed_native(relax_dir="/path/to/relax", native_path="/path/to/native.pdb", chain="A", delete_all=True, backbone_only=False)

   Arguments:
     - relax_dir: Folder containing relaxed PDB models.
     - native_path: Path to the native PDB file.
     - chain: Chain ID used for alignment (default: "A").
     - delete_all: Whether to clear all objects before loading (default: True).
     - backbone_only: If True, alignment is based on C-alpha atoms only.

3. To load the next relax structure:
   PyMOL> load_next_with_fixed_native()

4. To load the previous relax structure:
   PyMOL> load_previous_with_fixed_native()

Notes:
- Native structure will be loaded once and fixed throughout browsing.
- Only the relax model is deleted and replaced when switching structures.
- Alignment RMSD will be printed in the console after each load.
'''


# Global states
POINTER = -1
LOADLIST = []
RELAX_DIR = ""
NATIVE_PATH = ""
CHAIN = "A"
BACKBONE_ONLY = False
NATIVE_LOADED = False

def load_batch_pdb_with_fixed_native(relax_dir, native_path, chain="A", delete_all=True, backbone_only=False):
    """
    Initialize loading:
    - Load all relax PDB files from the specified directory
    - Set the native structure
    - Specify chain for alignment
    - Choose whether to align using backbone atoms only
    """
    global POINTER, LOADLIST, RELAX_DIR, NATIVE_PATH, CHAIN, BACKBONE_ONLY, NATIVE_LOADED

    if delete_all:
        cmd.delete('all')

    pattern = os.path.join(relax_dir, "*.pdb")
    relax_files = sorted(glob.glob(pattern))

    if not relax_files:
        print(f"No relax PDB files found in {relax_dir}")
        return

    LOADLIST = [(os.path.basename(p), relax_dir) for p in relax_files]
    RELAX_DIR = relax_dir
    NATIVE_PATH = native_path
    CHAIN = chain
    BACKBONE_ONLY = backbone_only
    POINTER = -1
    NATIVE_LOADED = False

    load_next_with_fixed_native()

def load_next_with_fixed_native():
    """
    Load the next relax structure and align to the fixed native structure.
    Only delete the previously loaded relax structure, keep native loaded.
    """
    global POINTER, LOADLIST, RELAX_DIR, NATIVE_PATH, CHAIN, BACKBONE_ONLY, NATIVE_LOADED

    if POINTER >= len(LOADLIST) - 1:
        print("No more relax structures.")
        return

    if POINTER >= 0:
        relax_name, _ = LOADLIST[POINTER]
        relax_obj = os.path.splitext(relax_name)[0]
        cmd.delete(relax_obj)

    POINTER += 1
    relax_tag, relax_dir = LOADLIST[POINTER]
    relax_path = os.path.join(relax_dir, relax_tag)
    relax_obj = os.path.splitext(relax_tag)[0]

    print(f"Loading relax structure: {relax_tag}")

    if not NATIVE_LOADED:
        print(f"Loading fixed native structure: {NATIVE_PATH}")
        cmd.load(NATIVE_PATH, "native")
        NATIVE_LOADED = True

    cmd.load(relax_path, relax_obj)

    if BACKBONE_ONLY:
        mobile_selection = f"{relax_obj} and chain {CHAIN} and name CA"
        target_selection = f"native and chain {CHAIN} and name CA"
    else:
        mobile_selection = f"{relax_obj} and chain {CHAIN}"
        target_selection = f"native and chain {CHAIN}"

    rmsd = cmd.align(mobile_selection, target_selection)[0]
    print(f"Alignment RMSD (chain {CHAIN}): {rmsd:.3f} Å")

    cmd.zoom()

def load_previous_with_fixed_native():
    """
    Load the previous relax structure and align to the fixed native structure.
    """
    global POINTER, LOADLIST, RELAX_DIR, NATIVE_PATH, CHAIN, BACKBONE_ONLY, NATIVE_LOADED

    if POINTER <= 0:
        print("Already at the first relax structure.")
        return

    relax_name, _ = LOADLIST[POINTER]
    relax_obj = os.path.splitext(relax_name)[0]
    cmd.delete(relax_obj)

    POINTER -= 1
    relax_tag, relax_dir = LOADLIST[POINTER]
    relax_path = os.path.join(relax_dir, relax_tag)
    relax_obj = os.path.splitext(relax_tag)[0]

    print(f"Loading relax structure: {relax_tag}")

    cmd.load(relax_path, relax_obj)

    if BACKBONE_ONLY:
        mobile_selection = f"{relax_obj} and chain {CHAIN} and name CA"
        target_selection = f"native and chain {CHAIN} and name CA"
    else:
        mobile_selection = f"{relax_obj} and chain {CHAIN}"
        target_selection = f"native and chain {CHAIN}"

    rmsd = cmd.align(mobile_selection, target_selection)[0]
    print(f"Alignment RMSD (chain {CHAIN}): {rmsd:.3f} Å")

    cmd.zoom()

# Register as PyMOL commands
cmd.extend('load_batch_pdb_with_fixed_native', load_batch_pdb_with_fixed_native)
cmd.extend('load_next_with_fixed_native', load_next_with_fixed_native)
cmd.extend('load_previous_with_fixed_native', load_previous_with_fixed_native)

