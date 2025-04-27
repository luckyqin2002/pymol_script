from pymol import cmd

def color_by_residue_type(selection='all'):
    """
    Color residues based on their chemical properties:
    - Hydrophobic residues: red
    - Polar residues: magenta
    - Negatively charged residues: green
    - Positively charged residues: blue

    Parameters:
    selection (str): Target selection in PyMOL to apply coloring. Default is 'all'.
    """

    # Define residue groups
    hydrophobic = ['ALA', 'VAL', 'ILE', 'LEU', 'MET', 'PHE', 'TRP', 'PRO', 'GLY']
    polar = ['SER', 'THR', 'CYS', 'TYR', 'ASN', 'GLN']
    negative = ['ASP', 'GLU']
    positive = ['LYS', 'ARG', 'HIS']

    # Define colors for each group
    colors = {
        'hydrophobic': 'red',
        'polar': 'magenta',
        'negative': 'green',
        'positive': 'blue'
    }

    # Group dictionary
    groups = {
        'hydrophobic': hydrophobic,
        'polar': polar,
        'negative': negative,
        'positive': positive
    }

    # Apply coloring
    for group_name, residues in groups.items():
        temp_selection_name = f'_temp_{group_name}'
        residue_query = ' or '.join([f'resname {res}' for res in residues])
        full_selection = f'({selection}) and ({residue_query})'
        
        cmd.select(temp_selection_name, full_selection)
        cmd.color(colors[group_name], temp_selection_name)
        cmd.delete(temp_selection_name)

    # Deselect everything at the end
    cmd.deselect()

# Register the function as a PyMOL command
cmd.extend('color_by_residue_type', color_by_residue_type)
