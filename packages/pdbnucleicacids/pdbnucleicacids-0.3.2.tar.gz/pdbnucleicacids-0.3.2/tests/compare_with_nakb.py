import sqlite3
import pandas as pd

from Bio.PDB.PDBList import PDBList
from Bio.PDB.MMCIFParser import MMCIFParser
from PDBNucleicAcids.NucleicAcid import NABuilder, DSNABuilder


def query_polymers(db_filepath):
    # Creare una connessione al database SQLite
    conn = sqlite3.connect(db_filepath)

    # Creare un cursore
    cur = conn.cursor()

    # Eseguire una query
    cur.execute(
        """
        SELECT id, entity_id, auth_chain_id, description, sequence
        FROM Polymers WHERE polymer_type = 'DNA'
    """
    )

    # Risultati della query sotto forma di DataFrame
    data = cur.fetchall()
    df = pd.DataFrame(
        data,
        columns=[
            "id",
            "entity_id",
            "auth_chain_id",
            "description",
            "nakb_sequence",
        ],
    )

    # Chiudi la connessione
    conn.close()

    return df


def extract_my_seq(row):
    pdb_id = row["id"].lower()
    auth_chain_id = row["auth_chain_id"]

    filepath = (
        f"../tf-dna-sqlite/data/structures/assemblies/{pdb_id}-assembly1.cif"
    )

    structure = PARSER.get_structure("id", filepath)

    for chain_id in auth_chain_id.split(","):
        try:
            chain = structure[0][chain_id]
        except KeyError:
            continue
        na_list = BUILDER.build_nucleic_acids(chain)
        na = na_list[0]
        return " ".join([res.resname for res in na])
    return None


PARSER = MMCIFParser(QUIET=True)
BUILDER = NABuilder()

db_filepath = "../tf-dna-sqlite/db/tf-dna-sqlite.db"

df = query_polymers(db_filepath)
df["nakb_sequence"] = df["nakb_sequence"].apply(
    lambda x: "".join([i for i in x if i != " "])
)

df["nakb_sequence"] = df["nakb_sequence"].apply(
    lambda x: " ".join(x.split(")("))
)

df["nakb_sequence"] = df["nakb_sequence"].apply(lambda x: x[1:-1])

# comment out because takes a lot of time
# df["extracted_sequence"] = df.apply(extract_my_seq, axis=1)

filepath = "tests/data/compare_with_nakb.csv"
df = pd.read_csv(filepath, index_col=0, header=0)

df["is_equal"] = df.apply(
    lambda row: row["nakb_sequence"] == row["extracted_sequence"], axis=1
)

df1 = df[~df["is_equal"]]

df2 = df[df["extracted_sequence"].isna()]

df.to_csv(filepath)


# %% check structures from df2

pdb_id = "1FJL".lower()

pdbl = PDBList()
pdbl.retrieve_assembly_file(pdb_code=pdb_id, assembly_num=1, pdir=".")

filepath = f"{pdb_id}-assembly1.cif"
structure = PARSER.get_structure(pdb_id, filepath)
print([chain.id for chain in structure[0]])  # these are not in the assembly

# a quanto ho capito è una roba che ha a che fare con la assebly
# forse dovrei provarlo con le unità asimmetriche


# %% check structures from df1

pdb_id = "1BY4".lower()

pdbl = PDBList()
pdbl.retrieve_assembly_file(pdb_code=pdb_id, assembly_num=1, pdir=".")

filepath = f"{pdb_id}-assembly1.cif"
structure = PARSER.get_structure(pdb_id, filepath)
print([chain.id for chain in structure[0]])  # these are not in the assembly

na_list = BUILDER.build_nucleic_acids(structure)

# sembra che la assembly non rispetti la simmetria ??
# per esempio, ci sono due dsDNA che dovrebbero essere simmetrici
# ma uno di questi ha un nucleotide in più

# 1IF1
pdb_id = "1IF1".lower()

pdbl = PDBList()
pdbl.retrieve_assembly_file(pdb_code=pdb_id, assembly_num=1, pdir=".")

filepath = f"{pdb_id}-assembly1.cif"
structure = PARSER.get_structure(pdb_id, filepath)

builder = DSNABuilder()
dsna_list = builder.build_double_strands(structure)
