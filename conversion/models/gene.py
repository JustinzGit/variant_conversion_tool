from django.db import models

class Gene(models.Model):
    def __init__(self, name, cdna_seq):
        self.name = name
        self.cdna_seq = cdna_seq

    codon_table = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
        'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
        }

    aa_table = {
        'M': ['ATG'],
        'W': ['TGG'],
        'N': ['AAC', 'AAT'],
        'K': ['AAA', 'AAG'],
        'H': ['CAC', 'CAT'],
        'Q': ['CAA', 'CAG'],
        'D': ['GAC', 'GAT'],
        'E': ['GAA', 'GAG'],
        'F': ['TTC', 'TTT'],
        'Y': ['TAC', 'TAT'],
        'C': ['TGC', 'TGT'],
        'I': ['ATA', 'ATC', 'ATT'],
        '_': ['TAA', 'TAG', 'TGA'],
        'T': ['ACA', 'ACC', 'ACG', 'ACT'],
        'G': ['GGA', 'GGC', 'GGG', 'GGT'],
        'V': ['GTA', 'GTC', 'GTG', 'GTT'],
        'A': ['GCA', 'GCC', 'GCG', 'GCT'],
        'P': ['CCA', 'CCC', 'CCG', 'CCT'],
        'S': ['AGC', 'AGT','TCA', 'TCC', 'TCG', 'TCT'],
        'L': ['CTA', 'CTC', 'CTG', 'CTT', 'TTA', 'TTG'],
        'R': ['CGA', 'CGC', 'CGG', 'CGT', 'AGA', 'AGG']
    }
        
    def codon_seq(self):
        """
        Returns a nested list of codons
        """

        # Store sequence in a list of single characters
        nt_seq = list(self.cdna_seq)

        # Group nucleotides by 3
        codon_seq = []
        if len(nt_seq) % 3 == 0:
            for i in range(0, len(nt_seq), 3):
                codon = list(nt_seq[i:i + 3])
                codon_seq.append(codon)   

        return codon_seq

    def protein_variant(self, wt_nt, position, mt_nt):
        """
        Return protein variant as result of nucleotide change
        """
        
        # Obtain the WT codon
        codon_position = int((position - 1) / 3)
        codon_seq = self.codon_seq()
        wt_codon = codon_seq[codon_position]

        # Mutate the WT codon
        mt_codon = wt_codon.copy()
        mt_codon[(position - 1) % 3] = mt_nt

        # Convert WT/M codon lists to strings
        wt_codon = "".join(wt_codon)
        mt_codon = "".join(mt_codon)

        table = Gene.codon_table
        return f"p.{table[wt_codon]}{codon_position + 1}{table[mt_codon]}"


    # def coding_variant(self, wt_aa, aa_location, mt_aa):
    #     """
    #     Return coding variant as result of protein change 
    #     """

    #     # Obtain WT codon
    #     codon_seq = self.codon_seq()
    #     wt_codon = "".join(codon_seq[aa_location - 1])

    #     # Obtain list of codons that give rise to MT amino acid via a SNV
    #     mt_codon_list = mutant_codon_list(wt_codon, mt_aa)

    #         # Define list to hold index locations of nucleotide changes between WT/M codon
    #         # List holds [index location, MT codon]
    #         mutation_index = []

    #         # Iterate over codons in mutant codon list
    #         for mt_codon in mt_codon_list:
    #             index = 0

    #             # Determine codon index position where nucleotide changes occur
    #             for i,j in zip(wt_codon, mt_codon):
    #                 if i !=j:
    #                     mutation_index.append([index, mt_codon])
    #                 else:
    #                     index += 1

    


    