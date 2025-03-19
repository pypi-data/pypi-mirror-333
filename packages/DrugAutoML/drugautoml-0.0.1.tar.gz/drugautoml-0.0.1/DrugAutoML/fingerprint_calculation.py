import os
import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator

def get_fingerprint(mol):
    """
    Generates a Morgan (ECFP4, 2048-bit) fingerprint for the given molecule using
    rdFingerprintGenerator.
    """
    # Explicitly pass the required parameters:
    # radius = 2, countSimulation=False, includeChirality=False,
    # useBondTypes=True, onlyNonzeroInvariants=False, includeRingMembership=True,
    # countBounds=None, fpSize=2048.
    generator = rdFingerprintGenerator.GetMorganGenerator(
        2,                # radius
        False,            # countSimulation
        False,            # includeChirality
        True,             # useBondTypes
        False,            # onlyNonzeroInvariants
        True,             # includeRingMembership
        None,             # countBounds
        2048              # fpSize
    )
    fp = generator.GetFingerprint(mol)
    return list(fp)

def smiles_to_fingerprints(df, smiles_col='Smiles'):
    """
    Calculates the Morgan (ECFP4, 2048-bit) fingerprint for each SMILES string in a DataFrame
    using rdFingerprintGenerator to avoid deprecation warnings.

    Parameters:
      df (pd.DataFrame): Input DataFrame containing SMILES strings.
      smiles_col (str): Column name with SMILES.

    Returns:
      pd.DataFrame: DataFrame with SMILES and calculated ECFP4 fingerprints.
    """
    fingerprints = []
    for index, row in df.iterrows():
        smiles = row[smiles_col]
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            print(f"Error: Invalid SMILES {smiles} (row {index})")
            continue
        bit_list = get_fingerprint(mol)
        fingerprint_data = [smiles] + bit_list
        column_names = ["Smiles"] + [f"ECFP{i + 1}" for i in range(len(bit_list))]
        fingerprints.append(fingerprint_data)

    fingerprint_df = pd.DataFrame(fingerprints, columns=column_names)

    results_folder = "results"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    output_path = os.path.join(results_folder, "fingerprint_data.csv")
    fingerprint_df.to_csv(output_path, index=False)
    print(f"Fingerprint data saved to {output_path}")

    return fingerprint_df
