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
            return render(request, "conversion/conversion.html", {
                "alert": "A cDNA submission is required",
            })
    
        gene = Gene.objects.create(
            name = request.POST["gene_name"],
            cdna_seq = cdna_seq
        )

        return render(request, "conversion/conversion.html", {
                    "file_data": gene.codon_seq()
                })

    return render(request, "conversion/index.html")