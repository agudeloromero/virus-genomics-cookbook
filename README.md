# virus-genomics-cookbook

Short, practical recipes for virus genomics and virome analysis.

## What this is

A growing collection of notes on the things that trip people up when working with viral sequence data: output formats that mean something other than what they appear to, steps the official documentation leaves ambiguous, and conventions you only learn by getting them wrong.

Each recipe is self-contained and follows the same shape: the problem, the answer, the commands, real output, and a way to check you got it right. Written with students and newcomers in mind, though the fiddly details are there for everyone.

Maintained by [Patricia Agudelo-Romero](https://github.com/agudeloromero).

## Recipes

| Recipe | What it covers |
| --- | --- |
| [Reading blastx coordinates: nucleotides or amino acids?](notes/blastx-coordinates.md) | Which BLAST tabular columns are counted in nucleotides and which in amino acids, how to look it up in the console, and a toy exercise that proves it |

Planned: assembly of viral contigs, completeness and contamination checks, taxonomy assignment, annotating hypothetical proteins, pipeline gotchas.

## How to use it

Read any recipe straight from this page, or clone the repo to run the examples:

```bash
git clone https://github.com/agudeloromero/virus-genomics-cookbook.git
cd virus-genomics-cookbook
```

Each recipe states its own requirements and time estimate at the top. Helper scripts live in [`scripts/`](scripts/), so you can run them directly instead of copying code out of the Markdown.

## Layout

```
virus-genomics-cookbook/
├── README.md            index of recipes
├── notes/               one Markdown file per recipe
└── scripts/             runnable helpers used by the recipes
```

## Conventions

So that recipes stay consistent as the collection grows:

- One recipe per file in `notes/`, named in lowercase with hyphens, e.g. `blastx-coordinates.md`.
- Open with a one-line statement of the problem, then the answer, then the detail. Readers in a hurry should get what they need from the first screen.
- Show real output, not invented output. If a command appears in a recipe, it has been run.
- State the tool versions used. Output formats change between releases.
- Where the official documentation is silent or ambiguous, say so, and give the reader a way to verify the answer themselves.
- Put anything longer than a few lines of code in `scripts/` and link to it.
