import sys
import os
import subprocess

def main():
    path_ref=sys.argv[1]
    path_vcf=sys.argv[2]
    path_out=sys.argv[3]
    sample_id=sys.argv[4]
    THR=sys.argv[5]
    ALN=sys.argv[6]
    ALN_IDX=sys.argv[7]
    run_id=sys.argv[8]
    prefix=path_out+'/'+sample_id

    print("[Biastools] Align sequences to the original reference...")

    if ALN == "bowtie2":
        print("[Biastools] Align with bowtie2")
        if os.path.exists(ALN_IDX+'.1.bt2'):
            pass
        else:
            subprocess.call(' '.join(["bowtie2-build", path_ref, ALN_IDX]), shell=True)
        subprocess.call(' '.join(["bowtie2", "-p", THR, "-x", ALN_IDX, "--rg-id", run_id+"_hapA", "--rg", "SM:"+sample_id, "-1", prefix+".hapA_1.fq.gz", \
                         "-2", prefix+".hapA_2.fq.gz", "|", "samtools sort -@", THR, "-o", prefix+".hapA."+run_id+".sorted.bam"]), shell=True)
        subprocess.call(' '.join(["bowtie2", "-p", THR, "-x", ALN_IDX, "--rg-id", run_id+"_hapB", "--rg", "SM:"+sample_id, "-1", prefix+".hapB_1.fq.gz", \
                         "-2", prefix+".hapB_2.fq.gz", "|", "samtools sort -@", THR, "-o", prefix+".hapB."+run_id+".sorted.bam"]), shell=True)
    elif ALN == "bwamem":
        print("[Biastools] Align with BWA MEM")
        if os.path.exists(ALN_IDX+'.bwt'):
            pass
        else:
            subprocess.call(' '.join(["bwa index", path_ref, "-p", ALN_IDX]), shell=True)
        subprocess.call(' '.join(["bwa mem -t", THR, ALN_IDX, prefix+".hapA_1.fq.gz", prefix+".hapA_2.fq.gz", "-R", "@RG\tID:"+run_id+"_hapA\tSM:"+sample_id, + "|", \
                         "samtools sort -@ ", THR, "-o", prefix+".hapA."+run_id+".sorted.bam"]), shell=True)
        subprocess.call(' '.join(["bwa mem -t", THR, ALN_IDX, prefix+".hapB_1.fq.gz", prefix+".hapB_2.fq.gz", "-R", "@RG\tID:"+run_id+"_hapB\tSM:"+sample_id, + "|", \
                         "samtools sort -@ ", THR, "-o", prefix+".hapB."+run_id+".sorted.bam"]), shell=True)
    subprocess.call(' '.join(["samtools merge -f", prefix+'.'+run_id+".sorted.bam", prefix+'.hapA.'+run_id+".sorted.bam", \
                    prefix+'.hapB.'+run_id+".sorted.bam"]), shell=True)

    print("[Biastools] Intersect the bam file and vcf file")
    if os.path.exists(prefix+".het.vcf.gz") != True:
        subprocess.call(["python3", "biastools/filter_het_VCF.py", "-v", prefix+".normalized.vcf.gz", "-o", prefix+".het.vcf.gz"])
        subprocess.call(' '.join(["tabix", "-p", "vcf", prefix+".het.vcf.gz"]), shell=True)

    subprocess.call(' '.join(["bedtools intersect -a ", prefix+'.'+run_id+".sorted.bam", "-b", prefix+".het.vcf.gz", "| samtools view -bo", \
                     prefix+'.'+run_id+'.sorted.het.bam']), shell=True)
    subprocess.call(' '.join(["samtools index ", prefix+'.'+run_id+'.sorted.het.bam']), shell=True)

if __name__ == "__main__":
    #list_arguments = list(str(sys.argv))
    #print(list_arguments)
    main()
