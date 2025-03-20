from Bio import SeqIO
import hifisr_functions.base as hfbase
import numpy as np
import sys


def replace_fasta_id(genome, input_fasta_path, output_fasta_path):
    records = list(SeqIO.parse(input_fasta_path, "fasta"))
    count = 1
    fout = open(output_fasta_path, "wt")
    for record in records:
        ID = genome + "_" + str(count) + " [" + record.description + "]"
        count += 1
        print(">" + ID, file=fout)
        print(record.seq, file=fout)
    if count >= 3:
        print("There are", count - 1, "contigs in the input reference.", file=sys.stderr)
    elif count == 2:
        print("There is", count - 1, "contig in the input reference.", file=sys.stderr)
    fout.close()


def get_subseq(ref, start, end, flank=0):
    subseq = ref[start-1:end]
    subseq_flank_start = start-1-flank
    subseq_flank_end = end+flank
    if subseq_flank_start < 0:
        subseq_flank_start = 0
    if subseq_flank_end > len(ref):
        subseq_flank_end = len(ref)
    subseq_flank = ref[subseq_flank_start:subseq_flank_end]
    return subseq, subseq_flank


def rotate_ref_to_non_repeat_region(genome, genome_fasta_path, soft_paths_dict, rotation=False):
    ref_records = list(SeqIO.parse(genome_fasta_path, "fasta"))
    if len(ref_records) != 1:
        print("Error: fasta has more than one record.")
        return
    commands = soft_paths_dict.get("blastn") + " -query " + genome_fasta_path + " -subject " + genome_fasta_path + " -outfmt 6"
    blastn_lines = hfbase.get_cli_output_lines(commands, side_effect = False)
    repeat_pos_array = np.zeros(len(ref_records[0].seq), dtype=int)
    for line in blastn_lines[1:]: # skip the first line
        fields = line.split("\t")
        q_start = int(fields[6])
        q_end = int(fields[7])
        for i in range(q_start-1, q_end):
            repeat_pos_array[i] += 1
    if rotation:
        non_repeat_region_info = []
        while 0 in repeat_pos_array:
            non_repeat_region_info, repeat_pos_array = find_continous_zeros(non_repeat_region_info, repeat_pos_array)
            # find the largest non-repeat region
        non_repeat_region_info.sort(key=lambda x: x[2], reverse=True)
        non_start = non_repeat_region_info[0][0]
        non_end = non_repeat_region_info[0][1]
        length = non_repeat_region_info[0][2]
        rot_step = (non_end + non_start) // 2
        if length > 5000:
            print("The largest non-repeat region is " + str(length) + " bp long.", file=sys.stderr)
            rotate_fasta(genome_fasta_path, genome + "_rotated_" + str(rot_step) + ".fasta", rot_step)
        else:
            print("The largest non-repeat region is less than 5 kb.", file=sys.stderr)
        return rot_step
    else:
        return 0


def find_continous_zeros(info_list, repeat_pos_array):
    for i in range(0, len(repeat_pos_array)):
        if repeat_pos_array[i] == 0:
            piece_start = i
            piece_end = i
            repeat_pos_array[i] = 1
            break
    for i in range(piece_start+1, len(repeat_pos_array)):
        if repeat_pos_array[i] == 0:
            piece_end = i
            repeat_pos_array[i] = 1
            if i == len(repeat_pos_array) - 1:
                length = piece_end - piece_start + 1
                info_list.append((piece_start, piece_end, length))
                break
        else:
            length = piece_end - piece_start + 1
            info_list.append((piece_start, piece_end, length))
            break
    return info_list, repeat_pos_array


def rotate_fasta(genome_fasta_path, rotated_fasta_path, step):
    ref_records = list(SeqIO.parse(genome_fasta_path, "fasta"))
    if len(ref_records) != 1:
        print("Error: input fasta has more than one record.")
        return
    id = ref_records[0].id
    sequence = ref_records[0].seq
    if step > 0 and step < len(sequence):
        subseq_1 = sequence[step:]
        subseq_2 = sequence[0:step]
        rot_seq = subseq_1 + subseq_2
    elif step == 0:
        rot_seq = sequence
    elif step < 0:
        subseq_1 = sequence[:(len(sequence)+step)]
        subseq_2 = sequence[(len(sequence)+step):]
        rot_seq = subseq_2 + subseq_1
    else:
        print("Error: step must be greater than 0 and less than the length of the sequence.")
        return None
    with open(rotated_fasta_path, "wt") as fout:
        print(">" + id + " [rotation=" + str(step) + "]", file=fout)
        print(rot_seq, file=fout)


