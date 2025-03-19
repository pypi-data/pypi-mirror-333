# RRMScorer: RRM-RNA score predictor

![PyPI - Version](https://img.shields.io/pypi/v/rrmscorer)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rrmscorer)
![Conda Version](https://img.shields.io/conda/v/bioconda/rrmscorer)
![Website](https://img.shields.io/website?url=https%3A%2F%2Fbio2byte.be%2Frrmscorer&label=Web%20predictions)
![Bitbucket last commit](https://img.shields.io/bitbucket/last-commit/bio2byte/rrmscorer/master)


RRMScorer allows the user to easily predict how likely a single RRM is to bind ssRNA using a carefully generated alignment for the RRM structures in complex with RNA, from which we analyzed the interaction patterns and derived the scores (Please address to the publication for more details on the method REF)

**🔗 RRMScorer is also available online now! (https://bio2byte.be/rrmscorer/)**

From _"Deciphering the RRM-RNA recognition code: A computational analysis"_ publication:

> RNA recognition motifs (RRM) are the most prevalent class of RNA binding domains in eucaryotes. Their RNA binding preferences have been investigated for almost two decades, and even though some RRM domains are now very well described, their RNA recognition code has remained elusive. An increasing number of experimental structures of RRM-RNA complexes has become available in recent years. Here, we perform an in-depth computational analysis to derive an RNA recognition code for canonical RRMs. We present and validate a computational scoring method to estimate the binding between an RRM and a single stranded RNA, based on structural data from a carefully curated multiple sequence alignment, which can predict RRM binding RNA sequence motifs based on the RRM protein sequence. Given the importance and prevalence of RRMs in humans and other species, this tool could help design RNA binding motifs with uses in medical or synthetic biology applications, leading towards the de novo design of RRMs with specific RNA recognition.

Please address to the publication for more details on the method REF.

For more information about the methodology please visit the [Methodology](https://bio2byte.be/rrmscorer/methodology) page on our RRMScorer website.


## Installation

#### Clone this repository to your working environment:
```console
$ git clone git@bitbucket.org:bio2byte/rrmscorer.git && cd rrmscorer
```

#### The following packages are required:

```python
python~=3.10
numpy~=1.21
pandas~=1.4
biopython~=1.79
matplotlib~=3.5
scikit-learn~=1.1
hmmer~=3.3
logomaker~=0.8
seaborn~=0.13
requests~=2.32
```

#### Via [Conda](https://docs.conda.io/en/latest/):

```console
$ conda create --yes --name rrmscorer python==3.10.4
$ conda activate rrmscorer
$ conda install --yes --file requirements.txt
```

#### Via [Virtual Environment](https://docs.python.org/3/tutorial/venv.html):

```console
$ python3 -m venv rrmscorer-venv
$ source ./rrmscorer-venv/bin/activate
$ python -m pip install -r rrmscorer/requirements.txt
```

## How to run it:
Either you are using Conda or Virtual Environments for your installation, before executing this software features, you need to setup the Python environment.
Using Conda:

```console
$ conda activate rrmscorer
```
Using Virtual Environment:

```console
$ source ./rrmscorer-venv/bin/activate
```

Continue reading the next section to find further details about the available features.
In case you need to deactivate this Python environment:

Using Conda:

```console
$ conda deactivate
```

Using Virtual Environment:

```console
$ deactivate
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
7. `-a` [Optional] To generate a fasta file with each input sequence aligned to the HMM


```console
$ python rrm_rna_wrapper.py -u P19339 -r UAUAUUAGUAGUA -w 5 -j output/ -c output/ -p output/
```

Example output:
```console
UAUAU -1.08
AUAUU -0.99
UAUUA -1.33
AUUAG -0.90
UUAGU -1.07
```

### ii) Fasta file with RRM sequences vs RNA
To use this feature the user needs to input:

1. `-f` Fasta file with 1 or more RRM sequences. The sequences are aligned to the master alignment HMM.
1. `-r` The RNA sequence to test
1. `-w` [default=5] The window size to test (**Only 3 and 5 nucleotide windows are accepted**)
4. `-j` [Optional] To store the results in a json file per RRM found in the declared directory path
5. `-c` [Optional] To store the results in a csv file per RRM found in the declared directory path
6. `-p` [Optional] To generate score plots for all the RNA possible windows per RRM found in the declared directory path
7. `-a` [Optional] To generate a fasta file with each input sequence aligned to the HMM

```console
$ python rrm_rna_wrapper.py -f input_files/rrm_seq.fasta -r UAUAUUAGUAGUA -c output/
```


### iii) Fasta file / UniProt id to find top-scoring RNAs
To use this feature the user needs to input:

1. `-f` Fasta file or UniProt Id is as described in the previous cases.
1. `-w` [default=5] The window size to test (**Only 3 and 5 nucleotide windows are accepted**)
1. `-t` To find the top-scoring RNA for the specified RRM/s
4. `-j` [Optional] To store the results in a json file per RRM found in the declared directory path
5. `-c` [Optional] To store the results in a csv file per RRM found in the declared directory path
6. `-p` [Optional] To generate score plots for all the RNA possible windows per RRM found in the declared directory path
7. `-a` [Optional] To generate a fasta file with each input sequence aligned to the HMM

```console
$ python rrm_rna_wrapper.py -f input_files/rrm_seq.fasta -ws 5 -top -j output/
```


## Contact us

Developed by [Bio2Byte](https://bio2byte.be) group, within the [RNAct](https://rnact.eu) project. Wim Vranken, VUB, Brussels. For any further questions, feedback or suggestions, please contact us via email: [Bio2Byte@vub.be](mailto:Bio2Byte@vub.be).

## Funding

This project has received funding from the European Union's Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No. 813239. This work was supported by the European Regional Development Fund and Brussels-Capital Region-Innoviris within the framework of the Operational Programme 2014–2020 [ERDF-2020 project ICITY-RDI.BRU]
