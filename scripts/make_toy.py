#!/usr/bin/env python3
"""Build toy sequences for the blastx coordinate exercise.

Creates a DNA contig in which you know exactly which bases encode which amino
acids, so you can compare BLAST's reported coordinates against the truth.

Writes three FASTA files into the current directory:
    protein.fa     a made-up 221 aa protein
    contig.fa      a 600 nt contig; bases 101-550 encode aa 1-150 of that protein
    contig_rc.fa   the reverse complement of that contig

See notes/blastx-coordinates.md for the exercise this belongs to.
"""

# A made-up 221 aa protein
PROTEIN = (
    "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKR"
    "QTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFG"
    "LAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDW"
)

# One codon per amino acid, so the mapping is unambiguous
CODON = {
    "A": "GCT", "R": "CGT", "N": "AAC", "D": "GAC", "C": "TGC",
    "Q": "CAG", "E": "GAA", "G": "GGT", "H": "CAC", "I": "ATC",
    "L": "CTG", "K": "AAA", "M": "ATG", "F": "TTC", "P": "CCG",
    "S": "TCT", "T": "ACC", "W": "TGG", "Y": "TAC", "V": "GTT",
}

N_CODING_AA = 150   # how many residues to encode in the contig
PAD_5 = 100         # nt of padding before the coding region
PAD_3 = 50          # nt of padding after it


def main() -> None:
    coding = "".join(CODON[aa] for aa in PROTEIN[:N_CODING_AA])
    contig = "A" * PAD_5 + coding + "T" * PAD_3
    rc = contig[::-1].translate(str.maketrans("ACGT", "TGCA"))

    with open("protein.fa", "w") as fh:
        fh.write(">myProtein\n" + PROTEIN + "\n")
    with open("contig.fa", "w") as fh:
        fh.write(">contig1\n" + contig + "\n")
    with open("contig_rc.fa", "w") as fh:
        fh.write(">contig1_rc\n" + rc + "\n")

    coding_start = PAD_5 + 1
    coding_end = PAD_5 + len(coding)
    print(f"protein : {len(PROTEIN)} aa")
    print(f"contig  : {len(contig)} nt")
    print(f"coding  : nt {coding_start}-{coding_end} encodes aa 1-{N_CODING_AA}")
    print("wrote protein.fa, contig.fa, contig_rc.fa")


if __name__ == "__main__":
    main()
