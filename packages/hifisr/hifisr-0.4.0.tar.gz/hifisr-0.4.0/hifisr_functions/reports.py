import hifisr_functions.base as hfbase
import numpy as np
import pandas as pd
from Bio import SeqIO
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import sys
import os


def get_fastq_stats(prefix, sample_fastq_path, soft_paths_dict, threads):
    commands = soft_paths_dict.get("seqkit") + " stat -a -T " + sample_fastq_path + " -j " + threads
    output_lines_1 = hfbase.get_cli_output_lines(commands)
    total_read_number = output_lines_1[1].split("\t")[3]
    total_bases = output_lines_1[1].split("\t")[4]
    id_length_qual_file = prefix + "_id_length_qual.txt"
    commands = soft_paths_dict.get("seqkit") + " fx2tab -j " + threads + " -qlni " + sample_fastq_path + " > " + id_length_qual_file
    hfbase.get_cli_output_lines(commands) # ID, length, qual 
    return id_length_qual_file, total_read_number, total_bases


def plot_length_qual(prefix, sample_platform, id_length_qual_file, total_read_number, total_bases):
    id_length_qual_lines = hfbase.get_file_lines(id_length_qual_file)
    length_list = [ int(line.split("\t")[1]) for line in id_length_qual_lines ]
    qual_list = [ float(line.split("\t")[2]) for line in id_length_qual_lines ]
    length_bin_dict = {
        "HiFi": (50000, 500),
        "CLR": (50000, 500),
        "ONT": (50000, 500),
        "ultra-long": (100000, 500),
        "Short": (500, 10),
    }
    fig = plt.figure(figsize=(10, 8))
    gs = gridspec.GridSpec(13, 2)
    ax1 = plt.subplot(gs[0:5, :])
    ax2 = plt.subplot(gs[7:12, :])
    axs = [ax1, ax2]
    # plot length distribution
    length_bins = np.arange(0, length_bin_dict.get(sample_platform)[0], length_bin_dict.get(sample_platform)[1])
    axs[0].hist(length_list, bins=length_bins, color="blue", alpha=0.5, edgecolor="black", linewidth=0.5)
    axs[0].axvline(sum(length_list)/len(length_list), color="red", linestyle="--")
    axs[0].set_xlim([0, length_bin_dict.get(sample_platform)[0]])
    axs[0].grid(True, alpha=0.5)
    axs[0].spines['top'].set_visible(False)
    axs[0].spines['right'].set_visible(False)
    axs[0].set_xlabel("Read Length")
    axs[0].set_ylabel("Counts")
    axs[0].set_title("total_read_number = " + total_read_number + "; total_bases = " + total_bases)
    axs[1].hist(qual_list, bins=np.arange(0, 100, 1), color="red", alpha=0.5, edgecolor="black", linewidth=0.5)
    axs[1].axvline(sum(qual_list)/len(qual_list), color="red", linestyle="--")
    axs[1].set_xlim([0, 100])
    axs[1].grid(True, alpha=0.5)
    axs[1].spines['top'].set_visible(False)
    axs[1].spines['right'].set_visible(False)
    axs[1].set_xlabel("Read Quality")
    axs[1].set_ylabel("Counts")
    axs[1].set_title("total_read_number = " + total_read_number + "; total_bases = " + total_bases)
    plt.savefig(prefix + "_length_qual_distribution.pdf")
    # clear the figure
    plt.clf()
    # create 2-D histogram for length and quality
    fig = plt.figure(figsize=(10, 8))
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0, 0])
    white_to_red = mcolors.LinearSegmentedColormap.from_list("white_red", ["white", "red"])
    hb = plt.hexbin(length_list, qual_list, gridsize=30, cmap=white_to_red, edgecolors="lightgray")
    cb = plt.colorbar(hb, label="Count in bin")
    ax.set_xlabel("Read Length")
    ax.set_ylabel("Read Quality")
    ax.set_title("total_read_number = " + total_read_number + "; total_bases = " + total_bases)
    plt.savefig(prefix + "_length_qual_2d_distribution.pdf")
    plt.close()
    return


