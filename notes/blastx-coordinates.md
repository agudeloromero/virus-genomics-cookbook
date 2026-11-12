# Reading blastx coordinates: nucleotides or amino acids?

**The problem.** A blastx table mixes units across its columns and never tells you which is which. If you read them wrongly, you extract the wrong region of your contig.

**Requirements:** BLAST+ (tested with 2.12.0), Python 3
**Time:** about 20 minutes

---

## Contents

1. [The answer](#the-answer)
2. [Why it matters](#why-it-matters)
3. [Documentation](#documentation)
4. [Finding it in the console](#finding-it-in-the-console)
5. [Videos](#videos)
6. [Toy exercise](#toy-exercise)
7. [Questions](#questions)
8. [Cheat sheet](#cheat-sheet)
9. [References](#references)

---

## The answer

In **blastx**, a nucleotide query is translated in all six reading frames and searched against a protein database.

| Columns | Side | Unit |
| --- | --- | --- |
| `qstart`, `qend`, `qlen` | Query (your DNA) | **nt** |
| `sstart`, `send`, `slen` | Subject (the protein) | **aa** |
| `length`, `mismatch`, `gapopen`, `pident` | The translated alignment | **aa** |

> [!TIP]
> The protein side is counted in amino acids, the DNA side in nucleotides.
> Quick check for blastx: `(qend − qstart + 1) / 3 ≈ length`

---

## Why it matters

The output table never states which unit a column uses. If you mix them up, you will:

- Extract the wrong region of your contig when you pull out a gene (off by a factor of 3).
- Misjudge coverage, e.g. think a hit covers one third of your contig when it covers all of it.
- Misplace genes when mapping several hits along a viral or microbial contig.

---

## Documentation

| Resource | What to read |
| --- | --- |
| [NCBI BLAST+ Command Line Applications User Manual](https://ncbi.nlm.nih.gov/books/NBK279675) | Full manual; the options appendix lists the 12 default `-outfmt 6` columns (the `std` keyword) |
| [Custom output format (PDF)](https://ncbi.nlm.nih.gov/books/NBK569862/pdf/Bookshelf_NBK569862.pdf) | How to choose your own columns with `-outfmt "6 ..."` |
| [BLAST Tabular Output Guide](https://ibl-bioinformatics-wiki.readthedocs.io/basic_tools/tabular_output_guide.html) | Plain-language description of every column, including frame and strand fields |

> [!NOTE]
> None of these pages states explicitly that blastx query coordinates are in nt and subject coordinates in aa. The manual only describes `qstart` as the start of the alignment in the query. That is why the exercise below has you prove it yourself.

---

## Finding it in the console

Every BLAST+ program documents its own columns; no internet needed.

```bash
# 1. Check BLAST is installed
blastx -version

# 2. Browse the full help (type /outfmt to search, q to quit)
blastx -help | less

# 3. Jump to the list of output columns
blastx -help | grep -A 70 "outfmt <String>"

# 4. Look up specific columns
blastx -help | grep -E " (qstart|qend|sstart|send|length|qframe) means"
```

Expected output of step 4:

```
    qstart means Start of alignment in query
      qend means End of alignment in query
    sstart means Start of alignment in subject
      send means End of alignment in subject
    length means Alignment length
    qframe means Query frame
```

The help tells you *where* each position is, but not *in which unit*.

---

## Videos

Background viewing, in suggested order. None focuses on the nt/aa coordinate question, so use the exercise for that.

| # | Video | Topic |
| --- | --- | --- |
| 1 | [Bioinf Class 9C: BLASTN, BLASTP, BLASTX, TBLASTN and TBLASTX](https://www.youtube.com/watch?v=xT0EM44ucRI) | The five BLAST programs and which sequence gets translated |
| 2 | [Translated Nucleotide to Protein BLAST: BLASTX](https://www.youtube.com/watch?v=sFXvSpq4LDs) | How blastx translates a DNA query |
| 3 | [ncbi-blast+ -outfmt](https://www.youtube.com/watch?v=KlRRx2VcRq8) | Choosing tabular output columns |
| 4 | [BLAST from the command line, part 1](https://www.youtube.com/watch?v=1AzujLnr3RM) and [part 2](https://www.youtube.com/watch?v=bDL_TNq_RtI) | Running BLAST+ locally |

---

## Toy exercise

You will build a DNA contig where **you** know exactly which bases encode which amino acids, then compare BLAST's output with what you know.

### Step 1. Install BLAST+

```bash
conda install -c bioconda blast    # or: sudo apt install ncbi-blast+
blastx -version
```

### Step 2. Build the toy sequences

Run [`scripts/make_toy.py`](../scripts/make_toy.py). It writes three FASTA files into whatever directory you run it from:

```bash
git clone https://github.com/agudeloromero/virus-genomics-cookbook.git
mkdir -p ~/blastx-exercise && cd ~/blastx-exercise
python3 ../virus-genomics-cookbook/scripts/make_toy.py
```

```
protein : 221 aa
contig  : 600 nt
coding  : nt 101-550 encodes aa 1-150
wrote protein.fa, contig.fa, contig_rc.fa
```

What you now know for certain:

```
contig1 (600 nt)
|-- padding --|-------------- coding --------------|- padding -|
1           100 101                              550 551     600
                 encodes aa 1-150 of myProtein (221 aa)
```

### Step 3. Predict before running

Write down your guess:

- If BLAST counted the query in **aa**, `qstart`/`qend` would be about **34–184**.
- If it counts the query in **nt**, they would be **101–550**.

### Step 4. Run blastx

```bash
COLS="6 qseqid sseqid pident length qstart qend sstart send qframe qlen slen evalue"
blastx -query contig.fa -subject protein.fa -outfmt "$COLS"
```

Expected output:

```
contig1  myProtein  100.000  150  101  550  1  150  2  600  221  5.61e-112
```

### Step 5. Compare each number with what you built

| Column | Value | Corresponds to | Unit |
| --- | --- | --- | --- |
| `qstart`, `qend` | 101, 550 | The coding bases of the contig | **nt** |
| `sstart`, `send` | 1, 150 | The first 150 residues of the protein | **aa** |
| `length` | 150 | Number of aligned residues | **aa** |
| `qlen` | 600 | Contig length | **nt** |
| `slen` | 221 | Protein length | **aa** |
| `qframe` | +2 | Plus strand, starting at base 101: ((101 − 1) mod 3) + 1 = 2 | frame |

**Conclusion: query side = nucleotides, subject side = amino acids.**

### Step 6. Check with arithmetic

If the query is in nt, the query span divided by 3 equals `length`:

```bash
blastx -query contig.fa -subject protein.fa -outfmt "$COLS" \
  | awk '{span=$6-$5+1; print "span =", span, "nt; /3 =", span/3, "; length =", $4}'
```

Expected: `span = 450 nt; /3 = 150 ; length = 150`

> [!TIP]
> Use this check on any real blastx output. With gaps it will be close rather than exact.

### Step 7. Reverse strand

```bash
blastx -query contig_rc.fa -subject protein.fa -outfmt "$COLS"
```

Expected:

```
contig1_rc  myProtein  100.000  150  500  51  1  150  -2  600  221  5.61e-112
```

`qstart > qend` and `qframe = -2` tell you the gene is on the minus strand. The span is still 500 − 51 + 1 = 450 nt, so the values are still nucleotides.

### Step 8. Flip the programs with tblastn

```bash
tblastn -query protein.fa -subject contig.fa \
  -outfmt "6 qseqid sseqid pident length qstart qend sstart send sframe qlen slen"
```

Expected:

```
myProtein  contig1  99.338  151  1  151  101  553  2  221  600
```

The units have swapped sides: the **query is now aa** and the **subject is nt**.

> [!NOTE]
> The hit runs to aa 151 and nt 553, one codon past what you built, at 99.3% identity. The first padding codon (TTT, phenylalanine) scored well enough for BLAST to extend into it. Real alignments can also run a few residues past a true gene boundary.

---

## Questions

**Q1.** A blastx row has `qstart 1201`, `qend 1500`, `length 100`. How many nt of the contig does the hit cover, and is that consistent?

<details>
<summary>Answer</summary>

300 nt (1500 − 1201 + 1). 300 / 3 = 100 aa, which matches `length`.

</details>

**Q2.** A blastx row has `qstart 900`, `qend 301`. Which strand is the hit on, and how long is the query span?

<details>
<summary>Answer</summary>

Minus strand (`qstart > qend`). Span = 900 − 301 + 1 = 600 nt.

</details>

**Q3.** You want to extract the hit region from your contig with `samtools faidx`. Which columns do you use, and do you need to convert units?

<details>
<summary>Answer</summary>

Use `qstart` and `qend` directly (swap them if `qstart > qend`, and reverse-complement the result). They are already in nt, so no conversion is needed.

</details>

**Q4.** In tblastn output, which columns would you use to extract the matching region from the DNA sequence?

<details>
<summary>Answer</summary>

`sstart` and `send`. In tblastn the subject is the DNA, so those are the nt coordinates.

</details>

---

## Cheat sheet

| Program | Query → Subject | `qstart`/`qend`, `qlen` | `sstart`/`send`, `slen` | `length`, `mismatch` | Minus strand shows as |
| --- | --- | --- | --- | --- | --- |
| blastn | DNA → DNA | nt | nt | nt | `sstart > send` |
| blastp | protein → protein | aa | aa | aa | n/a |
| **blastx** | **DNA → protein** | **nt** | **aa** | **aa** | **`qstart > qend`**, negative `qframe` |
| tblastn | protein → DNA | aa | nt | aa | `sstart > send`, negative `sframe` |
| tblastx | DNA → DNA, both translated | nt | nt | aa | either side reversed |

DIAMOND blastx uses the same `-outfmt 6` layout and follows the same rules.

---

## References

- Camacho C, Coulouris G, Avagyan V, Ma N, Papadopoulos J, Bealer K, Madden TL. BLAST+: architecture and applications. *BMC Bioinformatics*. 2009;10:421. doi:[10.1186/1471-2105-10-421](https://doi.org/10.1186/1471-2105-10-421)
- NCBI. [BLAST® Command Line Applications User Manual](https://ncbi.nlm.nih.gov/books/NBK279675). Bethesda (MD): National Center for Biotechnology Information; 2008–.
- Buchfink B, Xie C, Huson DH. Fast and sensitive protein alignment using DIAMOND. *Nature Methods*. 2015;12:59–60. doi:[10.1038/nmeth.3176](https://doi.org/10.1038/nmeth.3176)

---

← Back to the [cookbook index](../README.md)
