from django.shortcuts import render
from .models import *

def index(request):

    aa_table = [
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

    return render(request, "conversion/index.html", {
        "aa_table": aa_table
    })

def conversion(request):
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

        wt_nt = request.POST["wt_nt"]
        nt_location = request.POST["nt_location"]
        mt_nt = request.POST["mt_nt"]

        return render(request, "conversion/index.html", {
                    "file_data": gene.protein_variant(wt_nt, int(nt_location), mt_nt)
                })

    return render(request, "conversion/index.html")