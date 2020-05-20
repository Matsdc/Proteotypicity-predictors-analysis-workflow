#making a set of the peptides so it does not contain duplicates (needed for DeepMSpeptide)
peptides = set()

# adjust path to cpdt output
with open('E:/Mats/CP-DT/SIHUMIx/SIHUMIx_crap.cpdt', 'r') as file:
    for line in file:
        if 'PEPTIDE' in line:
            line = line.split()
            peptide = line[1][:-1]
            peptides.add(peptide)

# making a file containing the sorted and unique peptides
peptides = sorted(peptides)

# file will be made in same directory as script
peptide_list = open('Peptide_list_SIHUMIx.txt', 'w+')

for peptide in peptides:
    print(peptide, file = peptide_list)

peptide_list.close()