from django.db import models


class Organism(models.Model):
    genus_name = models.CharField(max_length=255)
    species_name = models.CharField(max_length=255)


class Protein(models.Model):
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE)
    protein_sequence = models.TextField()


class Domain(models.Model):
    domain_description = models.TextField()


class ProteinDomain(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    start_coordinate = models.IntegerField()
    end_coordinate = models.IntegerField()
