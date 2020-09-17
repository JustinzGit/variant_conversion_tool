from django.shortcuts import render
from .models import *
import re

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
                 "aa_table": Gene.aa_info
            })

        wt_allele = request.POST["wt_aa"]
        variant_position = request.POST["aa_location"]
        mt_allele = request.POST["mt_aa"]

        if not wt_allele.strip() or not variant_position.strip() or not mt_allele.strip():
             return render(request, "conversion/index.html", {
                "alert": "Improper Protein Variant Submission: Be Sure To Fill Out All Fields",
                 "aa_table": Gene.aa_info
            })

        gene = Gene(
            name = request.POST["gene_name"],
            cdna_seq = cdna_seq,
            wt_allele = wt_allele,
            variant_position = variant_position,
            mt_allele = mt_allele
        )

        # Obtain list of coding variants 
        try:
            coding_variants = gene.coding_variants(gene.wt_allele, gene.variant_position, gene.mt_allele)
        except IndexError:
             return render(request, "conversion/index.html", {
                "alert": "Variant position is out of range",
                 "aa_table": Gene.aa_info
            })

        # Obtain wt and mt codons
        wt_codon = gene.wt_codon("protein")
        if wt_codon not in Gene.aa_table[gene.wt_allele]:
             return render(request, "conversion/index.html", {
                "alert": f"Amino acid '{gene.wt_allele}' is not located at position {gene.variant_position}",
                 "aa_table": Gene.aa_info
            })
        
        mt_codon_list = Gene.mutant_codon_list(wt_codon, gene.mt_allele)
        if len(mt_codon_list) == 0:
            return render(request, "conversion/index.html", {
                "alert": f"The WT codon '{wt_codon}' that encodes the amino acid '{gene.wt_allele}' within your sequence cannot produe the amino acid '{gene.mt_allele}' via a single nucleotide change",
                "aa_table": Gene.aa_info
            })
        
        mt_codons = ", ".join(mt_codon_list)

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

        # Gather amino acid properties 
        wt_aa_info = Gene.get_aa_info(gene.wt_allele)
        mt_aa_info = Gene.get_aa_info(gene.mt_allele)

        # Store amino acid information in list
        wt_aa_info = [wt_codon, gene.wt_allele, wt_aa_info[1], wt_aa_info[2], wt_aa_info[3]]
        mt_aa_info = [mt_codons, gene.mt_allele, mt_aa_info[1], mt_aa_info[2], mt_aa_info[3]]

        return render(request, "conversion/protein.html", {
                    "gene": gene,
                    "variants": variants,
                    "var_ids": var_ids,
                    "gnomad_data": gnomad_data,
                    "chromosome": genomic_variants[0]['chromosome'],
                    "gdna_start": genomic_variants[0]['gdna_start'],
                    "wt_aa_info": wt_aa_info,
                    "mt_aa_info": mt_aa_info
                })

    elif request.method == "GET":
         return render(request, "conversion/index.html", {
                "alert": "A variant submission is required",
                 "aa_table": Gene.aa_info
            })

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
        genomic_variant = gene.genomic_variant()

        chromosome = re.split(':|/| |Chr', genomic_variant)[2]
        gdna_start = re.split(':|/| |Chr', genomic_variant)[3]

        # Obtain variant id
        variant_id = gene.variant_id(genomic_variant)

        # Obtain data from gnomad
        gnomad_data = Gnomad.gnomad_data(variant_id)

        # Obtain wt and mt codon
        wt_codon = gene.wt_codon("coding")
        mt_codon = gene.mt_codon(gene.variant_position, wt_codon, gene.mt_allele)

        # Obtain protein variant
        protein_variant = gene.protein_variant(wt_codon, mt_codon)
        split_protein_variant = protein_variant.split(".")[1]
        wt_aa = split_protein_variant[0]
        mt_aa = split_protein_variant[-1]

        # Gather amino acid properties 
        wt_aa_info = Gene.get_aa_info(wt_aa)
        mt_aa_info = Gene.get_aa_info(mt_aa)

        # Store amino acid information in list
        wt_aa_info = [wt_codon, wt_aa, wt_aa_info[1], wt_aa_info[2], wt_aa_info[3]]
        mt_aa_info = [mt_codon, mt_aa, mt_aa_info[1], mt_aa_info[2], mt_aa_info[3]]
        
        return render(request, "conversion/coding.html", {
            "gene": gene,
            "genomic_variant": genomic_variant,
            "variant_id": variant_id,
            "protein_variant": protein_variant,
            "chromosome": chromosome,
            "gdna_start": gdna_start,
            "wt_aa_info": wt_aa_info,
            "mt_aa_info": mt_aa_info,
            "gnomad_data": gnomad_data
        })

    elif request.method == "GET":
         return render(request, "conversion/index.html", {
                "alert": "A Variant Submission Is Required",
                 "aa_table": Gene.aa_info
            })