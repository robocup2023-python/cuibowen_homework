# 将密码子信息存储到字典codon_dict中
codon_dict = {}
with open("codon.txt", "r") as codon_file:
    for line in codon_file:
        codon, amino_acid = line.strip().split()
        codon_dict[codon] = amino_acid
    codon_dict["stop"] = "stop"

# 将DNA序列转录为mRNA序列
def transcript(dna_sequence):
    return dna_sequence.replace("T", "U")

# 将DNA序列翻译为氨基酸序列
def translate(dna_sequence):
    start_codon = "AUG"
    protein_sequence = ""
    for i in range(0, len(dna_sequence), 3):
        codon = dna_sequence[i:i+3]
        if codon == start_codon:
            protein_sequence += codon_dict[codon]
        elif codon_dict[codon] == "stop":
            break
        else:
            protein_sequence += codon_dict[codon]
    return protein_sequence

# 将序列存储到字典seq_dict中
seq_dict = {}
with open("seq.fa", "r") as seq_file:
    current_sequence_name = ""
    current_sequence = ""
    for line in seq_file:
        if line.startswith(">"):
            if current_sequence_name != "":
                seq_dict[current_sequence_name] = current_sequence
            current_sequence_name = line.strip()[1:]
            current_sequence = ""
        else:
            current_sequence += line.strip()
    seq_dict[current_sequence_name] = current_sequence

# 建立字典，键为序列名称，值为对应序列的翻译结果
protein_dict = {}
for sequence_name, sequence in seq_dict.items():
    mrna_sequence = transcript(sequence)
    protein_sequence = translate(mrna_sequence)
    protein_dict[sequence_name] = protein_sequence

# 打印结果
for sequence_name, protein_sequence in protein_dict.items():
    print(f"Sequence Name: {sequence_name}")
    print(f"Protein Sequence: {protein_sequence}")
