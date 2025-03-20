import hifisr_functions.base as hfbase
from Bio import SeqIO
import polars as pl
import sys


def split_mtpt_reads(sample_index, sample_fastq_path, sample_platform, mito_fa, plastid_fa, soft_paths_dict, threads):
    platform_dict = {
            "HiFi": "map-hifi",
            "CLR": "map-pb",
            "ONT": "map-ont",
            "ultra-long": "map-ont",
        }
    command_1 = soft_paths_dict.get("seqkit") + " seq -ni " + mito_fa + " > mito_ids.txt"
    command_2 = soft_paths_dict.get("seqkit") + " seq -ni " + plastid_fa + " > plastid_ids.txt"
    command_3 = "cat " + mito_fa + " " + plastid_fa + " > mtpt.fa"
    command_4 = soft_paths_dict.get("minimap2") + " -t " + threads + " -ax " + platform_dict.get(sample_platform) + " mtpt.fa " + sample_fastq_path
    command_5 = soft_paths_dict.get("samtools") + " view -Sb -F 4 -@ " + threads + " - "
    command_6 = soft_paths_dict.get("samtools") + " sort -@ " + threads + " - -o reads.sorted.bam"
    command_7 = soft_paths_dict.get("samtools") + " index reads.sorted.bam"
    command_8 = soft_paths_dict.get("bamtools") + " split -in reads.sorted.bam -reference"
    command_9 = "rm -rf mito.fastq plastid.fastq"
    command_10 = "cat mito_ids.txt | while read ID; do " + soft_paths_dict.get("samtools") + " fastq reads.sorted.REF_${ID}.bam -@ " + threads + " >> " + sample_index + "_mito.fastq; done"
    command_11 = "cat plastid_ids.txt | while read ID; do " + soft_paths_dict.get("samtools") + " fastq reads.sorted.REF_${ID}.bam -@ " + threads + " >> " + sample_index + "_plastid.fastq; done"
    command_12 = "rm -rf mito_ids.txt plastid_ids.txt mtpt.fa reads.sorted.bam reads.sorted.bam.bai reads.sorted.*.bam" 
    commands = command_1 + " ; " + command_2 + " ; " + command_3 + " ; " + command_4 + " | " + command_5 + " | " + command_6 + " && " + command_7 + " && " + command_8 + " ; " + command_9 + " ; " + command_10 + " ; " + command_11 + " ; " + command_12
    hfbase.get_cli_output_lines(commands, side_effect = True)
    return


def filt_length_qual(prefix, id_length_qual_file, filt_length=0, filt_qual=0):
    df = pl.read_csv(id_length_qual_file, separator="\t", has_header=False, new_columns=["id", "length", "qual"])
    df = df.with_columns([
        pl.col("length").cast(pl.Int64),
        pl.col("qual").cast(pl.Float64)
    ])
    df_filtered = df.filter((pl.col("length") >= filt_length) & (pl.col("qual") >= filt_qual))
    filt_read_number = str(df_filtered.shape[0])
    filt_bases = str(df_filtered["length"].sum())
    id_length_qual_file_filt = "filt_" + prefix + "_id_length_qual.txt"
    df_filtered.write_csv(id_length_qual_file_filt, separator="\t", include_header=False)
    return id_length_qual_file_filt, filt_read_number, filt_bases


def random_sampling(prefix, id_length_qual_file, sample_number):
    df = pl.read_csv(id_length_qual_file, separator="\t", has_header=False, new_columns=["id", "length", "qual"])
    df = df.with_columns([
        pl.col("length").cast(pl.Int64),
        pl.col("qual").cast(pl.Float64)
    ])
    total_rows = int(df.shape[0])
    if sample_number > total_rows:
        sample_number = total_rows
    df_sampled = df.sample(n=sample_number, with_replacement=False, seed=2025)
    sample_read_number = str(df_sampled.shape[0])
    sample_bases = str(df_sampled["length"].sum())
    id_length_qual_file_sampled = prefix + "_id_length_qual.txt"
    df_sampled.write_csv(id_length_qual_file_sampled, separator="\t", include_header=False)
    return id_length_qual_file_sampled, sample_read_number, sample_bases


def replace_reads_id(reads_file, new_reads_file):
    with open(reads_file, "rt") as fin, open(new_reads_file, "wt") as fout:
        for record in SeqIO.parse(fin, "fasta"):
            record.id = record.id.replace("/", "_")
            record.description = ""
            SeqIO.write(record, fout, "fasta")
    return new_reads_file


def cal_ID_coverage(prefix, ref_fasta, reads_fasta, sample_platform, soft_paths_dict, threads):
    platform_dict = {
            "HiFi": "map-hifi",
            "CLR": "map-pb",
            "ONT": "map-ont",
            "ultra-long": "map-ont",
        }
    command_1 = soft_paths_dict.get("minimap2") + " -t " + threads + " -ax " + platform_dict.get(sample_platform) + " " + ref_fasta + " " + reads_fasta
    command_2 = soft_paths_dict.get("samtools") + " view -Sb -F 0x100 -@ " + threads + " -"
    command_3 = soft_paths_dict.get("samtools") + " sort -@ " + threads + " -o " + prefix + ".sorted.bam "
    command_4 = soft_paths_dict.get("samtools") + " index -@ " + threads + " " + prefix + ".sorted.bam "
    command_5 = soft_paths_dict.get("samtools") + " depth -a -J -@ " + threads + " " + prefix + ".sorted.bam | cut -f2- > " + prefix + "_cov.txt"
    command_6 = "rm " + prefix + ".sorted.bam " + prefix + ".sorted.bam.bai"
    commands = command_1 + " | " + command_2 + " | " + command_3 + " ; " + command_4 + " ; " + command_5 + " ; " + command_6
    hfbase.get_cli_output_lines(commands, side_effect = True)
    return


