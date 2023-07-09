from django.core.management.base import BaseCommand

# I wrote this code
from django.db.utils import IntegrityError
from api.models import Organism, Protein, Domain, ProteinDomain, OrganismProtein
import pandas as pd
from tqdm import tqdm
# end of code I wrote


class Command(BaseCommand):
    help = "Loads data from CSV file to database"

    def handle(self, *args, **options):

        # I wrote this code
        print("Uploading data...")

        # load from /data: data-seq.csv, dataset.csv, pfam-descriptions.csv
        seq_df = pd.read_csv("data/data-sequences.csv")
        dataset_df = pd.read_csv("data/dataset.csv")
        pfam_df = pd.read_csv("data/pfam-descriptions.csv")

        # process the data into their respective models:

        # all organism data is located in dataset_df
        organism_df = dataset_df[['organism_taxa_id', 'organism_clade_identifier', 'genus_species']].drop_duplicates()
        # rename columns taxa_id, clade_id, genus_species
        organism_df = organism_df.rename(
            columns={
                'organism_taxa_id': 'taxa_id',
                'organism_clade_identifier': 'clade_id',
                'genus_species': 'genus_species'
            }
        )
            

        # majority data is in dataset_df, not all records will have a sequence length
        # we do left join to keep all records that dont have protein sequence length
        protein_df = dataset_df[['protein_id', 'length_of_protein']].drop_duplicates()
        protein_df = protein_df.merge(seq_df, on='protein_id', how='left')
        protein_df = protein_df.drop_duplicates()
        # rename columns protein_id, sequence, length, organism_id  
        protein_df = protein_df.rename(
            columns={
                'length_of_protein': 'length',
                'protein_sequence': 'sequence'
            }
        )


        # most domain data is in dataset_df, but some records are missing domain_pfam_ids
        domain_df = dataset_df[['domain_id']].drop_duplicates() 
        domain_df = domain_df.merge(pfam_df, on='domain_id', how='left')
        domain_df = domain_df.drop_duplicates()
        domain_df = domain_df.rename(
            columns={
                'domain_description': 'description',
            }
        )


        # protein_domain data is in dataset_df
        protein_domain_df = dataset_df[['protein_id', 'domain_id', 'domain_start_coordinate', 'domain_end_coordinate']].drop_duplicates()
        protein_domain_df = protein_domain_df.rename(
            columns={
                'domain_start_coordinate': 'start_coordinate',
                'domain_end_coordinate': 'end_coordinate'
            }
        )   

        # organism_protein data is in dataset_df
        organism_protein_df = dataset_df[['organism_taxa_id', 'protein_id']].drop_duplicates()
        organism_protein_df = organism_protein_df.rename(
            columns={
                'organism_taxa_id': 'taxa_id',
            }
        )

        print("Uploading organisms...")
        for index, row in tqdm(list(organism_df.iterrows())):
            try:
                Organism.objects.create(
                    taxa_id=row['taxa_id'],
                    clade_id=row['clade_id'],
                    genus_species=row['genus_species']
                )
            except IntegrityError:
                print("Organism already exists in database")

        print("Uploading proteins...")
        for index, row in tqdm(list(protein_df.iterrows())):
            try:
                Protein.objects.create(
                    protein_id=row['protein_id'],
                    sequence= row['sequence'] if 'sequence' in row else '',
                    length=row['length'],
                )
            except IntegrityError:
                print("Protein already exists in database")

        print("Uploading domains...")
        for index, row in tqdm(list(domain_df.iterrows())):
            try:
                Domain.objects.create(
                    domain_id=row['domain_id'],
                    description=row['description'] if 'description' in row else '',
                )
            except IntegrityError:
                print("Domain already exists in database")
                print(row['domain_id'], row['description'])

        print("Uploading protein domains...")
        for index, row in tqdm(list(protein_domain_df.iterrows())):
            try:
                protein = Protein.objects.get(protein_id=row['protein_id'])
                domain = Domain.objects.get(domain_id=row['domain_id'])
                ProteinDomain.objects.create(
                    start_coordinate=row['start_coordinate'],
                    end_coordinate=row['end_coordinate'],
                    protein_id=protein,
                    domain_id=domain
                )
            except IntegrityError:
                print("ProteinDomain already exists in database")
            except Protein.DoesNotExist:
                print("Protein : {} does not exist in database".format(row['protein_id']))
            except Domain.DoesNotExist:
                print("Domain : {} does not exist in database".format(row['domain_id']))

        print("Uploading organism proteins...")
        for index, row in tqdm(list(organism_protein_df.iterrows())):
            try:
                taxa = Organism.objects.get(taxa_id=row['taxa_id'])
                protein = Protein.objects.get(protein_id=row['protein_id'])
                OrganismProtein.objects.create(
                    taxa_id=taxa,
                    protein_id=protein
                )
            except IntegrityError:
                print("OrganismProtein already exists in database")
            except Organism.DoesNotExist:
                print("Organism ID: {} does not exist in database".format(row['taxa_id']))
            except Protein.DoesNotExist:
                print("Protein : {} does not exist in database".format(row['protein_id']))


        print("Data upload complete!")
        # end of code I wrote
            