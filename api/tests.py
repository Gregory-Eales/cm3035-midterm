from django.test import TestCase, Client
from django.urls import reverse
from .models import Protein, Domain, ProteinDomain, Organism, OrganismProtein
from .serializers import ProteinSerializer, PfamSerializer
from rest_framework import status
from rest_framework.test import APIClient

class ProteinAPITestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.organism = Organism.objects.create(
            taxa_id=53326, 
            clade_id="E", 
            genus_species="Ancylostoma ceylanicum"
        )

        self.protein = Protein.objects.create(
            protein_id="A0A016S8J7", 
            sequence="MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA", 
            length=101
        )

        self.organismProtein = OrganismProtein.objects.create(
            taxa_id=self.organism,
            protein_id=self.protein
        )

        self.domain1 = Domain.objects.create(
            domain_id="PF01650", 
            description="Peptidase C13 legumain"
        )

        self.domain2 = Domain.objects.create(
            domain_id="PF02931", 
            description="Neurotransmitter-gated ion-channel ligand-binding domain"
        )

        self.proteinDomain1 = ProteinDomain.objects.create(
            start_coordinate=40, 
            end_coordinate=94, 
            protein_id=self.protein, 
            domain_id=self.domain1
        )

        self.proteinDomain2 = ProteinDomain.objects.create(
            start_coordinate=23, 
            end_coordinate=39, 
            protein_id=self.protein, 
            domain_id=self.domain2
        )

    def test_get_protein(self):
        response = self.client.get(reverse('protein_id', kwargs={'protein_id': self.protein.protein_id}))
        
        protein_serializer_data = ProteinSerializer(instance=self.protein).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, protein_serializer_data)

class PfamTestCase(TestCase):
    """ Test module for Pfam GET """

    def setUp(self):
        self.client = Client()
        self.pfam = Domain.objects.create(
            domain_id="PF00360", description="Phytochromeregion"
        )
        self.valid_payload = {
            "domain_id": "PF00360",
            "domain_description": "Phytochromeregion"
        }
        self.url = reverse('pfam', kwargs={'domain_id': self.pfam.domain_id})

    def test_valid_pfam_get(self):
        response = self.client.get(self.url)
        pfam = Domain.objects.get(domain_id=self.valid_payload['domain_id'])
        serializer = PfamSerializer(pfam)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProteinByOrganismView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.organism = Organism.objects.create(taxa_id=55661, clade_id=1111, genus_species='Example Name')
        self.protein1 = Protein.objects.create(protein_id="A0A091FY39", sequence="SEQUENCE1", length=1000)
        self.protein2 = Protein.objects.create(protein_id="A0A091FMY9", sequence="SEQUENCE2", length=1000)
        self.organism_protein1 = OrganismProtein.objects.create(taxa_id=self.organism, protein_id=self.protein1)
        self.organism_protein2 = OrganismProtein.objects.create(taxa_id=self.organism, protein_id=self.protein2)

    def test_get_proteins_list_by_organism(self):
        """
        This test ensures that proteins for the specified organism exist and
        return with status 200 and correct content when accessed via the API
        endpoint.
        """
        response = self.client.get(reverse('proteins', kwargs={'taxa_id': self.organism.taxa_id}))
        expected_data = [
            {
                "id": self.organism_protein1.id,
                "protein_id": "A0A091FY39"
            },
            {
                "id": self.organism_protein2.id,
                "protein_id": "A0A091FMY9"
            },
        ]
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.json(), expected_data)


class TestPfamsByOrganismView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.organism = Organism.objects.create(taxa_id=55661, clade_id=1111, genus_species='Example Name')

        self.protein1 = Protein.objects.create(protein_id="A0A091FY39", sequence="SEQUENCE1", length=1000)
        self.protein2 = Protein.objects.create(protein_id="A0A091FMY9", sequence="SEQUENCE2", length=1000)

        self.organism_protein1 = OrganismProtein.objects.create(taxa_id=self.organism, protein_id=self.protein1)
        self.organism_protein2 = OrganismProtein.objects.create(taxa_id=self.organism, protein_id=self.protein2)

        self.domain1 = Domain.objects.create(domain_id="mobidb-lite", description="disorder prediction")
        self.domain2 = Domain.objects.create(domain_id="PF00307", description="Calponin homology (CH) domain")

        self.protein_domain1 = ProteinDomain.objects.create(protein_id=self.protein1, 
                                                            domain_id=self.domain1, 
                                                            start_coordinate=1, 
                                                            end_coordinate=100)
        self.protein_domain2 = ProteinDomain.objects.create(protein_id=self.protein2, 
                                                            domain_id=self.domain2, 
                                                            start_coordinate=101, 
                                                            end_coordinate=200)

    def test_get_pfams_by_organism(self):
        """
        This test ensures that protein domains for the specified organism exist and
        return with status 200 and correct content when accessed via the API endpoint.
        """
        response = self.client.get(reverse('pfams', kwargs={'taxa_id': self.organism.taxa_id}))

        expected_data = [
            {
                "id": self.protein_domain1.id,
                "pfam_id": {
                    "domain_id": "mobidb-lite",
                    "domain_description": "disorder prediction"
                }
            },
            {
                "id": self.protein_domain2.id,
                "pfam_id": {
                    "domain_id": "PF00307",
                    "domain_description": "Calponin homology (CH) domain"
                }
            },
        ]

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.json(), expected_data)


class TestCoverageView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.protein = Protein.objects.create(protein_id="A0A016S8J7", sequence="SEQUENCE1", length=101)

        self.domain1 = Domain.objects.create(domain_id="PF00111", description="Protein kinase domain")
        self.domain2 = Domain.objects.create(domain_id="PF00228", description="Adenylate and Guanylate kinase catalytic domain")

        ProteinDomain.objects.create(protein_id=self.protein, domain_id=self.domain1, start_coordinate=10, end_coordinate=30)
        ProteinDomain.objects.create(protein_id=self.protein, domain_id=self.domain2, start_coordinate=40, end_coordinate=70)

    def test_get_coverage(self):
        """
        This test ensures that the correct coverage for a given protein is
        returned when accessing via the API endpoint.
        """
        response = self.client.get(reverse('coverage', kwargs={'protein_id': self.protein.protein_id}))

        expected_data = {'coverage': 0.5}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_data)