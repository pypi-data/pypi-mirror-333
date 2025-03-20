import pandas as pd
from Bio import SeqIO
import math


def get_variant_types(ref_fasta_file, input_excel, output_excel):
    ref_record = SeqIO.read(ref_fasta_file, "fasta")
    df_final_variants = pd.read_excel(input_excel)
    for i in range(len(df_final_variants)):
        pos = int(df_final_variants.loc[i, "POS"])
        ref = df_final_variants.loc[i, "REF"]
        alt = df_final_variants.loc[i, "ALT"]
        variant_type = df_final_variants.loc[i, "TYPE"]
        df_final_variants.loc[i, "annotation"] = "No"
        if variant_type == "SNV":
            if pos == 1:
                df_final_variants.loc[i, "trinucleotide_context"] = str(ref_record.seq[-1] + ref + ref_record.seq[pos])
            elif pos == len(ref_record.seq):
                df_final_variants.loc[i, "trinucleotide_context"] = str(ref_record.seq[pos-2] + ref + ref_record.seq[0])
            else:
                df_final_variants.loc[i, "trinucleotide_context"] = str(ref_record.seq[pos-2] + ref + ref_record.seq[pos])
            df_final_variants.loc[i, "SNV_group"] = str(ref) + ">" + str(alt)
            df_final_variants.loc[i, "InDel_group"] = "-"
            df_final_variants.loc[i, "summary_anno"] = "-"
            df_final_variants.loc[i, "annotation"] = "Yes"
        if variant_type == "InDel":
            df_final_variants.loc[i, "trinucleotide_context"] = "-"
            df_final_variants.loc[i, "SNV_group"] = "-"
            df_final_variants.loc[i, "InDel_group"] = "-"
            df_final_variants.loc[i, "summary_anno"] = "-" # modify later
            # for homopolymer: unit_size = 1, len(ref) >1, ref_base = ref[-1], ref_size = len(ref) - 1, alt_size = len(alt) -1
            if len(ref) > 1 and len(alt) > 1:
                ref_str = ref[1:]
                alt_str = alt[1:]
                ref_unit_base = ref[1]
                alt_unit_base = alt[1]
                if ref_unit_base == alt_unit_base:
                    unit_base = ref_unit_base
                    # count of unit_base in ref and alt
                    ref_count = ref_str.count(unit_base)
                    alt_count = alt_str.count(unit_base)
                    if ref_count == len(ref_str) and alt_count == len(alt_str):
                        df_final_variants.loc[i, "InDel_group"] = "homopolymer"
                        df_final_variants.loc[i, "summary_anno"] = "poly-" + str(unit_base) + ";ref_size=" + str(len(ref_str)) + ";alt_size=" + str(len(alt_str))
                        df_final_variants.loc[i, "annotation"] = "Yes"
            # for homodimer
            if len(ref) > 2 and len(alt) > 2:
                ref_str = ref[1:]
                alt_str = alt[1:]
                ref_unit_base = ref[1:3]
                alt_unit_base = alt[1:3]
                if ref_unit_base == alt_unit_base and ref_unit_base[0] != ref_unit_base[1]: # avoid the same base
                    unit_base = ref_unit_base
                    # count of unit_base in ref and alt
                    ref_count = len(ref_str)//2
                    alt_count = len(alt_str)//2
                    if ref_str == unit_base * ref_count and alt_str == unit_base * alt_count:
                        df_final_variants.loc[i, "InDel_group"] = "homodimer"
                        df_final_variants.loc[i, "summary_anno"] = "dimer-" + str(unit_base) + ";ref_size=" + str(ref_count) + ";alt_size=" + str(alt_count)
                        df_final_variants.loc[i, "annotation"] = "Yes"
            
            # for other cases
            if df_final_variants.loc[i, "annotation"] == "No":
                # for tandem: unit_size > 1, ref_copy, alt_copy — slippage is here, add later
                # gain/loss of tandem copies for cases when one of them is a single copy unit
                if len(ref) > 1 and len(alt) > 1:
                    ref_str = ref[1:]
                    alt_str = alt[1:]
                    # guess the unit based on gcd
                    current_gcd = math.gcd(len(ref_str), len(alt_str)) # the most frequent count is 1
                    ref_count = len(ref_str) // current_gcd
                    alt_count = len(alt_str) // current_gcd
                    ref_unit = ref_str[:current_gcd]
                    if ref[0] == alt[0] and ref_str == ref_unit * ref_count and alt_str == ref_unit * alt_count:
                        df_final_variants.loc[i, "InDel_group"] = "tandem"
                        df_final_variants.loc[i, "summary_anno"] = "tandem-" + str(ref_unit) + ";ref_size=" + str(ref_count) + ";alt_size=" + str(alt_count)
                        df_final_variants.loc[i, "annotation"] = "Yes"
            if df_final_variants.loc[i, "annotation"] == "No":
                # also tamdem, but the first few bases are different, not 1 as above
                leading_base_count = 2
                while ref[:leading_base_count] == alt[:leading_base_count]:
                    if len(ref) > leading_base_count and len(alt) > leading_base_count:
                        ref_str = ref[leading_base_count:]
                        alt_str = alt[leading_base_count:]
                        current_gcd = math.gcd(len(ref_str), len(alt_str))
                        ref_count = len(ref_str) // current_gcd
                        alt_count = len(alt_str) // current_gcd
                        ref_unit = ref_str[:current_gcd]
                        if ref_str == ref_unit * ref_count and alt_str == ref_unit * alt_count:
                            df_final_variants.loc[i, "InDel_group"] = "tandem"
                            df_final_variants.loc[i, "summary_anno"] = "tandem-" + str(ref_unit) + ";ref_size=" + str(ref_count) + ";alt_size=" + str(alt_count)
                            df_final_variants.loc[i, "annotation"] = "Yes"
                            break
                    leading_base_count += 1
                    if leading_base_count == len(ref) or leading_base_count == len(alt):
                        break
            if df_final_variants.loc[i, "annotation"] == "No":
                leading_base_count = 1
                while ref[:leading_base_count] == alt[:leading_base_count]:
                    leading_base_count += 1
                leading_base_count -= 1
                if leading_base_count == len(ref): # ref is a prefix of alt
                    ref_border_pos = pos + len(ref) - 1
                    ref_border_seq = ref_record.seq[0:ref_border_pos]
                    alt_border_seq = ref_border_seq[0:ref_border_pos] + alt[len(ref):]
                    microhomology_size = 0
                    j = 1
                    while j < 100:
                        if ref_border_seq[-j] == alt_border_seq[-j]:
                            microhomology_size += 1
                            j += 1
                        else:
                            break
                    if microhomology_size == 0 or microhomology_size == 1:
                        df_final_variants.loc[i, "InDel_group"] = "NHEJ"
                    elif microhomology_size > 1:
                        df_final_variants.loc[i, "InDel_group"] = "MMEJ"
                    indel_size = len(alt) - len(ref) # positive for insertion, negative for deletion
                    df_final_variants.loc[i, "summary_anno"] = "MH_size=" + str(microhomology_size) + ";indel_size=" + str(indel_size)
                    df_final_variants.loc[i, "annotation"] = "Yes"
                elif leading_base_count == len(alt): # alt is a prefix of ref
                    ref_border_seq = ref_record.seq[0:(pos-1)] + ref
                    alt_border_seq = ref_border_seq[0:(pos-1)] + alt
                    microhomology_size = 0
                    j = 1
                    while j < 100:
                        if ref_border_seq[-j] == alt_border_seq[-j]:
                            microhomology_size += 1
                            j += 1
                        else:
                            break
                    if microhomology_size == 0 or microhomology_size == 1:
                        df_final_variants.loc[i, "InDel_group"] = "NHEJ"
                    elif microhomology_size > 1:
                        df_final_variants.loc[i, "InDel_group"] = "MMEJ"
                    indel_size = len(alt) - len(ref) # positive for insertion, negative for deletion
                    df_final_variants.loc[i, "summary_anno"] = "MH_size=" + str(microhomology_size) + ";indel_size=" + str(indel_size)
                    df_final_variants.loc[i, "annotation"] = "Yes"
    df_final_variants.to_excel(output_excel, index=False)


