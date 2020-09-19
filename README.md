# Variant Conversion Tool (VCT)
The VCT is a tool for scientists who wish to easily convert mutation coordinates to their respective coding or protein variant. 

Genomic coordinates (GRCh37/hg19) are also obtained and a link is provided for quick access to the variants position on the [UCSC Genome Browser](https://genome.ucsc.edu/). 

Genome and/or exome data from [gnomAd](https://gnomad.broadinstitute.org/) is displayed if the variant is located within gnomADs dataset v2.1 (GRCh37/hg19). A link to a variants webpage at gnomAD is also provided to obtain additional information.

Data is collected from Ensembl to obtain a variants genomic coordinates using the [Ensembl REST API](http://europepmc.org/article/MED/25236461?singleResult=true).

The VCT can be accessed from the web at [https://variant-conversion-tool.herokuapp.com/](https://variant-conversion-tool.herokuapp.com/)

# Usage
- Navigate to [VCT at Heroku](https://variant-conversion-tool.herokuapp.com/)
- Provide the official gene name
- Input a cDNA text file that begins with a start codon and ends with a stop codon
- Alternatively, the nucelotide sequence can be pasted into the provided text box
- Input either coding or protein variant to obtain conversion coordinates

## Contributing
Bug reports and pull requests are welcome on GitHub at https://github.com/JustinzGit/variant_conversion_tool. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct.

## License
This application is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
