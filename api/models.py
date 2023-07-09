from django.db import models

# Create your models here.

# I wrote this code


class Organism(models.Model):
    taxa_id = models.IntegerField(primary_key=True)
    clade_id = models.TextField(blank=True)
    genus_species = models.TextField()


class Protein(models.Model):
    protein_id = models.CharField(max_length=200, primary_key=True)
    sequence = models.TextField(blank=True)
    length = models.IntegerField()


class Domain(models.Model):
    domain_id = models.CharField(max_length=200, primary_key=True)
    description = models.TextField()


class ProteinDomain(models.Model):

    domain_id = models.ForeignKey(Domain, on_delete=models.CASCADE)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)
    start_coordinate = models.IntegerField()
    end_coordinate = models.IntegerField()

    # make domain_id and protein_id indexed
    class Meta:
        indexes = [
            models.Index(fields=['domain_id', 'protein_id'])
        ]
    

class OrganismProtein(models.Model):
    taxa_id = models.ForeignKey(Organism, on_delete=models.CASCADE)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)

    # make taxa_id and protein_id indexed
    class Meta:
        indexes = [
            models.Index(fields=['taxa_id', 'protein_id'])
        ]
    
# end of code I wrote