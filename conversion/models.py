from django.db import models

class Gene(models.Model):
    name = models.CharField(max_length=8)
    cdna_seq = models.TextField()
        
    def format_sequence(self):

        # Store sequence in a list of single characters
        nt_seq = list(self.cdna_seq)

        # Group nucleotides by 3
        codon_seq = []
        if len(nt_seq) % 3 == 0:
            for i in range(0, len(nt_seq), 3):
                codon = list(nt_seq[i:i + 3])
                codon_seq.append(codon)
                
        return codon_seq