from django.db import models

class Gene(models.Model):
    name = models.CharField(max_length=8)
    sequence = models.TextField()
        
    def format_sequence(self):
        cdna_seq = self.sequence.read().decode("utf-8").replace("\n", "").replace("\r", "").upper()

        # Store sequence in a list of single characters
        nt_seq = list(cdna_seq)

        # Group nucleotides by 3
        codon_seq = []
        if len(nt_seq) % 3 == 0:
            for i in range(0, len(nt_seq), 3):
                codon = list(nt_seq[i:i + 3])
                codon_seq.append(codon)
                
        return codon_seq