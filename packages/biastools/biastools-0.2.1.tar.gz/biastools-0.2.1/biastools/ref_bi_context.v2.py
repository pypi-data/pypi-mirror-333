import argparse
import re
import pickle
from os import path
import pysam
import numpy as np
from scipy.stats import chisquare
from typing import List, Tuple, Dict, Union, Set
from collections import defaultdict
import logging

# Constants
PADDING = 5
VAR_CHAIN = 25
EXTEND_LIMIT = 70

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VariantAnalyzer:
    def __init__(self, vcf_file: str, sam_file: str, fasta_file: str, 
                 golden_pickle: str = None, run_id: str = None, 
                 real_data: bool = False, output_file: str = "output.rpt"):
        self.f_vcf = pysam.VariantFile(vcf_file)
        self.f_sam = pysam.AlignmentFile(sam_file)
        self.f_fasta = pysam.FastaFile(fasta_file)
        self.golden_pickle = golden_pickle
        self.run_id = run_id
        self.real_data = real_data
        self.output_file = output_file
        self.dict_ref_haps = defaultdict(dict)
        self.dict_ref_cohorts = defaultdict(dict)
        self.dict_set_conflict_vars = defaultdict(set)
        self.dict_ref_bias = defaultdict(lambda: defaultdict(lambda: {'n_read':[0,0,0], 'n_var':[0,0,0,0], 'map_q':[0,0,0], 'distribute':[[],[],[],[]]}))
        
        if not self.real_data and self.golden_pickle:
            with open(self.golden_pickle, "rb") as f:
                self.dict_ref_var_name = pickle.load(f)

    def analyze(self):
        self.build_variant_maps()
        # TODO: just print out the variant map for checking, remove later
        f_tmp = open("/home/mlin77/vast/personalized_leviosam/bwa_Ltag_experiment/bt_chr21/refact.variant_map.txt", "w")
        for ref_name in self.dict_ref_haps:
            for pos in self.dict_ref_haps[ref_name]:
                f_tmp.write(f"{pos}\t{self.dict_ref_haps[ref_name][pos]}\n")
        f_tmp.close()
        f_tmp = open("/home/mlin77/vast/personalized_leviosam/bwa_Ltag_experiment/bt_chr21/refact.variant_cohort.txt", "w")
        for ref_name in self.dict_ref_cohorts:
            for pos in self.dict_ref_cohorts[ref_name]:
                f_tmp.write(f"{pos}\t{self.dict_ref_cohorts[ref_name][pos]}\n")
        f_tmp.close()
        print("Testing over")
        exit()
        # TODO end of testing
        self.compare_reads_to_variants()
        self.generate_report()

    def build_variant_maps(self):
        logger.info("Start building the variant maps...")
        self.variant_seq()
        
        # Extend conflict set
        for ref_name, positions in self.dict_set_conflict_vars.items():
            for pos in list(positions):
                self.dict_set_conflict_vars[ref_name].update(range(pos - VAR_CHAIN, pos + VAR_CHAIN + 1))

    def compare_reads_to_variants(self):
        logger.info("Start comparing reads to the variant map...")
        self.compare_sam_to_haps()

    def generate_report(self):
        logger.info("Start output report...")
        self.output_report()

    def variant_seq(self):
        for ref_name in self.f_fasta.references:
            for var in self.f_vcf.fetch(ref_name):
                self.process_variant(ref_name, var)

    def process_variant(self, ref_name: str, var: pysam.VariantRecord):
        var_start = var.start - PADDING
        var_stop = var.stop + PADDING
        ref_seq = self.f_fasta.fetch(reference=ref_name, start=var_start, end=var_stop)
        hap_0, hap_1 = var.samples[0]['GT']
        
        seq_hap0, diff_hap0, _ = self.switch_var_seq(var, ref_seq, var_start, hap_0)
        seq_hap1, diff_hap1, _ = self.switch_var_seq(var, ref_seq, var_start, hap_1)
        
        if hap_0 != hap_1 and ((seq_hap0 in seq_hap1) or (seq_hap1 in seq_hap0)):
            # Handle repetitive sequences
            flag_side = self.left_right_check(seq_hap0, seq_hap1)
            if flag_side in [0, 2]:  # right side or both sides
                ref_extend = self.f_fasta.fetch(reference=ref_name, start=var_stop, end=var_stop+EXTEND_LIMIT+PADDING)
                seq_hap0, seq_hap1, len_extend = self.extend_ref_seq_padding(seq_hap0, seq_hap1, ref_extend, ref_extend, True, PADDING)
                var_stop += len_extend
            if flag_side in [1, 2]:  # left side or both sides
                ref_extend = self.f_fasta.fetch(reference=ref_name, start=var_start-EXTEND_LIMIT-PADDING, end=var_start)
                seq_hap0, seq_hap1, len_extend = self.extend_ref_seq_padding(seq_hap0, seq_hap1, ref_extend, ref_extend, False, PADDING)
                var_start -= len_extend
        
        self.dict_ref_haps[ref_name][var.start] = (var_start+PADDING, var_stop-PADDING, seq_hap0, seq_hap1)
        #TODO implement the cohort variants
        cohort_variants = list(self.f_vcf.fetch(ref_name, var.start-VAR_CHAIN, var.stop+VAR_CHAIN))
        if len(cohort_variants) == 1:
            #TODO implement the dict_ref_cohorts
            pass
        else:
            cohort_start = cohort_variants[0].start - VAR_CHAIN
            cohort_stop = var.stop + VAR_CHAIN
            for v in cohort_variants:
                len_extend = self.check_right_repeat(v)
    
    def check_right_repeat(self, c_var: pysam.VariantRecord):
        c_var_start = c_var.start - PADDING
        c_var_stop = c_var.stop + PADDING
        c_var_seq = self.f_fasta.fetch(reference=c_var.contig, start=c_var_start, end=c_var_stop)
        
        flag_side = self.left_right_check(c_var_seq_hap0, c_var_seq_hap1)
        if flag_side in [0, 2]:  # right side or both sides
            ref_extend = self.f_fasta.fetch(reference=c_var.contig, start=c_var_stop, end=c_var_stop+EXTEND_LIMIT+PADDING)
            c_var_seq_hap0, c_var_seq_hap1, len_extend = self.extend_ref_seq_padding(c_var_seq_hap0, c_var_seq_hap1, ref_extend, ref_extend, True, PADDING)
            c_var_stop += len_extend
        
        c_var_hap0, c_var_hap1 = c_var.samples[0]['GT']
        if c_var_hap0 == c_var_hap1:
            return False
        else:
            c_var_start  = c_var.start - PADDING
            c_var_stop   = c_var.stop + PADDING
            c_var_len   = c_var.stop - c_var.start + 2*PADDING
            c_var_limmit = c_var.stop + EXTEND_LIMIT
            full_seq = self.f_fasta.fetch(reference=c_var.contig, start=c_var_start, end=c_var_limmit)
            c_var_seq_hap0, *_ = self.switch_var_seq(c_var, full_seq[:c_var_len], c_var_start, c_var_hap0)
            c_var_seq_hap1, *_ = self.switch_var_seq(c_var, full_seq[:c_var_len], c_var_start, c_var_hap1)
            if len(c_var_seq_hap0) == len(c_var_seq_hap1):
                return False
            elif c_var_seq_hap0 in c_var_seq_hap1 or c_var_seq_hap1 in c_var_seq_hap0:
                c_var_extend_hap0, c_var_extend_hap1, len_extend = self.extend_ref_seq(c_var_seq_hap0, c_var_seq_hap1, full_seq, full_seq, True)
                return len_extend
        return False




    def compare_sam_to_haps(self):
        for segment in self.f_sam:
            if segment.is_unmapped:
                continue
            self.process_read(segment)

    def process_read(self, segment: pysam.AlignedSegment):
        ref_name = segment.reference_name
        pos_start = segment.reference_start
        pos_end = segment.reference_end
        cigar_tuples = segment.cigartuples
        mapq = segment.mapping_quality
        read_seq = segment.query_alignment_sequence

        related_vars = list(self.f_vcf.fetch(ref_name, pos_start, pos_end))
        
        for var in related_vars:
            if var.start in self.dict_set_conflict_vars[ref_name]:
                continue

            match_flag_0 = self.match_to_hap(segment.query_name, pos_start, pos_end, var.start, 
                                             read_seq, self.dict_ref_haps[ref_name][var.start][2], 
                                             cigar_tuples, PADDING, PADDING+1, PADDING+1, True)
            match_flag_1 = self.match_to_hap(segment.query_name, pos_start, pos_end, var.start, 
                                             read_seq, self.dict_ref_haps[ref_name][var.start][3], 
                                             cigar_tuples, PADDING, PADDING+1, PADDING+1, True)

            if match_flag_0 == 1 and match_flag_1 == 1:
                self.dict_ref_bias[ref_name][var.start]['n_var'][2] += 1
            elif match_flag_0 == 1:
                self.dict_ref_bias[ref_name][var.start]['n_var'][0] += 1
                self.dict_ref_bias[ref_name][var.start]['distribute'][0].append(pos_start)
                self.dict_ref_bias[ref_name][var.start]['distribute'][2].append(pos_end)
            elif match_flag_1 == 1:
                self.dict_ref_bias[ref_name][var.start]['n_var'][1] += 1
                self.dict_ref_bias[ref_name][var.start]['distribute'][1].append(pos_start)
                self.dict_ref_bias[ref_name][var.start]['distribute'][3].append(pos_end)
            else:
                self.dict_ref_bias[ref_name][var.start]['n_var'][3] += 1

            if self.real_data:
                self.dict_ref_bias[ref_name][var.start]['n_read'][0] += 1
                self.dict_ref_bias[ref_name][var.start]['map_q'][0] += mapq
            else:
                # Handle simulated data
                pass  # Implement the logic for simulated data here

    def output_report(self):
        with open(self.output_file, 'w') as f_all, \
             open(self.output_file + '.gap', 'w') as f_gap, \
             open(self.output_file + '.SNP', 'w') as f_SNP:
            
            headers = self.get_report_headers()
            f_all.write(headers['all'])
            f_gap.write(headers['gap'])
            f_SNP.write(headers['SNP'])

            for var in self.f_vcf:
                self.write_variant_data(var, f_all, f_gap, f_SNP)

    def get_report_headers(self) -> Dict[str, str]:
        if self.real_data:
            header = "CHR\tHET_SITE\tNUM_READS\tAVG_MAPQ\tEVEN_P_VALUE\tBALANCE\tREF\tALT\tBOTH\tOTHER\tGAP\n"
            return {'all': header, 'gap': header, 'SNP': header}
        else:
            header = "CHR\tHET_SITE\tNUM_READS\tAVG_MAPQ\tEVEN_P_VALUE\tBALANCE\tREF\tALT\tBOTH\tOTHER\tMAP_BALANCE\tMAP_REF\tMAP_ALT\tMIS_MAP\tSIM_BALANCE\tSIM_REF\tSIM_ALT\tGAP\n"
            return {'all': header, 'gap': header, 'SNP': header}

    def write_variant_data(self, var: pysam.VariantRecord, f_all, f_gap, f_SNP):
        ref_name = var.contig
        hap = var.samples[0]['GT']
        if (hap[0] != 0 and hap[1] != 0) or (hap[0] == 0 and hap[1] == 0):
            return
        if hap[0] == 0:
            idx_ref, idx_alt = 0, 1
        else:
            idx_ref, idx_alt = 1, 0
        
        if var.start in self.dict_set_conflict_vars[ref_name]:
            return

        bias_data = self.dict_ref_bias[ref_name][var.start]
        n_read = bias_data['n_read']
        n_var = bias_data['n_var']
        map_q = bias_data['map_q']
        p_value = self.chi_square_test(var.start, bias_data['distribute'][idx_alt])
        p_value = min(p_value, self.chi_square_test(var.start, bias_data['distribute'][idx_ref]))

        output_string = f"{ref_name}\t{var.start+1}\t{sum(n_read)}\t{self.get_division(sum(map_q[:2]), sum(n_read[:2]))}\t{p_value:.4f}\t"
        output_string += f"{self.get_division(n_var[idx_ref]+n_var[2]*0.5, sum(n_var[:3]))}\t{n_var[idx_ref]}\t{n_var[idx_alt]}\t{n_var[2]}\t{n_var[3]}"

        if not self.real_data:
            output_string += f"\t{self.get_division(n_read[idx_ref], sum(n_read[:2]))}\t{n_read[idx_ref]}\t{n_read[idx_alt]}\t{n_read[2]}"
            read_info = self.dict_ref_var_name[ref_name][var.start]
            output_string += f"\t{self.get_division(read_info[idx_ref+2], sum(read_info[2:4]))}\t{read_info[idx_ref+2]}\t{read_info[idx_alt+2]}"

        if len(var.ref) == len(var.alts[hap[idx_alt] - 1]):
            f_all.write(output_string + "\t\n")
            f_SNP.write(output_string + "\n")
        else:
            f_all.write(output_string + "\t.\n")
            f_gap.write(output_string + "\n")

    def chi_square_test(self, var_start: int, list_pos_start: List[int]) -> float:
        if len(list_pos_start) < 2:
            return 0
        bucket_num = 5
        bucket_len = int(100 / bucket_num)
        list_count = np.zeros(bucket_num)
        input_idx = np.minimum((var_start - np.array(list_pos_start)) // bucket_len, bucket_num - 1)
        np.add.at(list_count, input_idx, 1)
        _, p_value = chisquare(list_count)
        return 0 if np.isnan(p_value) else p_value

    def get_division(self, num_1: float, num_2: float) -> str:
        if num_2 == 0:
            return 'nan'
        else:
            return format(num_1 / num_2, '.4f')

    def switch_var_seq(self, var: pysam.VariantRecord, ref: str, start: int, genotype: int) -> Tuple[str, int, int]:
        if genotype == 0:
            return ref, 0, len(var.ref)
        else:
            alt = var.alts[genotype - 1]
            return ref[:var.start-start] + alt + ref[var.stop-start:], len(var.ref) - len(alt), len(alt)

    def left_right_check(self, seq_hap0: str, seq_hap1: str) -> int:
        assert seq_hap0 != seq_hap1
        assert (seq_hap0 in seq_hap1) or (seq_hap1 in seq_hap0)
        len_0, len_1 = len(seq_hap0), len(seq_hap1)
        if len_0 > len_1:
            if seq_hap0[:len_1] == seq_hap1:
                return 0  # right side repetitive
            elif seq_hap0[-len_1:] == seq_hap1:
                return 1  # left side repetitive
        else:
            if seq_hap1[:len_0] == seq_hap0:
                return 0  # right side repetitive
            elif seq_hap1[-len_0:] == seq_hap0:
                return 1  # left side repetitive
        return 2  # in the middle

    def extend_ref_seq_padding(self, seq_hap0: str, seq_hap1: str, ref_extend_0: str, ref_extend_1: str, 
                               flag_right: bool = True, padding: int = PADDING) -> Tuple[str, str, int]:
        if flag_right:
            seq_hap0_extend, seq_hap1_extend, len_extend = self.extend_ref_seq(seq_hap0, seq_hap1, ref_extend_0[:-padding], ref_extend_1[:-padding], flag_right)
            if len_extend:
                return seq_hap0_extend + ref_extend_0[len_extend:len_extend+padding], seq_hap1_extend + ref_extend_1[len_extend:len_extend+padding], len_extend+padding
            else:
                return seq_hap0, seq_hap1, False
        else:
            seq_hap0_extend, seq_hap1_extend, len_extend = self.extend_ref_seq(seq_hap0, seq_hap1, ref_extend_0[padding:], ref_extend_1[padding:], flag_right)
            if len_extend:
                return ref_extend_0[-len_extend-padding:-len_extend] + seq_hap0_extend, ref_extend_1[-len_extend-padding:-len_extend] + seq_hap1_extend, len_extend+padding
            else:
                return seq_hap0, seq_hap1, False

    def extend_ref_seq(self, seq_hap0: str, seq_hap1: str, ref_extend_0: str, ref_extend_1: str, flag_right: bool = True) -> Tuple[str, str, int]:
        seq_hap0_extend, seq_hap1_extend = seq_hap0, seq_hap1
        assert (seq_hap0_extend in seq_hap1_extend) or (seq_hap1_extend in seq_hap0_extend)
        len_iterate = min(len(ref_extend_0), len(ref_extend_1))
        if flag_right:
            for idx in range(len_iterate):
                seq_hap0_extend += ref_extend_0[idx]
                seq_hap1_extend += ref_extend_1[idx]
                if not ((seq_hap0_extend in seq_hap1_extend) or (seq_hap1_extend in seq_hap0_extend)):
                    return seq_hap0_extend, seq_hap1_extend, idx+1
        else:
            for idx in range(len_iterate):
                seq_hap0_extend = ref_extend_0[-idx-1] + seq_hap0_extend
                seq_hap1_extend = ref_extend_1[-idx-1] + seq_hap1_extend
                if not ((seq_hap0_extend in seq_hap1_extend) or (seq_hap1_extend in seq_hap0_extend)):
                    return seq_hap0_extend, seq_hap1_extend, idx+1
        return seq_hap0_extend, seq_hap1_extend, False

    def match_to_hap(self, seq_name: str, read_start: int, read_end: int, var_start: int,
                     seq_read: str, seq_hap: str, cigar_tuples: List[Tuple[int, int]],
                     padding: int, l_min_req: int, r_min_req: int, start_flag: bool = True) -> int:
        if read_start > var_start or read_end < var_start:
            return -1
        r_start = self.locate_by_cigar(read_start, var_start, cigar_tuples)
        
        if start_flag:
            l_bound = r_start - padding
            r_bound = l_bound + len(seq_hap)
        else:
            r_bound = r_start + padding
            l_bound = r_bound - len(seq_hap)

        min_match = 0
        if l_bound < 0:
            seq_hap = seq_hap[-l_bound:]
            l_bound = 0
            min_match = r_min_req
        if r_bound > len(seq_read):
            seq_hap = seq_hap[:len(seq_read)-r_bound]
            r_bound = len(seq_read)
            if min_match != 0:
                logger.warning(f"The read is totally contained in the variant!! {seq_name} at {var_start}")
            min_match = l_min_req
        if r_bound - l_bound < min_match:
            return -1
        if seq_read[l_bound:r_bound].upper() == seq_hap.upper():
            return 1
        else:
            return 0

    def locate_by_cigar(self, read_start: int, target_pos: int, cigar_tuples: List[Tuple[int, int]]) -> int:
        ref_cursor = read_start
        read_cursor = 0
        for code, runs in cigar_tuples:
            if code in (0, 7, 8):  # M or = or X
                ref_cursor += runs
                if ref_cursor > target_pos:
                    return read_cursor + (runs - ref_cursor + target_pos)
                read_cursor += runs
            elif code == 1:  # I
                if ref_cursor > target_pos:
                    return read_cursor
                read_cursor += runs
            elif code == 2:  # D
                ref_cursor += runs
                if ref_cursor > target_pos:
                    return read_cursor
            elif code in (4, 5):  # S or H, pysam already parsed
                pass
            else:
                logger.error(f"Unexpected CIGAR code {code}")
        return read_cursor

def parse_arguments():
    parser = argparse.ArgumentParser(description="Analyze reference bias in genomic sequencing data.")
    parser.add_argument('-v', '--vcf', help='VCF file', required=True)
    parser.add_argument('-s', '--sam', help='SAM file', required=True)
    parser.add_argument('-f', '--fasta', help='Reference FASTA file', required=True)
    parser.add_argument('-r', '--real_data', help='Turn off hap_information warning for real data', action='store_true')
    parser.add_argument('-p', '--golden_pickle', help='Pickle file containing the golden information for report reference')
    parser.add_argument('-t', '--run_id', help='Tag for run_id, can be used to indicate chromosome number')
    parser.add_argument('-o', '--out', help='Output file', required=True)
    return parser.parse_args()

if __name__ == "__main__":
    try:
        args = parse_arguments()
        analyzer = VariantAnalyzer(args.vcf, args.sam, args.fasta, 
                                   args.golden_pickle, args.run_id, 
                                   args.real_data, args.out)
        analyzer.analyze()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise