from django.shortcuts import render
from .models import *

def index(request):
    return render(request, "conversion/index.html")

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