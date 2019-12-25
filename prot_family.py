import collections
import re

def get_protein_families(file_name):
    family_dict = dict()
    id_dict = dict()
    family_id = 0
    with open(file_name, "r") as fp:
        cnt = 0
        id_list = list()
        for line in fp:
            if 'family' in line:
                if cnt > 200:
                    id_dict[family_id] = id_list
                    #print(len(id_list))
                family_id = family_id + 1
                cnt = 0
                #id_list[:] = []
                id_list = list()
            else:
                match = re.search(r'.+\((.+)\).+\((.+)\).+\((.+)\).*', line)
                if match:
                    family_dict[match.group(1)] = family_id
                    family_dict[match.group(2)] = family_id
                    family_dict[match.group(3)] = family_id
                    cnt = cnt + 3
                    id_list.append(match.group(1))
                    id_list.append(match.group(2))
                    id_list.append(match.group(3))
                else:
                    match = re.search(r'.+\((.+)\).+\((.+)\).*', line)
                    if match:
                        family_dict[match.group(1)] = family_id
                        family_dict[match.group(2)] = family_id
                        cnt = cnt + 2
                        id_list.append(match.group(1))
                        id_list.append(match.group(2))
                    else:
                        match = re.search(r'.+\((.+)\).*', line)
                        if match:
                            family_dict[match.group(1)] = family_id
                            cnt = cnt + 1
                            id_list.append(match.group(1))

                        
    return id_dict

def get_protein_sequences(file_name):
    seq_dict = dict()
    prot = ""
    with open(file_name, "r") as fp:
        for line in fp:
            if line.startswith(">sp"):
                match = re.search(r'>sp\|(.+)\|.+', line)
                if prot != "":
                    seq_dict[seq_id] = prot
                    prot = ""
                seq_id = match.group(1)
            else:
                prot += line.strip()
    if prot != "":
        seq_dict[seq_id] = prot
    return seq_dict

seq_dict = get_protein_sequences('uniprot_sprot.fasta')
id_dict = get_protein_families('similar.txt')

with open('train.txt', "w") as train_fp:
    with open('test.txt', "w") as test_fp:
        for family_id, id_list in id_dict.items():
            num_seq = len(id_list)
            print(num_seq)
            train_seq_num = num_seq * 0.6
            idx = 0
            for seq_id in id_list:
                if idx < train_seq_num:
                    train_fp.write(seq_dict[seq_id])
                    train_fp.write(" ")
                    train_fp.write(str(family_id))
                    train_fp.write("\n")
                else:
                    test_fp.write(seq_dict[seq_id])
                    test_fp.write(" ")
                    test_fp.write(str(family_id))
                    test_fp.write("\n")
                idx = idx + 1
                

