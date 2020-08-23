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
        Returns variant id, format recognized by gnomad
        """

        # If gene is on negative strand, convert nucleotides
        if int(strand) < 0:
            wt_nt = cls.convert_nucleotide(wt_nt)
            mt_nt = cls.convert_nucleotide(mt_nt)

        return f"{chromosome}-{gdna_start}-{wt_nt}-{mt_nt}"

        