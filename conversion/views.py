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
            cdna_seq = cdna_seq
        )

        # Ensure user has submitted these
        wt_aa = request.POST["wt_aa"]
        aa_location = request.POST["aa_location"]
        mt_aa = request.POST["mt_aa"]

        # Format protein variant according to input 
        protein_variant = f"p.{wt_aa}{aa_location}{mt_aa}"

        # Obtain list of coding variants 
        coding_variants = gene.coding_variants(wt_aa, aa_location, mt_aa)

        # Fetch genomic information for each potential coding variant
        genomic_variants = []
        for variant in coding_variants:
            genomic_variants.append(Ensemble.get_genomic_info(gene.name, variant[0]))

        # Using first variant in genomic / coding variants list to collect data from gnomAD
        strand = genomic_variants[0]["strand"]
        gdna_start = genomic_variants[0]["gdna_start"]
        chromosome = genomic_variants[0]["chromosome"]
        
        wt_nt = coding_variants[0][1]
        mt_nt = coding_variants[0][2]

        variant_ids = []
        for variant in genomic_variants:
            variant_ids.append(Gnomad.get_variant_id(variant["strand"], variant["chromosome"], 
            variant["gdna_start"], wt_nt, mt_nt))

        gnomad_data = Gnomad.get_gnomad_data(strand, chromosome, gdna_start, wt_nt, mt_nt)

        variant_id = Gnomad.get_variant_id(variant["strand"], variant["chromosome"], variant["gdna_start"], wt_nt, mt_nt)
        
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