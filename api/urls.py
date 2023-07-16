from django.urls import path
from .views import ProteinView, CreateProteinView, PfamView, ProteinByOrganismView, PfamsByOrganismView, CoverageView

urlpatterns = [
    # I wrote this code
    path('protein/', CreateProteinView.as_view(), name='protein'),
    path('protein/<str:protein_id>', ProteinView.as_view(), name='protein_id'), # works
    path('pfam/<str:domain_id>', PfamView.as_view(), name='pfam'), # 
    path('proteins/<int:taxa_id>', ProteinByOrganismView.as_view(), name='proteins'),
    path('pfams/<int:taxa_id>', PfamsByOrganismView.as_view(), name='pfams'),
    path('coverage/<str:protein_id>', CoverageView.as_view(), name='coverage'),
    # end of code I wrote
]