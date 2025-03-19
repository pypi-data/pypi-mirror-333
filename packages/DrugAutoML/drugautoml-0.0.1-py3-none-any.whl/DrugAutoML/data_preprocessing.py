import os
import pandas as pd
from rdkit import Chem
import warnings
import logging
import re

warnings.filterwarnings("ignore", category=RuntimeWarning)
logging.basicConfig(level=logging.INFO)

pd.options.display.max_columns = None
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)

def load_and_prepare_data(file_path, ic50_thresholds):
    """
    Load and prepare data from a CSV file.

    Steps:
      - Read CSV file
      - Clean quotes and whitespace in string columns
      - Validate SMILES strings and canonicalize them
      - Filter records with 'nm' as Standard Units
      - Convert 'Standard Value' to numeric
      - Classify activity based on IC50 thresholds (Active/Inactive/Gray Area)
      - Update response using comments
      - Remove 'Gray Area' records and duplicates
      - Save the final data to "results/preprocessed_data.csv"

    Parameters:
      file_path (str): Path to the input CSV file.
      ic50_thresholds (dict): Dictionary with keys 'lower_cutoff' and 'upper_cutoff'.

    Returns:
      pd.DataFrame: The cleaned and processed DataFrame.
    """
    columns = [
        'Molecule ChEMBL ID',
        'Molecule Name',
        'Smiles',
        'Comment',
        'Standard Type',
        'Standard Units',
        'Standard Relation',
        'Standard Value'
    ]

    data = pd.read_csv(file_path, sep=None, engine='python', usecols=columns)
    print(f"Total molecules read from CSV: {len(data)}")

    # Clean string columns
    data = data.apply(lambda col: col.str.replace('"', '').replace("'", "").str.strip()
                      if col.dtype == 'object' else col)

    data = data.dropna(subset=['Smiles'])
    print(f"Molecules after dropping missing SMILES: {len(data)}")

    data = data[data['Smiles'].apply(lambda x: Chem.MolFromSmiles(x) is not None)]
    print(f"Molecules after removing invalid SMILES: {len(data)}")

    data = data[data['Standard Units'].str.strip().str.lower() == 'nm']
    print(f"Molecules with 'nm' as Standard Units: {len(data)}")

    data['Standard Relation'] = data['Standard Relation'].replace({'>>': '>', '<<': '<'}, regex=False)
    data['Standard Value'] = pd.to_numeric(data['Standard Value'], errors='coerce')
    data = data.dropna(subset=['Standard Value'])
    print(f"Molecules after converting Standard Value to numeric: {len(data)}")

    data['Smiles'] = data['Smiles'].apply(clean_and_standardize_smiles)
    data = data.dropna(subset=['Smiles'])
    print(f"Molecules after SMILES cleaning: {len(data)}")

    data = classify_activity(data, ic50_thresholds)
    data = update_response_with_comments(data)

    data = data[data['Response'] != 'Gray Area'].reset_index(drop=True)
    print(f"Molecules outside of 'Gray Area': {len(data)}")

    data = data.drop_duplicates(subset=['Smiles', 'Molecule ChEMBL ID']).reset_index(drop=True)
    print(f"Molecules after removing duplicates: {len(data)}")

    active_count = (data['Response'] == 'Active').sum()
    inactive_count = (data['Response'] == 'Inactive').sum()
    total = len(data)
    if total > 0:
        print(f"Active molecules: {active_count} ({100 * active_count / total:.2f}%), "
              f"Inactive molecules: {inactive_count} ({100 * inactive_count / total:.2f}%)")
    else:
        print("No molecules left after processing.")

    results_folder = "results"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    output_path = os.path.join(results_folder, "preprocessed_data.csv")
    data.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")

    return data

def classify_activity(df, thresholds):
    df['Response'] = 'Gray Area'
    df.loc[df['Standard Value'] < thresholds['lower_cutoff'], 'Response'] = 'Active'
    df.loc[df['Standard Value'] > thresholds['upper_cutoff'], 'Response'] = 'Inactive'
    return df

def update_response_with_comments(df):
    inactive_terms = ['not active', 'inactive', 'no activity', 'lack of activity', 'failed']
    active_terms = ['active', 'potent', 'good activity']
    inactive_pattern = r'\b(?:' + '|'.join(map(re.escape, inactive_terms)) + r')\b'
    active_pattern = r'\b(?:' + '|'.join(map(re.escape, active_terms)) + r')\b'
    df.loc[df['Comment'].str.contains(inactive_pattern, flags=re.IGNORECASE, na=False), 'Response'] = 'Inactive'
    df.loc[df['Comment'].str.contains(active_pattern, flags=re.IGNORECASE, na=False), 'Response'] = 'Active'
    return df

def clean_and_standardize_smiles(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return None
        largest_frag = max(Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True), key=lambda m: m.GetNumAtoms())
        return Chem.MolToSmiles(largest_frag, canonical=True)
    except Exception as e:
        logging.warning(f"Error cleaning SMILES: {e}")
        return None
