# I wrote this code
from rest_framework import serializers
from .models import Protein, Domain, ProteinDomain, Organism, OrganismProtein


class ProteinSerializer(serializers.ModelSerializer):
    taxonomy = serializers.SerializerMethodField()
    domains = serializers.SerializerMethodField()

    class Meta:
        model = Protein
        fields = ('protein_id', 'sequence', 'length', 'taxonomy', 'domains')

    def get_taxonomy(self, obj):
        organism = obj.organismprotein_set.first().taxa_id
        return OrganismSerializer(organism).data

    def get_domains(self, obj):
        protein_domains = obj.proteindomain_set.all()
        return ProteinDomainSerializer(protein_domains, many=True).data


class PfamSerializer(serializers.ModelSerializer):
    domain_description = serializers.CharField(source='description')

    class Meta:
        model = Domain
        fields = ('domain_id', 'domain_description')


class OrganismSerializer(serializers.ModelSerializer):
    genus = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()

    class Meta:
        model = Organism
        fields = ('taxa_id', 'clade_id', 'genus', 'species')

    def get_genus(self, obj):
        return obj.genus_species.split()[0]

    def get_species(self, obj):
        return obj.genus_species.split()[1] if len(obj.genus_species.split()) > 1 else ''


class DomainSerializer(serializers.ModelSerializer):
    pfam_id = serializers.SerializerMethodField()

    class Meta:
        model = Domain
        fields = ('pfam_id', 'description')

    def get_pfam_id(self, obj):
        return {
            'domain_id': obj.domain_id,
            'domain_description': obj.description
        }

class OrganismProteinSerializer(serializers.ModelSerializer):
    protein_id = serializers.SlugRelatedField(read_only=True, slug_field='protein_id')

    class Meta:
        model = OrganismProtein
        fields = ['id', 'protein_id']


class ProteinDomainSerializer(serializers.ModelSerializer):
    domain_id = DomainSerializer()
    
    class Meta:
        model = ProteinDomain
        fields = ('start_coordinate', 'end_coordinate', 'domain_id')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        pfam_data = representation.pop('domain_id')
        pfam_data.update({
            'start': representation.pop('start_coordinate'),
            'stop': representation.pop('end_coordinate'),
        })
        return pfam_data


class DomainSerializerTwo(serializers.ModelSerializer):

    class Meta:
        model = Domain
        fields = ('domain_id', 'description')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {
            "domain_id": rep['domain_id'],
            "domain_description": rep['description']
        }

class ProteinDomainForOrganismSerializer(serializers.ModelSerializer):
    pfam_id = DomainSerializerTwo(source='domain_id')

    class Meta:
        model = ProteinDomain
        fields = ['id', 'pfam_id']


class CoverageSerializer(serializers.Serializer):
    coverage = serializers.FloatField()
# end of code I wrote
