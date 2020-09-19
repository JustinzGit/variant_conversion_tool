# Variant Conversion Tool (VCT)
The VCT is a tool for scientists who wish to easily convert mutation coordinates to their respective coding or protein variant. Genomic coordinates (GRCh37/hg19) are also obtained and a link is provided for quick access to the variants position on the [UCSC Genome Browser](https://genome.ucsc.edu/). Genome and/or exome data from [gnomAd](https://gnomad.broadinstitute.org/) is displayed if the variant is located within the v2.1 (GRCh37/hg19) gnomAD dataset. A link to a variants webpage at gnomAD is also provided to obtain additional information. To obtain a variants genomic coordinate data is collected from Ensembl using the [Ensembl REST API](http://europepmc.org/article/MED/25236461?singleResult=true).

The VCT can be accessed from the web at [https://variant-conversion-tool.herokuapp.com/](https://variant-conversion-tool.herokuapp.com/)

# Installation
- Clone this repository 
- Be sure to have [python](https://www.python.org/downloads/) and [django](https://www.djangoproject.com/download/) installed
- Within the main directory, run `python manage.py makemigrations` to create migrations
- Run `python manage.py migrate` to apply migrations
- Run `python manage.py runserver` to start up a local server
- Navigate to `localhost:8000` within the browser to access the conversion application

# Usage
- Provide the official gene name
- Input a cDNA text file that begins with a start codon and ends with a stop codon
- Alternatively, the nucelotide sequence can be pasted into the provided text box
- Input either coding or protein variant to obtain conversion coordinates

## Contributing
Bug reports and pull requests are welcome on GitHub at https://github.com/JustinzGit/variant_conversion_tool. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct.

## License
This application is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
