# RRMScorer: RRM-RNA score predictor

![PyPI - Version](https://img.shields.io/pypi/v/rrmscorer)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rrmscorer)
![Conda Version](https://img.shields.io/conda/v/bioconda/rrmscorer)
![Website](https://img.shields.io/website?url=https%3A%2F%2Fbio2byte.be%2Frrmscorer&label=Web%20predictions)
![Bitbucket last commit](https://img.shields.io/bitbucket/last-commit/bio2byte/rrmscorer/master)

RRMScorer allows the user to easily predict how likely a single RRM is to bind ssRNA using a carefully generated alignment for the RRM structures in complex with RNA, from which we analyzed the interaction patterns and derived the scores.

**🔗 RRMScorer is also available online now! (https://bio2byte.be/rrmscorer/)**

From _"Deciphering the RRM-RNA recognition code: A computational analysis"_ publication:

> RNA recognition motifs (RRM) are the most prevalent class of RNA binding domains in eucaryotes. Their RNA binding preferences have been investigated for almost two decades, and even though some RRM domains are now very well described, their RNA recognition code has remained elusive. An increasing number of experimental structures of RRM-RNA complexes has become available in recent years. Here, we perform an in-depth computational analysis to derive an RNA recognition code for canonical RRMs. We present and validate a computational scoring method to estimate the binding between an RRM and a single stranded RNA, based on structural data from a carefully curated multiple sequence alignment, which can predict RRM binding RNA sequence motifs based on the RRM protein sequence. Given the importance and prevalence of RRMs in humans and other species, this tool could help design RNA binding motifs with uses in medical or synthetic biology applications, leading towards the de novo design of RRMs with specific RNA recognition.

Please address to the publication for more details on the method REF.

For more information about the methodology please visit the [Methodology](https://bio2byte.be/rrmscorer/methodology) page on our RRMScorer website.

### Pip package installation
> pip is the package installer for Python. You can use pip to install packages from the Python Package Index and other indexes.

**🔗 Related links:**

- [Official website and online predictor](https://bio2byte.be/rrmscorer/)
- [PyPi package for RRMScorer](https://pypi.org/project/rrmscorer/)
- [Bioconda recipe for RRMScorer](https://bioconda.github.io/recipes/rrmscorer/README.html)

```bash
$ pip install rrmscorer
```

**⚠️ Important note:**
Apple silicon users may need to install the package in a Rosetta environment, using conda for isntance, bacause some packages are not available for the silicon architecture yet.
```bash
$ CONDA_SUBDIR=osx-64 conda create -n rosetta_environment
```

## Features

RRMScorer has several features to either calculate the binding score for a specific RRM and RNA sequences, for a set of RRM sequences in a FASTA file, or to explore which are the best RNA binders according to our scoring method.

```bash
$ rrmscorer --help
```

```bash
Executing rrmscorer version ...
usage: rrmscorer [-h] (-u UNIPROT_ID | -f /path/to/input.fasta) (-r RNA_SEQUENCE | -t) [-w N] [-j /path/to/output] [-c /path/to/output] [-p /path/to/output] [-a /path/to/output] [-v]

RRM-RNA scoring version ...

options:
  -h, --help            show this help message and exit
  -u UNIPROT_ID, --uniprot UNIPROT_ID
                        UniProt identifier
  -f /path/to/input.fasta, --fasta /path/to/input.fasta
                        Fasta file path
  -r RNA_SEQUENCE, --rna RNA_SEQUENCE
                        RNA sequence
  -t, --top             To find the top scoring RNA fragments
  -w N, --window_size N
                        The window size to test
  -j /path/to/output, --json /path/to/output
                        Store the results in a json file in the declared directory path
  -c /path/to/output, --csv /path/to/output
                        Store the results in a CSV file in the declared directory path
  -p /path/to/output, --plot /path/to/output
                        Store the plots in the declared directory path
  -a /path/to/output, --aligned /path/to/output
                        Store the aligned sequences in the declared directory path
  --x_min X_MIN         Minimum value for x-axis in plots (default: -0.9)
  --x_max X_MAX         Maximum value for x-axis in plots (default: 1.0)
  --title TITLE         Title for the generated plots
  --wrap-title          Wrap long titles to multiple lines
  -v, --version         show RRM-RNA scoring version number and exit
```

### i) UniProt id (with 1 or more RRMs) vs RNA
To use this feature the user needs to input:

1. `-u` The UniProt identifier
2. `-r` The RNA sequence to score
3. `-w` [default=5] The window size to test (**Only 3 and 5 nucleotide windows are accepted**)
4. `-j` [Optional] To store the results in a json file per RRM found in the declared directory path
5. `-c` [Optional] To store the results in a csv file per RRM found in the declared directory path
6. `-p` [Optional] To generate score plots for all the RNA possible windows per RRM found in the declared directory path
7. `-a` [Optional] To generate a FASTA file with each input sequence aligned to the HMM


```bash
$ python -m rrmscorer -u P19339 -r UAUAUUAGUAGUA -w 5 -j output/ -c output/ -p output/
```

### ii) FASTA file with RRM sequences vs RNA
To use this feature the user needs to input:

1. `-f` FASTA file with 1 or more RRM sequences. The sequences are aligned to the master alignment HMM.
1. `-r` The RNA sequence to test
1. `-w` [default=5] The window size to test (**Only 3 and 5 nucleotide windows are accepted**)
4. `-j` [Optional] To store the results in a json file per RRM found in the declared directory path
5. `-c` [Optional] To store the results in a csv file per RRM found in the declared directory path
6. `-p` [Optional] To generate score plots for all the RNA possible windows per RRM found in the declared directory path
7. `-a` [Optional] To generate a FASTA file with each input sequence aligned to the HMM

```bash
$ python -m rrmscorer -f input_files/rrm_seq.fasta -r UAUAUUAGUAGUA -c output/
```

### iii) FASTA file / UniProt id to find top-scoring RNAs
To use this feature the user needs to input:

1. `-f` FASTA file or UniProt Id is as described in the previous cases.
1. `-w` [default=5] The window size to test (**Only 3 and 5 nucleotide windows are accepted**)
1. `-t` To find the top-scoring RNA for the specified RRM/s
4. `-j` [Optional] To store the results in a json file per RRM found in the declared directory path
5. `-c` [Optional] To store the results in a csv file per RRM found in the declared directory path
6. `-p` [Optional] To generate score plots for all the RNA possible windows per RRM found in the declared directory path
7. `-a` [Optional] To generate a FASTA file with each input sequence aligned to the HMM

```bash
$ python -m rrmscorer -f input_files/rrm_seq.fasta -w 5 -top -j output/
```

## 📖 How to cite
If you use this package or data in this package, please cite:

> Roca-Martínez J, Vranken W. Deciphering the RRM-RNA recognition code: A computational analysis. *PLoS Comput Biol.* 2023 Jan 23;19(1):e1010859. [doi:10.1371/journal.pcbi.1010859](https://doi.org/10.1371/journal.pcbi.1010859).


## Contact us

Developed by [Bio2Byte](https://bio2byte.be) group, within the [RNAct](https://rnact.eu) project. Wim Vranken, VUB, Brussels. For any further questions, feedback or suggestions, please contact us via email: [Bio2Byte@vub.be](mailto:Bio2Byte@vub.be).

## Funding

This project has received funding from the European Union's Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No. 813239. This work was supported by the European Regional Development Fund and Brussels-Capital Region-Innoviris within the framework of the Operational Programme 2014–2020 [ERDF-2020 project ICITY-RDI.BRU]
