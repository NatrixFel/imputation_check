import csv
import argparse

def compare_tables(file1, file2):
    # Функция для загрузки таблицы и извлечения хедера и данных
    def load_table(file):
        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            header = []
            info_header = []
            data = []
            for row in reader:
                if row[0].startswith("#"):
                    if row[0].startswith("#CHROM"):
                        header = row  # Хэдер с образцами отдельно               
                    else:
                        info_header.append(row[0])
                else:
                    data.append(row)
            info_header.append('##FORMAT=<ID=IMP,Number=2,Type=Integer,Description="Imputation Flag">')
            return info_header, header, data

    # Загрузка данных из обоих файлов
    info_header1, header1, data1 = load_table(file1)
    info_header2, header2, data2 = load_table(file2)
    print('\n'.join(info_header2))
    print('\t'.join(header2))
    # Сравниваем строки
    for row1, row2 in zip(data1, data2):
        snp_info = row1[:8]+["GT:IMP"]  # Первые 9 столбцов
        genotype1 = [g.replace('/', '|') for g in row1[9:]]  # Данные генотипов для первой таблицы
        genotype2 = row2[9:]  # Данные генотипов для второй таблицы
        
        #differences = []
        updated_genotypes = []
        imp_flag = False
        #сначала идет образец, потом исходный генотип, а потом предсказанный генотип
        for i, (geno1, geno2) in enumerate(zip(genotype1, genotype2)):
            if geno1 != geno2:
                updated_genotypes.append(f"{geno2}:1")
                imp_flag = True
            else:
                updated_genotypes.append(f"{geno2}:0")
        if imp_flag:
            snp_info[7] = 'IMP'
            
        print("\t".join(snp_info) + "\t" + "\t".join(updated_genotypes))
        
# Путь к файлам
#file1 = "test_LD_no_imputing.vcf"
#file2 = "test_LD_imputing.vcf"
if __name__ == "__main__":
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description="Compare two genotype tables.")
    parser.add_argument('file1', help="Path to the first table file")
    parser.add_argument('file2', help="Path to the second table file")
    
    # Чтение аргументов
    args = parser.parse_args()
    
    # Запуск функции сравнения с указанными файлами
    compare_tables(args.file1, args.file2)

# Запуск функции сравнения
#compare_tables(file1, file2)