def combine_variant_anno(input_excel, output_excel):
    # combine lines with the same POS, REF, and variant_type (SNV, InDel_homopolymer, ...)
    df_final_variants = pd.read_excel(input_excel)
    # current columns: POS, REF, ALT, TYPE, ID_list, counts, annotation, trinucleotide_context, SNV_group, InDel_group, summary_anno
    # unused column: annotation
    df_final_variants = df_final_variants.drop(columns=["annotation"])
    combined_rows = []
    pos_list = list(df_final_variants["POS"])
    pos_list = list(set(pos_list))
    pos_list.sort()
    for pos in pos_list:
        df_tmp = df_final_variants[df_final_variants["POS"] == pos]
        df_tmp = df_tmp.reset_index(drop=True)
        SNV_rows = []
        InDel_homopolymer_rows = []
        InDel_homodimer_rows = []
        InDel_tandem_rows = []
        InDel_others_rows = []
        for i in range(len(df_tmp)):
            ref = df_tmp.loc[i, "REF"]
            alt = df_tmp.loc[i, "ALT"]
            aln_type = df_tmp.loc[i, "TYPE"]
            trinucleotide_context = df_tmp.loc[i, "trinucleotide_context"]
            SNV_group = df_tmp.loc[i, "SNV_group"]
            InDel_group = df_tmp.loc[i, "InDel_group"]
            summary_anno = df_tmp.loc[i, "summary_anno"]
            sample_info = ref + "," + alt + "," + aln_type + "," + trinucleotide_context + "," + SNV_group + "," + InDel_group + "|" + summary_anno
            ID_list = df_tmp.loc[i, "ID_list"]
            counts = df_tmp.loc[i, "counts"]
            # separate SNVs, InDels(homopolymer, homodimer, tandem), MMEJ, NHEJ, No
            if aln_type == "SNV":
                SNV_rows.append([pos, ref, "SNV", alt, sample_info, counts, ID_list])
            elif aln_type == "InDel":
                if InDel_group == "homopolymer":
                    InDel_homopolymer_rows.append([pos, ref, "InDel,homopolymer", alt, sample_info, counts, ID_list])
                elif InDel_group == "homodimer":
                    InDel_homodimer_rows.append([pos, ref, "InDel,homodimer", alt, sample_info, counts, ID_list])
                elif InDel_group == "tandem":
                    InDel_tandem_rows.append([pos, ref, "InDel,tandem", alt, sample_info, counts, ID_list])
                else:
                    InDel_others_rows.append([pos, ref, "InDel," + InDel_group, alt, sample_info, counts, ID_list])
        # combine multi-allelic SNVs: same pos, ref, different alt; lable the counts
        if len(SNV_rows) > 0:
            df_tmp_SNV = pd.DataFrame(SNV_rows)
            df_tmp_SNV.columns = ["pos", "ref", "type", "alt", "sample_info", "counts", "ID_list"]
            alt_list = list(df_tmp_SNV["alt"])
            sample_info_list = list(df_tmp_SNV["sample_info"])
            count_list = list(df_tmp_SNV["counts"])
            for i in range(len(count_list)):
                count_list[i] = str(count_list[i])
            ID_names_list = list(df_tmp_SNV["ID_list"])
            combined_rows.append([pos, ref, "SNV", "#".join(alt_list), "#".join(sample_info_list), "#".join(count_list), "#".join(ID_names_list), "code"])
        # combine multi-allelic InDels: homopolymer, homodimer, tandem: same pos, ref, repeating unit, different alt; lable the counts
        if len(InDel_homopolymer_rows) > 0:
            df_tmp_InDel_homopolymer = pd.DataFrame(InDel_homopolymer_rows)
            df_tmp_InDel_homopolymer.columns = ["pos", "ref", "type", "alt", "sample_info", "counts", "ID_list"]
            alt_list = list(df_tmp_InDel_homopolymer["alt"])
            sample_info_list = list(df_tmp_InDel_homopolymer["sample_info"])
            count_list = list(df_tmp_InDel_homopolymer["counts"])
            for i in range(len(count_list)):
                count_list[i] = str(count_list[i])
            ID_names_list = list(df_tmp_InDel_homopolymer["ID_list"])
            combined_rows.append([pos, ref, "InDel,homopolymer", "#".join(alt_list), "#".join(sample_info_list), "#".join(count_list), "#".join(ID_names_list), "code"])
        if len(InDel_homodimer_rows) > 0:
            df_tmp_InDel_homodimer = pd.DataFrame(InDel_homodimer_rows)
            df_tmp_InDel_homodimer.columns = ["pos", "ref", "type", "alt", "sample_info", "counts", "ID_list"]
            alt_list = list(df_tmp_InDel_homodimer["alt"])
            sample_info_list = list(df_tmp_InDel_homodimer["sample_info"])
            count_list = list(df_tmp_InDel_homodimer["counts"])
            for i in range(len(count_list)):
                count_list[i] = str(count_list[i])
            ID_names_list = list(df_tmp_InDel_homodimer["ID_list"])
            combined_rows.append([pos, ref, "InDel,homodimer", "#".join(alt_list), "#".join(sample_info_list), "#".join(count_list), "#".join(ID_names_list), "code"])
        if len(InDel_tandem_rows) > 0:
            df_tmp_InDel_tandem = pd.DataFrame(InDel_tandem_rows)
            df_tmp_InDel_tandem.columns = ["pos", "ref", "type", "alt", "sample_info", "counts", "ID_list"]
            alt_list = list(df_tmp_InDel_tandem["alt"])
            sample_info_list = list(df_tmp_InDel_tandem["sample_info"])
            count_list = list(df_tmp_InDel_tandem["counts"])
            for i in range(len(count_list)):
                count_list[i] = str(count_list[i])
            ID_names_list = list(df_tmp_InDel_tandem["ID_list"])
            combined_rows.append([pos, ref, "InDel,tandem", "#".join(alt_list), "#".join(sample_info_list), "#".join(count_list), "#".join(ID_names_list), "code"])
            # do not combine complex cases: MMEJ, NHEJ, No
        if len(InDel_others_rows) > 0:
            for i in range(len(InDel_others_rows)):
                pos, ref, aln_type, alt, sample_info, counts, ID_list = InDel_others_rows[i]
                combined_rows.append([pos, ref, aln_type, alt, sample_info, str(counts), ID_list, "code"])
        
    # save two copies: add a column for method: code, manual
    df_variants_combined = pd.DataFrame(combined_rows)
    df_variants_combined.columns = ["pos", "ref", "type", "alt", "sample_info", "counts", "ID_list", "method"]
    df_variants_combined = df_variants_combined.sort_values(by=["pos"])
    df_variants_combined = df_variants_combined.reset_index(drop=True)

    # add multi-allelic if there are multiple alts
    for i in range(len(df_variants_combined)):
        variant_type = df_variants_combined.loc[i, "type"]
        count = df_variants_combined.loc[i, "counts"]
        total_count = 0
        for c in count.split("#"):
            total_count += int(c)
        if "#" in count:
            df_variants_combined.loc[i, "multi-allelic"] = "multi-allelic"
        else:
            df_variants_combined.loc[i, "multi-allelic"] = "di-allelic"
        df_variants_combined.loc[i, "total_count"] = total_count
        if variant_type == "SNV":
            sample_info = df_variants_combined.loc[i, "sample_info"]
            if "#" in sample_info:
                SNV_group_list = []
                trinucleotide_context_group = ""
                for j in range(len(sample_info.split("#"))):
                    info = sample_info.split("#")[j] # # A,T,SNV,simple,AAT,A>T,-|-#A,C,SNV,simple,AAT,A>C,-|-
                    c = count.split("#")[j]
                    _, _, aln_type, trinucleotide_context, SNV_group, _ = info.split(",")
                    SNV_group_list = SNV_group_list + [SNV_group + "=" + str(c)]
                    trinucleotide_context_group = trinucleotide_context
                df_variants_combined.loc[i, "combined_info"] = trinucleotide_context_group + "," + ",".join(SNV_group_list)
            else:
                _, _, aln_type, trinucleotide_context, SNV_group, _ = sample_info.split(",")
                df_variants_combined.loc[i, "combined_info"] = trinucleotide_context + "," + SNV_group + "=" + str(total_count)
        if variant_type == "InDel,homopolymer" or variant_type == "InDel,homodimer" or variant_type == "InDel,tandem":
            sample_info = df_variants_combined.loc[i, "sample_info"] # CTTTTTTTTTT,CTTTTTTTTT,InDel,simple,-,-,homopolymer|poly-T;ref_size=10;alt_size=9
            if "#" in sample_info:
                ref_size_str_group = ""
                alt_count_list = []
                for j in range(len(sample_info.split("#"))):
                    info_1, info_2 = sample_info.split("#")[j].split("|")
                    subtype, ref_size_str, alt_size_str = info_2.split(";")
                    ref_size = ref_size_str.split("=")[1]
                    alt_size = alt_size_str.split("=")[1]
                    change_size = int(alt_size) - int(ref_size)
                    c = count.split("#")[j]
                    ref_size_str_group = ref_size_str
                    alt_count_list = alt_count_list + [str(change_size) + ":" + str(c)]
                df_variants_combined.loc[i, "combined_info"] = subtype + ";" + ref_size_str_group + ";" + ",".join(alt_count_list)
            else:
                info_1, info_2 = sample_info.split("|")
                # poly-T;ref_size=10;alt_size=9
                subtype, ref_size_str, alt_size_str = info_2.split(";")
                ref_size = ref_size_str.split("=")[1]
                alt_size = alt_size_str.split("=")[1]
                change_size = int(alt_size) - int(ref_size)
                df_variants_combined.loc[i, "combined_info"] = subtype + ";" + ref_size_str + ";" + str(change_size) + ":" + str(total_count)
        elif variant_type == "InDel,MMEJ" or variant_type == "InDel,NHEJ":
            # TTGATAATGAT,TTGAT,InDel,simple,-,-,MMEJ|MH_size=4;indel_size=-6
            sample_info = df_variants_combined.loc[i, "sample_info"]
            info_1, info_2 = sample_info.split("|")
            df_variants_combined.loc[i, "combined_info"] = info_2
        else:
            if variant_type != "SNV":
                df_variants_combined.loc[i, "combined_info"] = "-"

    # sort the columns
    df_variants_combined = df_variants_combined[["pos", "ref", "alt", "type", "total_count", "combined_info", "multi-allelic", "method", "sample_info", "counts", "ID_list"]]
    # fix the REF
    for i in range(len(df_variants_combined)):
        ref_old = df_variants_combined.loc[i, "ref"]
        multi_allelic = df_variants_combined.loc[i, "multi-allelic"]
        if multi_allelic == "di-allelic":
            sample_info = df_variants_combined.loc[i, "sample_info"]
            REF_new = sample_info.split(",")[0]
            if REF_new != ref_old:
                df_variants_combined.loc[i, "ref"] = REF_new
                df_variants_combined.loc[i, "fixed_REF"] = "Yes"
            else:
                df_variants_combined.loc[i, "fixed_REF"] = "No"
        else:
            # ACC,ACCC,InDel,-,-,homopolymer|poly-C;ref_size=2;alt_size=3#ACC,AC,InDel,-,-,homopolymer|poly-C;ref_size=2;alt_size=1
            sample_info_list = df_variants_combined.loc[i, "sample_info"].split("#")
            ref_new_list = []
            for sample_info in sample_info_list:
                ref_new_list.append(sample_info.split(",")[0])
            if len(set(ref_new_list)) == 1:
                ref_new = ref_new_list[0]
                if ref_new != ref_old:
                    df_variants_combined.loc[i, "ref"] = ref_new
                    df_variants_combined.loc[i, "fixed_REF"] = "Yes"
                else:
                    df_variants_combined.loc[i, "fixed_REF"] = "No"
            elif len(set(ref_new_list)) > 1:
                df_variants_combined.loc[i, "fixed_REF"] = "multi_ref"
                df_variants_combined.loc[i, "fixed_REF"] = "No"
    df_variants_combined.to_excel(output_excel, index=False)

