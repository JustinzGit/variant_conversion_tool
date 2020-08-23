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


    @classmethod
    def genomic_information(cls, transcript_id, nt_position):
        """
        Use ensemble API to genomic information (hg38)
        http://europepmc.org/article/MED/25236461?singleResult=true
        """
        
        # Request genomic information 
        request = f"https://rest.ensembl.org/map/cds/{transcript_id}/{nt_position}..{nt_position}"
        response = requests.get(request, headers={ "Content-Type" : "application/json"})

        # Convert string to JSON object
        response = response.json()
    
        return {
            "chromosome": repr(response["mappings"][0]["seq_region_name"]).replace("'",""),
            "gdna_location": repr(response["mappings"][0]["start"]),
            "assembly": repr(response["mappings"][0]["assembly_name"]),
            "strand": repr(response["mappings"][0]["strand"])
        }