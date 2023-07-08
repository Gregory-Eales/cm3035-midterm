from django.db import models

# Create your models here.

# I wrote this code


class Organism(models.Model):
    tax_id = models.IntegerField(primary_key=True)
    clade = models.TextField(blank=True)
    scientific_name = models.TextField()


class Protein(models.Model):
    protein_id = models.CharField(max_length=200, primary_key=True)
    sequence = models.TextField(blank=True)
    length = models.IntegerField()
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE)


class Domain(models.Model):
    domain_id = models.CharField(max_length=200, primary_key=True)
    description = models.TextField()
    start_coordinate = models.IntegerField()
    end_coordinate = models.IntegerField()
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)


# end of code I wrote