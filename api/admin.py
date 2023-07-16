from django.contrib import admin
from .models import * 

admin.site.register(Organism)
admin.site.register(Protein)
admin.site.register(Domain)
admin.site.register(ProteinDomain)
admin.site.register(OrganismProtein)


# Register your models here.
