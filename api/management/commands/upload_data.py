from django.core.management.base import BaseCommand

# I wrote this code
from django.db.utils import IntegrityError
from api.models import Organism, Protein, Domain
import pandas as pd
# end of code I wrote


class Command(BaseCommand):
    help = "Loads data from CSV file to database"

    def handle(self, *args, **options):

        # I wrote this code
        print("uploading data...")

        # load data from csv files:
        seq_df = pd.read_csv("data/data-sequences.csv")
        dataset_df = pd.read_csv("data/dataset.csv")
        pfam_df = pd.read_csv("data/pfam-descriptions.csv")

        # upload data to the database:
        for index, row in dataset_df.iterrows():

            try:
                organism, _ = Organism.objects.get_or_create(
                    tax_id=row["taxa_id"],
                    clade=row["clade"],
                    scientific_name=row["scientific_name"]
                )

                protein_seq = seq_df.loc[seq_df["protein_id"] == row["protein_id"]]
                protein, _ = Protein.objects.get_or_create(
                    protein_id=row["protein_id"],
                    sequence=protein_seq.iloc[0]["sequence"] if not protein_seq.empty else '',
                    length=row["protein_length"],
                    organism=organism
                )

                pfam = pfam_df.loc[pfam_df["pfam_id"] == row["pfam_id"]]
                domain, _ = Domain.objects.get_or_create(
                    domain_id=row["pfam_id"],
                    description=pfam.iloc[0]["description"] if not pfam.empty else '',
                    start_coord=row["start"],
                    end_coord=row["end"],
                    protein=protein
                )

            except IntegrityError as e:
                print(f"Integrity error on row {index}, data {row}. Exception: {e}")
                continue

            except Exception as e:
                print(f"Error on row {index}, data {row}. Exception: {e}")
                continue

        print("Data upload complete.")

        # end of code I wrote