# I wrote this code
from rest_framework import serializers
from .models import Protein, Domain, ProteinDomain, Organism, OrganismProtein


class CreateProteinSerializer(serializers.Serializer):
    protein_id = serializers.CharField(max_length=200)
    sequence = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    length = serializers.IntegerField(required=False)
    taxonomy = serializers.JSONField(required=False)
    domains = serializers.ListField(child=serializers.DictField(), required=False)

    def create(self, validated_data):
        taxa_data = validated_data.pop('taxonomy', None)
        domains_data = validated_data.pop('domains', None)

        protein = Protein.objects.create(**validated_data)

        if taxa_data:
            organism, _ = Organism.objects.get_or_create(
                taxa_id=taxa_data.get('taxa_id'),
                defaults={'genus_species': f"{taxa_data.get('genus')} {taxa_data.get('species')}", 'clade_id': taxa_data.get('clade')}
            )
            OrganismProtein.objects.create(taxa_id=organism, protein_id=protein)

        if domains_data:
            for domain in domains_data:
                pfam_data = domain.pop('pfam_id')
                domain_instance, _ = Domain.objects.get_or_create(
                    domain_id=pfam_data.get('domain_id'),
                    defaults={'description': pfam_data.get('domain_description')}
                )

                ProteinDomain.objects.create(
                    protein_id=protein, 
                    domain_id=domain_instance,
                    start_coordinate=domain.get('start'),
                    end_coordinate=domain.get('stop')
                )

        return protein

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
