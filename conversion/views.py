from django.shortcuts import render
from .models import *

def index(request):
    return render(request, "conversion/index.html", {
        "aa_table": Gene.aa_info
    })


def protein(request):
    if request.method == "POST":

        # cDNA seq was submitted as file 
        if request.FILES.get("cdna_file", False):
            cdna_seq = request.FILES["cdna_file"].read().decode("utf-8").replace("\n", "").replace("\r", "").upper()

        # cDNA seq was submitted through textbox
        elif request.POST["cdna_text"]:
            cdna_seq = request.POST["cdna_text"].upper()

        else:
            return render(request, "conversion/index.html", {
                "alert": "A cDNA submission is required",
            })

        gene = Gene(
            name = request.POST["gene_name"],
            cdna_seq = cdna_seq,
            wt_allele = request.POST["wt_aa"],
            variant_position = request.POST["aa_location"],
            mt_allele = request.POST["mt_aa"]
        )

        # Obtain list of coding variants 
        coding_variants = gene.coding_variants(gene.wt_allele, gene.variant_position, gene.mt_allele)

        # Obtain list of genomic variants
        genomic_variants = gene.genomic_variants()

        # Obtain list of variant Ids for gnomAD
        var_ids = gene.variant_ids(genomic_variants, coding_variants)

        # Collect gnomad data for each variant id
        gnomad_data = {}
        for variant_id in var_ids:
            data = Gnomad.gnomad_data(variant_id)
            gnomad_data[variant_id] = data[variant_id]
            
        # Zip variant lists to iterate over together in html
        variants = zip(coding_variants, genomic_variants, var_ids)

        # Obtain wt and mt codons
        wt_codon = gene.wt_codon()
        mt_codons = ", ".join(Gene.mutant_codon_list(wt_codon, gene.mt_allele))

        # Gather amino acid properties 
        wt_aa_info = Gene.get_aa_info(gene.wt_allele)
        mt_aa_info = Gene.get_aa_info(gene.mt_allele)

        # Store amino acid information in list
        wt_aa_info = [wt_codon, gene.wt_allele, wt_aa_info[1], wt_aa_info[2], wt_aa_info[3]]
        mt_aa_info = [mt_codons, gene.mt_allele, mt_aa_info[1], mt_aa_info[2], mt_aa_info[3]]

        return render(request, "conversion/protein.html", {
                    "gene": gene,
                    "variants": variants,
                    "gnomad_data": gnomad_data,
                    "chromosome": genomic_variants[0]['chromosome'],
                    "gdna_start": genomic_variants[0]['gdna_start'],
                    "wt_aa_info": wt_aa_info,
                    "mt_aa_info": mt_aa_info
                })

    return render(request, "conversion/index.html")

def coding(request):
    if request.method == "POST":

        # cDNA seq was submitted as file 
        if request.FILES.get("cdna_file", False):
            cdna_seq = request.FILES["cdna_file"].read().decode("utf-8").replace("\n", "").replace("\r", "").upper()

        # cDNA seq was submitted through textbox
        elif request.POST["cdna_text"]:
            cdna_seq = request.POST["cdna_text"].upper()

        else:
            return render(request, "conversion/index.html", {
                "alert": "A cDNA submission is required",
            })

        gene = Gene(
            name = request.POST["gene_name"],
            cdna_seq = cdna_seq,
            wt_allele = request.POST["wt_nt"],
            variant_position = request.POST["nt_location"],
            mt_allele = request.POST["mt_nt"]
        )

        # Obtain genomic variant
        genomic_variant = Ensemble.get_genomic_info(gene.name, gene.variant_position)

        # Obtain variant id
        variant_id = self.variant_id(genomic_variant)
        
        return render(request, "conversion/coding.html")

    return render(request, "conversion/index.html")