import csv
import argparse

def compare_tables(file1, file2):
    # Save table in the dictionary with SNP_ID keys (third row)
    def load_table(file):
        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            header = []
            info_header = []
            data = {}
            for row in reader:
                if row[0].startswith("#"):
                    if row[0].startswith("#CHROM"):
                        header = row  # CHROM header separately
                    else:
                        info_header.append(row[0])
                else:
                    snp_id = row[2]  
                    data[snp_id] = row
            info_header.append('##FORMAT=<ID=IMP,Number=2,Type=Integer,Description="Imputation Flag">')
            return info_header, header, data

    info_header1, header1, data1 = load_table(file1)
    info_header2, header2, data2 = load_table(file2)

    print('\n'.join(info_header2))
    print('\t'.join(header2))

    # Merge SNP_ID from both table
    all_snp_ids = set(data1.keys()).union(set(data2.keys()))

    # Compare strings by coincidence SNP_ID
    for snp_id in all_snp_ids:
        row1 = data1.get(snp_id, None)
        row2 = data2.get(snp_id, None)

        # Compare strings with same SNP
        snp_info = row1[:8] + ["GT:IMP"]
        genotype1 = [g.replace('/', '|') for g in row1[9:]]
        genotype2 = [g.replace('/', '|') for g in row2[9:]]
        updated_genotypes = []
        imp_flag = False

        for i, (geno1, geno2) in enumerate(zip(genotype1, genotype2)):
            if geno1 != geno2:
                updated_genotypes.append(f"{geno2}:1")
                imp_flag = True
            else:
                updated_genotypes.append(f"{geno2}:0")
        
        if imp_flag:
            snp_info[7] = 'IMP'  # add "IMP" flag if there are differences

        print("\t".join(snp_info) + "\t" + "\t".join(updated_genotypes))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two genotype tables.")
    parser.add_argument('file1', help="Path to the pre-imputed table file")
    parser.add_argument('file2', help="Path to the post-imputed table file")
    
    args = parser.parse_args()

    compare_tables(args.file1, args.file2)
