# I wrote this code

from rest_framework import generics
from .models import Protein, Domain, ProteinDomain, Organism, OrganismProtein
from .serializers import (ProteinSerializer, OrganismProteinSerializer, CoverageSerializer,
    PfamSerializer, ProteinDomainForOrganismSerializer, CreateProteinSerializer)
from django.db.models import Sum, F
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateProteinView(generics.CreateAPIView):
    queryset = Protein.objects.all()
    serializer_class = CreateProteinSerializer


class ProteinView(generics.RetrieveAPIView):
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer
    lookup_field = 'protein_id'


class PfamView(generics.RetrieveAPIView):
    queryset = Domain.objects.all()
    serializer_class = PfamSerializer
    lookup_field = 'domain_id'


class ProteinByOrganismView(generics.ListAPIView):
    serializer_class = OrganismProteinSerializer

    def get_queryset(self):
        taxa_id = self.kwargs['taxa_id']
        return OrganismProtein.objects.filter(taxa_id=taxa_id)


class PfamsByOrganismView(generics.ListAPIView):
    serializer_class = ProteinDomainForOrganismSerializer

    def get_queryset(self):
        taxa_id = self.kwargs['taxa_id']
        proteins = OrganismProtein.objects.filter(taxa_id=taxa_id).values('protein_id')
        return ProteinDomain.objects.filter(protein_id__in=proteins)


class CoverageView(APIView):
    serializer_class = CoverageSerializer

    def get(self, request, *args, **kwargs):
        protein_id = self.kwargs['protein_id']

        coverage_data = ProteinDomain.objects.filter(
            protein_id=protein_id
        ).annotate(
            length=F('end_coordinate') - F('start_coordinate')
        ).aggregate(total_length=Sum('length'))

        protein_length = Protein.objects.get(protein_id=protein_id).length
        coverage = round(coverage_data['total_length'] / protein_length, 2) if protein_length else 0
        serializer = self.serializer_class({'coverage': coverage})
        return Response(serializer.data)

# end of code I wrote