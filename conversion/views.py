from django.shortcuts import render
# from django import forms
# from forms import UploadFileForm
# from django.http import HttpResponse

def index(request):
    return render(request, "conversion/index.html")

def protein_conversion(request):
    if request.method == "POST":

        # cDNA seq was submitted as file 
        if request.FILES.get('cdna_file', False):
            cdna_seq = request.FILES.read().decode("utf-8")
            cdna_seq = cdna_seq.replace("\n", "").replace("\r", "").upper()

        # cDNA seq was submitted through textbox
        elif request.POST["cdna_text"]:
            cdna_seq = request.POST["cdna_text"]
            cdna_seq = cdna_seq.replace("\n", "").replace("\r", "").upper()

        else:
            return render(request, "conversion/protein_conversion.html", {
                "alert": "A cDNA submission is required",
            })
            
    return render(request, "conversion/protein_conversion.html", {
                "file_data": cdna_seq
            })