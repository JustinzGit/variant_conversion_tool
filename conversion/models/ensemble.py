from django.db import models

class Ensemble(models.Model):
    @classmethod
    def gene_id(cls, gene_name):
        """
        Use ensemble API to obtain ensemble gene ID 
        http://europepmc.org/article/MED/25236461?singleResult=true
        """

        # Request gene information
        request = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene_name}?expand=1"
        response = requests.get(request, headers={ "Content-Type" : "application/json"})

        # Convert string to JSON object
        response = response.json()

        # Obtain Ensembl gene ID
        return repr(response["id"]).replace("'","")

    @classmethod
    def transcript_id(cls, gene_id):
        """
        Use ensemble API to obtain transcript ID 
        http://europepmc.org/article/MED/25236461?singleResult=true
        """

        # Request gene information 
        request = f"https://rest.ensembl.org/lookup/id/{gene_id}?expand=1"
        response = requests.get(request, headers={ "Content-Type" : "application/json"})

        # Convert string to JSON object
        response = response.json()

        # Obtain the first transcript ID of acquired gene ID
        return repr(response["Transcript"][0]["id"]).replace("'","")