from django.shortcuts import render
from .models import *

def index(request):
    return render(request, "conversion/index.html", {
        "aa_table": Gene.aa_info
    })

# Variant to test on
# P715L c.2144 C/T	chr17:40469200	

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
        coding_variants = gene.coding_variants(wt_aa, aa_location, mt_aa)

        # Obtain list of genomic variants
        genomic_variants = gene.genomic_variants()

        # Obtain variant Ids for gnomAD
        var_ids = gene.variant_ids(genomic_variants, coding_variants)

        # Collect gnomad data for each variant id
        gnomad_data = []
        for variant_id in var_ids:
            gnomad_data.append(Gnomad.gnomad_data(variant_id))

        if gnomad_data['genome'] is not None:
            title = f"{variant_id} - gnomAd - Genomes"
            gnomad_data = gnomad_data['genome']

        else:
            title = f"{variant_id} - gnomAd - Exomes"
            gnomad_data = gnomad_data['exome']
    
        # Zip variant lists to iterate over together in html
        variants = zip(coding_variants, genomic_variants, variant_ids)

        # Links to redirect user to genome browser and gnomad
        browser_link = f"https://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position={chromosome}%3A{gdna_start}"
        gnomad_link = f"https://gnomad.broadinstitute.org/variant/{variant_id}?dataset=gnomad_r2_1"

        wt_codon = gene.wt_codon(coding_variants[0][0])
        wt_aa_info = Gene.get_aa_info(wt_aa)
        wt_aa_info = ["".join(wt_codon), wt_aa, wt_aa_info[1], wt_aa_info[2], wt_aa_info[3]]

        mt_codons = ", ".join(Gene.mutant_codon_list(wt_codon, mt_aa))
        mt_aa_info = Gene.get_aa_info(mt_aa)
        mt_aa_info = [mt_codons, mt_aa, mt_aa_info[1], mt_aa_info[2], mt_aa_info[3]]

        return render(request, "conversion/protein.html", {
                    "gene_name": gene.name,
                    "variants": variants,
                    "protein_variant": protein_variant,
                    "variant_id": variant_id,
                    "gnomad_data": gnomad_data,
                    "title": title,
                    "browser_link": browser_link,
                    "gnomad_link": gnomad_link,
                    "wt_aa_info": wt_aa_info,
                    "mt_aa_info": mt_aa_info
                })

    return render(request, "conversion/index.html")

def coding(request):
    pass