import warnings
import numpy as np
import pandas as pd
from tqdm import tqdm
from inmoose.pycombat import pycombat_norm, pycombat_seq
from gtfparse import read_gtf
import pyranges as pr


def combat(counts, batch):
    return pycombat_norm(counts, batch)


def combat_seq(counts, batch):
    return pycombat_seq(counts, batch)


def counts_to_fpkm(counts, gtf):
    
    def merge_intervals_per_gene(exons):
        lengths = {}
        for gene, group in tqdm(exons.groupby("gene_id"), desc="Merging intervals per gene..."):
            gr = pr.PyRanges(group)
            gr = gr.merge()
            length = (gr.End - gr.Start + 1).sum()
            lengths[gene] = length
        return pd.Series(lengths)

    exons = gtf[gtf['feature'] == "exon"]
    exons = exons[["seqname", "start", "end", "gene_id"]]
    exons.columns = ["Chromosome", "Start", "End", "gene_id"]
    
    lengths = merge_intervals_per_gene(exons)
    lengths = lengths.reindex(counts.index).fillna(0)
    library_size = counts.sum(axis=0)
    
    fpkm = (counts * 1e9).div(lengths, axis=0).div(library_size, axis=1)
    fpkm = fpkm.replace([np.inf, -np.inf], 0)
    return fpkm

