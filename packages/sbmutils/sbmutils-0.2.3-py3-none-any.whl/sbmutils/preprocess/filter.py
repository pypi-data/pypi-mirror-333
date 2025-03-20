import warnings
from pybiomart import Server
from gtfparse import read_gtf
from tqdm import tqdm
import pandas as pd


def entrez_filtering(fpkm, mapper):
    fpkm_mapped = fpkm.merge(mapper, left_index=True, right_on="gene_id", how="left").reset_index(drop=True)

    fpkm_mapped = fpkm_mapped[fpkm_mapped.groupby("gene_id")["entrez_id"].transform("nunique") == 1]
    
    fpkm_mapped["FPKM_sum"] = fpkm_mapped.iloc[:, :-4].sum(axis=1)
    fpkm_mapped = fpkm_mapped.sort_values(by="FPKM_sum", ascending=False).groupby("entrez_id").first().reset_index()
    fpkm_mapped = fpkm_mapped.drop(columns=["FPKM_sum", "gene_id"])

    fpkm_mapped = fpkm_mapped.set_index(["entrez_id", "entrez_accession", "entrez_description"])
    return fpkm_mapped


def get_gene_id_to_entrez_mapper(gene_ids,
                                 host="http://www.ensembl.org/",
                                 dataset="hsapiens_gene_ensembl",
                                 attributes=["ensembl_gene_id",
                                             "entrezgene_id",
                                             "entrezgene_accession",
                                             "entrezgene_description"],
                                 chunk_size=100):
    gene_ids = [x.split(".")[0] for x in gene_ids]

    server = Server(host=host)
    dataset = server.marts["ENSEMBL_MART_ENSEMBL"].datasets[dataset]

    def chunker(seq, size):
        for pos in range(0, len(seq), size):
            yield seq[pos:pos + size]
    
    results = []
    for chunk in tqdm(list(chunker(gene_ids, chunk_size)), desc="Mapping gene IDs"):
        mapper_chunk = dataset.query(attributes=attributes,
                                    filters={"link_ensembl_gene_id": chunk})
        results.append(mapper_chunk)
    
    combined_mapper = pd.concat(results)
    return combined_mapper


def protein_coding_filtering(fpkm, gtf):
    if "gene_biotype" in gtf.columns:
        protein_coding_genes = gtf[gtf["gene_biotype"] == "protein_coding"]["gene_id"].unique()
    else:
        protein_coding_genes = gtf[gtf["gene_type"] == "protein_coding"]["gene_id"].unique()
    fpkm = fpkm.loc[fpkm.index.isin(protein_coding_genes)]
    return fpkm


def parse_gtf(gtf_file):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        gtf = read_gtf(gtf_file)
    return gtf
