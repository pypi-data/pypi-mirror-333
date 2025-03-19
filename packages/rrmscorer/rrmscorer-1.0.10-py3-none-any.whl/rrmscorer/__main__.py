# Python wrapper to have available all the scoring classes in one place and
# merge the results in a single output.
import argparse
import csv
import json
import os
import sys

from .rrm_rna_functions import HMMScanner, LogoGenerator, RNAScoring

__version__ = "1.0.10"


def main():
    print(f"Executing rrmscorer version {__version__}.")

    usr_input_handler = UserInputHandler()
    usr_input = usr_input_handler.parse_args()

    Manager(usr_input).input_handler()


class Manager:
    """
    This class is used to manage the input and output of the scoring framework
    """

    STANDARD_AMINO_ACIDS = {
        "A",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "K",
        "L",
        "M",
        "N",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "V",
        "W",
        "Y",
    }
    STANDARD_RNA_NUCLEOTIDES = {"A", "C", "G", "U"}
    N_MERS = [10, 50, 100, 250]

    # This is the general input manager of the scoring framework
    def __init__(self, usr_input):
        self.usr_input = usr_input
        self._rna_scoring = None
        self._hmm_scan = None
        self._logo_gen = None

    @property
    def rna_scoring(self):
        if not self._rna_scoring:
            self._rna_scoring = RNAScoring()

        return self._rna_scoring

    @property
    def hmm_scan(self):
        if not self._hmm_scan:
            self._hmm_scan = HMMScanner()

        return self._hmm_scan

    @property
    def logo_gen(self):
        if not self._logo_gen:
            self._logo_gen = LogoGenerator()

        return self._logo_gen

    def input_handler(self):
        if self.usr_input.fasta_file:
            seqs_dict = self.hmm_scan.hmmalign_RRMs(
                fasta_file=self.usr_input.fasta_file
            )
        elif self.usr_input.up_id:
            seqs_dict = self.hmm_scan.get_UP_seq(UP_id=self.usr_input.up_id)
        else:
            sys.exit("Invalid input parameters")

        for seq_id, seq in seqs_dict.items():
            self.handle_sequence(seq_id, seq)
            if self.usr_input.aligned:
                os.makedirs(os.path.abspath(self.usr_input.aligned), exist_ok=True)

                aln_out_path = os.path.join(
                    os.path.abspath(self.usr_input.aligned),
                    seq_id.replace("/", "_").replace("|", "_") + "_aligned" + ".fasta",
                )

                with open(aln_out_path, "w", encoding="utf-8") as aln_out:
                    aln_out.write(">{}\n{}\n".format(seq_id, seq))

    def handle_sequence(self, seq_id, seq):
        set_seq = set(seq.upper())
        set_seq.remove("-")
        if set_seq.issubset(Manager.STANDARD_AMINO_ACIDS):
            pass
        else:
            print(
                "\033[91m[ERROR] The protein sequence contains"
                " non-standard amino acids.\033[0m",
                file=sys.stderr,
            )
            sys.exit("The protein sequence contains non-standard amino acids.")
        seq_id = seq_id.replace("/", "_").replace("|", "_")

        print(f"\nRunning predictions for {seq_id}...")
        if self.usr_input.top:
            top_scores = self.rna_scoring.find_best_rna(rrm_seq=seq)

            if self.usr_input.json:
                json_path = os.path.join(
                    os.path.abspath(self.usr_input.json), f"{seq_id}_top_scorers.json"
                )
                os.makedirs(os.path.abspath(self.usr_input.json), exist_ok=True)

                with open(json_path, "w", encoding="utf-8") as fp:
                    json.dump(top_scores, fp, indent=2)
                    print(f"Json file successfully saved in {json_path}")

            if self.usr_input.plot:
                for n_mers in Manager.N_MERS:  # Right line
                    plot_path = os.path.join(
                        os.path.abspath(self.usr_input.plot),
                        f"{seq_id}_top_{n_mers}_logo.png",
                    )
                    os.makedirs(os.path.abspath(self.usr_input.plot), exist_ok=True)

                    self.logo_gen.generate_logo_to_file(
                        plot_path,
                        top_scores,
                        n_mers,
                        self.usr_input.window_size,
                        title=self.usr_input.title,
                        wrap_title=self.usr_input.wrap_title,
                    )
                    print(f"Plot successfully saved in {plot_path}")

        elif self.usr_input.rna_seq:
            if not set(self.usr_input.rna_seq).issubset(
                Manager.STANDARD_RNA_NUCLEOTIDES
            ):
                print(
                    "\033[91m[ERROR] The RNA sequence contains"
                    " non-standard RNA nucleotides.\033[0m"
                )
                sys.exit("Invalid input parameters")

            self.rna_scoring.score_out_seq(
                rrm_seq=seq,
                rna_seq=self.usr_input.rna_seq,
                rna_pos_range=self.usr_input.rna_pos_range,
            )

            for key, score in self.rna_scoring.scores_dict.items():
                print(key, score)

            if self.usr_input.json:
                json_path = os.path.join(
                    os.path.abspath(self.usr_input.json), f"{seq_id}.json"
                )

                os.makedirs(os.path.abspath(self.usr_input.json), exist_ok=True)

                with open(json_path, "w", encoding="utf-8") as fp:
                    json.dump(self.rna_scoring.scores_dict, fp, indent=2)
                    print(f"Json file successfully saved in {json_path}")

            if self.usr_input.csv:
                csv_path = os.path.join(
                    os.path.abspath(self.usr_input.csv), f"{seq_id}.csv"
                )

                os.makedirs(os.path.abspath(self.usr_input.csv), exist_ok=True)

                with open(csv_path, "w", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    for key, value in self.rna_scoring.scores_dict.items():
                        writer.writerow([key, value])
                    print(f"CSV file successfully saved in {csv_path}")

            if self.usr_input.plot:
                plot_path = os.path.join(
                    os.path.abspath(self.usr_input.plot), f"{seq_id}.png"
                )
                os.makedirs(os.path.abspath(self.usr_input.plot), exist_ok=True)

                self.rna_scoring.plot_rna_kde_to_file(
                    self.usr_input.rna_seq,
                    self.usr_input.window_size,
                    plot_path,
                    x_min=self.usr_input.x_min,
                    x_max=self.usr_input.x_max,
                    title=self.usr_input.title,
                    wrap_title=self.usr_input.wrap_title,
                )
                print(f"Plot(s) successfully saved in {plot_path}")


class UserInputHandler:
    """
    This class is used to handle the user input and parse it into a structured format
    """

    def __init__(self):
        self.parser = self._build_parser()

    def _build_parser(self):
        parser = argparse.ArgumentParser(
            description=f"RRM-RNA scoring version {__version__}"
        )

        input_arg = parser.add_mutually_exclusive_group(required=True)
        input_arg.add_argument(
            "-u", "--uniprot", help="UniProt identifier", metavar="UNIPROT_ID"
        )
        input_arg.add_argument(
            "-f", "--fasta", help="Fasta file path", metavar="/path/to/input.fasta"
        )

        feat_arg = parser.add_mutually_exclusive_group(required=True)
        feat_arg.add_argument(
            "-r", "--rna", help="RNA sequence", metavar="RNA_SEQUENCE"
        )
        feat_arg.add_argument(
            "-t",
            "--top",
            action="store_true",
            help="To find the top scoring RNA fragments",
        )

        parser.add_argument(
            "-w",
            "--window_size",
            required=False,
            help="The window size to test",
            metavar="N",
        )
        parser.add_argument(
            "-j",
            "--json",
            help="Store the results in a json file in the declared directory path",
            metavar="/path/to/output",
        )
        parser.add_argument(
            "-c",
            "--csv",
            help="Store the results in a CSV file in the declared directory path",
            metavar="/path/to/output",
        )
        parser.add_argument(
            "-p",
            "--plot",
            help="Store the plots in the declared directory path",
            metavar="/path/to/output",
        )
        parser.add_argument(
            "-a",
            "--aligned",
            help="Store the aligned sequences in the declared directory path",
            metavar="/path/to/output",
        )
        parser.add_argument(
            "--x_min",
            type=float,
            default=-0.9,
            help="Minimum value for x-axis in plots (default: -0.9)",
        )
        parser.add_argument(
            "--x_max",
            type=float,
            default=1.0,
            help="Maximum value for x-axis in plots (default: 1.0)",
        )
        parser.add_argument(
            "--title",
            type=str,
            help="Title for the generated plots",
        )
        parser.add_argument(
            "--wrap-title",
            action="store_true",
            help="Wrap long titles to multiple lines",
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            help="show RRM-RNA scoring version number and exit",
            version=f"RRM-RNA scoring {__version__}",
        )

        return parser

    def parse_args(self):
        """
        Parse the user input and return it in a structured format
        """

        usr_input = UserInput()

        input_files = self.parser.parse_args()

        usr_input.fasta_file = input_files.fasta
        usr_input.up_id = input_files.uniprot

        usr_input.rna_seq = input_files.rna
        usr_input.top = input_files.top

        # User defined outputs
        usr_input.json = input_files.json
        usr_input.csv = input_files.csv
        usr_input.plot = input_files.plot
        usr_input.aligned = input_files.aligned
        usr_input.x_min = input_files.x_min
        usr_input.x_max = input_files.x_max
        usr_input.title = input_files.title
        usr_input.wrap_title = input_files.wrap_title

        # Default window size
        if input_files.window_size:
            usr_input.window_size = int(input_files.window_size)

            if usr_input.window_size == 3:
                usr_input.rna_pos_range = (3, 6)

            elif usr_input.window_size == 5:
                usr_input.rna_pos_range = (2, 7)

            else:
                sys.exit("Only 3 and 5 nucleotide windows are accepted")
        else:  # Default ws=5 if not in input
            usr_input.window_size = 5
            usr_input.rna_pos_range = (2, 7)

        return usr_input


class UserInput:
    """
    This class is used to store the user input in a structured way
    """

    def __init__(self):
        self.fasta_file = None
        self.up_id = None
        self.rna_seq = None
        self.top = None
        self.json = None
        self.csv = None
        self.plot = None
        self.aligned = None
        self.window_size = None
        self.rna_pos_range = None
        self.x_min = None
        self.x_max = None
        self.title = None
        self.wrap_title = False


if __name__ == "__main__":
    main()