def plot_bubble_type_2_rep_raw(table_file, IDs_dir, ref_fasta):
    if os.path.exists(table_file):
        df = pd.read_excel(table_file, sheet_name='Sheet1') 
    else:
        return
    FL_ids_files = [IDs_dir + "/" + file for file in os.listdir(IDs_dir) if file.endswith("_FL_ids.txt")]
    FL_count = 0
    for file in FL_ids_files:
        FL_count += len(hfbase.get_file_lines(file))
    ref_len = len(SeqIO.read(ref_fasta, "fasta").seq) # mito_rotated_flye_polish_1.fasta
    df['subgroup_count_norm'] = df['subgroup_count'] / FL_count * 10000  # normalize to 10000 FL reads
    fig = plt.figure(figsize=(10, 10)) # set figure size with
    df["color"] = df["mid_olp_1"].apply(lambda x: "#FF00FF" if x >= 1000 else "#00FF00" if x >= 300 else "#0016FF" if x >= 200 else "#E8720C" if x >= 100 else "#E6E600" if x >= 50 else "#B0B0B0") # set colors for the bubble plot by the mid_olp_1
    df["se1"] = df["(se1, ss2)"].apply(lambda x: int(x.split(",")[0].lstrip("("))) # (se1, ss2)
    df["ss2"] = df["(se1, ss2)"].apply(lambda x: int(x.split(",")[1].rstrip(")"))) # (se1, ss2)
    size_ratio = 10
    alpha_value = 0.5 # df["alpha"] = 0.5
    if len(df) > 0:
        plt.scatter(df['se1'], df['ss2'], s=df['subgroup_count_norm']*size_ratio, c=df['color'], alpha=alpha_value, linewidths=0)
        plt.grid(True, alpha=0.5)
        plt.xlim(1, ref_len)
        plt.ylim(1, ref_len)
        plt.savefig('bubble_type_2_rep_raw.pdf')
    plt.close()
    return


def plot_coverage(cov_file_1, cov_file_2, cov_file_3, start, end, fig_length=12, fig_height=3):
    if os.path.exists(cov_file_1):
        cov_1 = np.loadtxt(cov_file_1, dtype=int, usecols=1)
    else:
        print("No coverage file found for " + cov_file_1, file=sys.stderr)
    if os.path.exists(cov_file_2):
        cov_2 = np.loadtxt(cov_file_2, dtype=int, usecols=1)
    else:
        cov_2 = np.zeros(cov_1.shape)
    if os.path.exists(cov_file_3):
        cov_3 = np.loadtxt(cov_file_3, dtype=int, usecols=1)
    else:
        cov_3 = np.zeros(cov_1.shape)
    cov_combine = cov_1 + cov_2
    fig = plt.figure(figsize=(fig_length, fig_height), dpi=600)
    plt.plot(cov_combine[(start-1):end], color="#EAB13E", label="FL")
    plt.plot(cov_1[(start-1):end], color="#D1D1D1", label="partial")
    plt.fill_between(np.arange(start-1, end), cov_combine[(start-1):end], 1, color="#EAB13E", alpha=1) # run long time
    plt.fill_between(np.arange(start-1, end), cov_1[(start-1):end], 1, color="#D1D1D1", alpha=1)
    plt.plot(cov_3[(start-1):end], color="#5CAB38", label="variant", linewidth=1)
    plt.grid(True, alpha=0.5)
    ax = plt.gca()
    ax.set_xlim([start, end+1])
    max_y = int(np.max(cov_combine[(start-1):end]))
    ax.set_ylim([0, max_y+100])
    plt.savefig('coverage_plot.pdf')
    plt.savefig('coverage_plot.png')
    plt.close()
    return

