from django.db import models
from .ensemble import Ensemble

class Gene(models.Model):
    def __init__(self, name, cdna_seq, wt_allele, variant_position, mt_allele):
        self.name = name
        self.cdna_seq = cdna_seq
        self.wt_allele = wt_allele
        self.variant_position = variant_position
        self.mt_allele = mt_allele

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

    aa_info = [
        ['M', 'Methionine', 'Met', 'Non-Polar, Sulfur-Containing', 'Essential'],
        ['C', 'Cysteine', 'Cys', 'Non-Polar, Sulfur-Containing', 'Non-Essential'],
        ['W', 'Tryptophan', 'Trp', 'Non-Polar, Aromatic', 'Essential'],
        ['F', 'Phenylalanine', 'Phe', 'Non-Polar, Aromatic', 'Essential'],
        ['I', 'Isoleucine', 'Ile', 'Non-Polar, Aliphatic', 'Essential'],
        ['G', 'Glycine', 'Gly', 'Non-Polar, Aliphatic', 'Non-Essential'],
        ['V', 'Valine', 'Val', 'Non-Polar, Aliphatic', 'Essential'],
        ['A', 'Alanine', 'Ala', 'Non-Polar, Aliphatic', 'Non-Essential'],
        ['P', 'Proline', 'Pro', 'Non-Polar, Aliphatic', 'Non-Essential'],
        ['L', 'Leucine', 'Leu', 'Non-Polar, Aliphatic', 'Essential'],
        ['N', 'Asparagine', 'Asn', 'Polar, Amidic', 'Non-Essential'],
        ['Q', 'Glutamine', 'Gln', 'Polar, Amidic', 'Non-Essential'],
        ['Y', 'Tyrosine', 'Tyr', 'Polar, Aromatic', 'Non-Essential'],
        ['T', 'Threonine', 'Thr', 'Polar, Hydroxylic', 'Essential'],
        ['S', 'Serine', 'Ser', 'Polar, Hydroxylic', 'Non-Essential'],
        ['K', 'Lysine', 'Lys', 'Positively-Charged, Basic', 'Essential'],
        ['H', 'Histidine', 'His', 'Positively-Charged, Basic', 'Essential'],
        ['R', 'Arginine', 'Arg', 'Positively-Charged, Basic', 'Non-Essential'],
        ['D', 'Aspartic Acid', 'Asp', 'Negatively-Charged, Acidic', 'Non-Essential'],
        ['E', 'Glutamic Acid', 'Glu', 'Negatively-Charged, Acidic', 'Non-Essential']
        ]
    
    def protein_variant(self):
        return f"p.{self.wt_allele}{self.variant_position}{self.mt_allele}"
        
    @classmethod
    def get_aa_info(cls, amino_acid):
        for aa in cls.aa_info:
            if aa[0] == amino_acid:
                return aa

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
    
    def wt_codon(self, aa_position):
        """
        Returns WT Codon based on amino acid position
        """
        codon_position = int((int(aa_position) - 1) / 3)
        codon_seq = self.codon_seq()
        return codon_seq[codon_position]

    def mt_codon(self, aa_position, wt_codon, mt_nt):
        """
        Returns MT Codon based on amino acid position
        """
        mt_codon = wt_codon.copy()
        mt_codon[(aa_position - 1) % 3] = mt_nt
        return mt_codon

    # def protein_variant(self, wt_nt, position, mt_nt):
    #     """
    #     Return protein variant as result of nucleotide change
    #     """

    #     # Obtain the WT codon
    #     wt_codon = self.wt_codon(position)

    #     # Mutate the WT codon
    #     mt_codon = self.mt_codon(position, wt_codon, mt_nt)

    #     # Convert WT/M codon lists to strings
    #     wt_codon = "".join(wt_codon)
    #     mt_codon = "".join(mt_codon)

    #     table = Gene.codon_table
    #     return f"p.{table[wt_codon]}{codon_position + 1}{table[mt_codon]}"

    @classmethod
    def mutant_codon_list(cls, wt_codon, mt_aa):
        """
        Returns list of codons that give rise to an amino acid via a SNV within reference codon
        """

        # Obtain codons of MT amino acid
        mt_codons = cls.aa_table[mt_aa]

        # List to store codons of mutant amino acid
        mut_codon_list = []

        # Iterate over each codon in list
        for mt_codon in mt_codons:

            # Counter to track nucleotide changes
            mutations = 0

            # Counter to track nucleotide count
            nt_count = 0

            # Iterate over each nucleotide in wildtype and mutant codon
            # Zip function pairs the two nucelotides together
            for i,j in zip(wt_codon, mt_codon):
                nt_count += 1

                if i != j:
                    mutations += 1

                # Append codons to list that give rise to amino acid via a SNV
                if nt_count == 3 and mutations == 1:
                    mut_codon_list.append(mt_codon)
        return mut_codon_list


    def coding_variants(self, wt_aa, aa_location, mt_aa):
        """
        Returns potential coding variants as a result of amino acid change
        Returns a nested list [variant, wt_nt, mt_nt] 
        """

        # Convert position to integer
        aa_location = int(aa_location)

        # Obtain WT codon
        codon_seq = self.codon_seq()
        wt_codon = "".join(codon_seq[aa_location - 1])

        # Obtain list of codons that give rise to MT amino acid via a SNV
        mt_codon_list = self.mutant_codon_list(wt_codon, mt_aa)

        # Declare list to hold index locations of nucleotide changes between WT/M codon
        # List holds [index location, MT codon]
        mutation_index = []

        # Iterate over codons in mutant codon list
        for mt_codon in mt_codon_list:
            index = 0

            # Determine codon index position where nucleotide changes occur
            for i,j in zip(wt_codon, mt_codon):
                if i !=j:
                    mutation_index.append([index, mt_codon])
                else:
                    index += 1

        # List to hold coding coordinates
        coding_variants = []

        for index in mutation_index:

            # Holds index location of first nucleotide of WT codon
            first_nt = ((aa_location) * 3) - 3

            # Determine which nucleotide in codon is changed
            nt_change = (first_nt + index[0]) + 1

            wt_nt = wt_codon[index[0]]
            mt_nt = index[1][index[0]]

            coding_variants.append([nt_change, wt_nt, mt_nt])

        return coding_variants

    def genomic_variants(self):
        """
        Returns genomic information for each coding variant
        Returns a nested list [chromosome, gdna_start, assembly, strand] 
        """

        # List to hold genomic variants
        genomic_variants = []

        # Obtain list of coding variants
        coding_variants = self.coding_variants(self.wt_allele, self.variant_position, self.mt_allele)

        # Obtain genomic variant for each coding variant
        for variant in coding_variants:
            genomic_variants.append(Ensemble.get_genomic_info(self.name, variant[0]))
        
        return genomic_variants

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

    def variant_ids(self, genomic_variants, coding_variants):
        # List to hold variant IDs
        variant_ids = []

        for genomic, coding in zip(genomic_variants, coding_variants):
            if int(genomic["strand"]) < 0:
                wt_nt = Gene.convert_nucleotide(coding[1])
                mt_nt = Gene.convert_nucleotide(coding[2])
            else:
                wt_nt = coding[1]
                mt_nt = coding[2]

            variant_ids.append(f"{genomic['chromosome']}-{genomic['gdna_start']}-{wt_nt}-{mt_nt}")

        return variant_ids