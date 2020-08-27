import requests
from django.db import models

class Gnomad(models.Model):

    @classmethod
    def gnomad_data(cls, variant_id):
        """
        Returns gnomAD data for provided variant (v2_1 data set (GRCh37))
        """

        query = """{{
            variant(dataset: gnomad_r2_1, variantId: "{variant_id}"){{
            genome {{
                ac
                an
                ac_hom
            populations{{
                id
                ac
                an
                ac_hom
            }}
            }}
            exome {{
                ac
                an
                ac_hom
            populations{{
                id
                ac
                an
                ac_hom
            }}
            }}
        }}
        }}"""

        query = query.format(variant_id=variant_id)

        # Request data from gnomad
        response = requests.post("https://gnomad.broadinstitute.org/api", json={'query': query}) 

        # Convert string to JSON object
        response = response.json()

        data_source = ["genome", "exome"]
        gnomad_data = {}
        gnomad_data[variant_id] = {}
        
        # Collect both genome and exome data 
        for source in data_source:
            key = source
            if response["errors"]:
                gnomad_data[variant_id][source] = None
                
            elif response["data"]["variant"][source] is not None:
                gnomad_data[variant_id][source] = {}

                for entry in response["data"]["variant"][source]["populations"]:
                    gnomad_data[variant_id][source][entry["id"]] = {
                        "allele_count": entry["ac"],
                        "allele_number": entry["an"],
                        "homozygotes": entry["ac_hom"],
                        "allele_freq": "{0:.9f}".format(float(entry["ac"] / entry["an"]))
                    }

                switch = {
                    "AFR": "African/African-American",
                    "AMI": "Amish",
                    "AMR": "Latino/Admixed American",
                    "ASJ": "Ashkenazi Jewish",
                    "EAS": "East Asian",
                    "FIN": "Finnish",
                    "NFE": "Non-Finnish European",
                    "OTH": "Other",
                    "SAS": "South Asian"
                }

                # Remove unwanted data, rename keys 
                for old_key in list(gnomad_data[variant_id][source]):
                    if old_key in switch:
                        new_key = switch.get(old_key, "")
                        gnomad_data[variant_id][source][new_key] = gnomad_data[variant_id][source].pop(old_key)
                    else:
                        gnomad_data[variant_id][source].pop(old_key)

                gnomad_data[variant_id][source]["totals"] = {
                    "allele_count": response["data"]["variant"][source]["ac"],
                    "allele_number": response["data"]["variant"][source]["an"],
                    "homozygotes": response["data"]["variant"][source]["ac_hom"]
                }

                allele_frequency = "{0:.9f}".format(float(gnomad_data[variant_id][source]["totals"]["allele_count"] / gnomad_data[variant_id][source]["totals"]["allele_number"]))
                gnomad_data[variant_id][source]["totals"]["allele_freq"] = allele_frequency
            else:
                gnomad_data[variant_id][source] = None

        return gnomad_data