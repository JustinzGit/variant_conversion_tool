from django.db import models

class Gnomad(models.Model):
    @classmethod
    def convert_nucleotide(cls, nucleotide):
        """
        Convert nucleotide to its binding partner
        """
        switch = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
        }

        return switch.get(nucleotide,"")

    @classmethod
    def get_variant_id(cls, strand, chromosome, gdna_start, wt_nt, mt_nt):
        """
        Returns variant in a format recognized by gnomad
        """

        # If gene is on negative strand, convert nucleotides
        if int(strand) < 0:
            wt_nt = cls.convert_nucleotide(wt_nt)
            mt_nt = cls.convert_nucleotide(mt_nt)

        return f"{chromosome}-{gdna_start}-{wt_nt}-{mt_nt}"

    @classmethod
    def gnomad_data(cls, variant_id):
        """
        Returns gnomAD data for provided variant
        """

        query = """query{{
            variant(dataset: gnomad_r2_1, variantId: "{variant_id}") {{
                genome{{
                ac
                an
                ac_hom
                populations {{
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
                populations {{
                    id
                    ac
                    an
                    ac_hom
                }}
                }}
                variantId
                reference_genome
                rsid
            }}
            }}""" 

        # Request data from gnomad
        request = requests.post("https://gnomad.broadinstitute.org/api", json={'query': query}) 

        # Convert string to JSON object
        response = response.json()

        # Variant was not found in gnomad
        if "errors" in response:
            gnomad_data = "variant not found"

        elif response["data"]["variant"]["genome"] is None:
            gnomad_data = "no genome data exists"

        # Dict to store data from gnomad
        else:
            gnomad_data = dict(
                population = ['African/African-American', 'Amish', 'Latino/Admixed American',
                'Ashkenazi Jewish','East Asian','Finnish','Non-Finnish European','Other','South Asian'], 
                allele_count = [], 
                allele_number = [], 
                homozygotes = [], 
                allele_freq = [], 
                total = [])

            # Collect population data
            populations = response["data"]["variant"]["genome"]["populations"]

            # Store population data
            for i in range(0, 27, 3):
                gnomad_data['allele_count'].append(populations[i]['ac'])
                gnomad_data['allele_number'].append(populations[i]['an'])
                gnomad_data['homozygotes'].append(populations[i]['ac_hom'])

            # Calculate allele frequency
            for i in range(len(gnomad['pop_ac'])):
                gnomad_data['allele_freq'].append("{0:.9f}".format(float(gnomad_data['allele_count'][i]/gnomad_data['allele_number'][i])))

            allele_count_total = 0
            allele_number_total = 0
            homozygotes_total = 0

            # Calculate totals for population data across ethnicities
            for i in range(len(gnomad_data['pop_ac'])):
                allele_count_total += int(gnomad_data['pop_ac'][i])
                allele_number_total += int(gnomad_data['pop_an'][i])
                homozygotes_total += int(gnomad_data['pop_hom'][i])
            
            gnomad_data['total'].append(allele_count_total)
            gnomad_data['total'].append(allele_number_total)
            gnomad_data['total'].append(homozygotes_total)
            gnomad_data['total'].append("{0:.9f}".format(float(gnomad_data['total'][0]/gnomad_data['total'][1])))
        
        return gnomad_data

    @classmethod
    def get_gnomad_data(cls, strand, chromosome, gdna_start, wt_nt, mt_nt):
        variant_id = cls.get_variant_id(strand, chromosome, gdna_start, wt_nt, mt_nt)
        return cls.gnomad_data(variant_id)