
from django.conf.urls import url
from . import views


"""
POST http://127.0.0.1:8000/api/protein/ - add a new record
GET  http://127.0.0.1:8000/api/protein/[PROTEIN ID] - return the protein sequence and all we know about it
http://127.0.0.1:8000/api/protein/A0A016S8J7 returns

GET  http://127.0.0.1:8000/api/pfam/[PFAM ID] - return the domain and it's deacription
http://127.0.0.1:8000/api/pfam/PF00360 returns

GET  http://127.0.0.1:8000/api/proteins/[TAXA ID] - return a list of all proteins for a given organism
NOTE: "id" here is sequential the primary key value generated by django for the table that holds the domain data
http://127.0.0.1:8000/api/proteins/55661 returns

GET  http://127.0.0.1:8000/api/pfams/[TAXA ID] - return a list of all domains in all the proteins for a given organism.
NOTE: "id" here is sequential the primary key value generated by django for the table that holds the domain data
http://127.0.0.1:8000/api/pfams/55661 returns

GET  http://127.0.0.1:8000/api/coverage/[PROTEIN ID] - return the domain coverage for a given protein. That is Sum of the protein domain lengths (start-stop)/length of protein.
http://127.0.0.1:8000/api/coverage/A0A016S8J7 returns
coverage:	0.693069306930693
"""

urlpatterns = [
    url("protein/", views.protein, name="protein"),
    url("proteins/", views.proteins, name="proteins"),
    url("pfam/", views.pfam, name="pfam"),
    url("pfams/", views.pfams, name="pfams"),
    url("coverage/", views.coverage, name="coverage"),
