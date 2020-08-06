import os
import json

# Adding the CPDT results to the library
# Specify path to the original database file (database parameter)
# Specify path to the CP-DT output of the database file
def add_cpdt(database, cpdt_file):
    """
    output example CP-DT:
    MKRHVEIKWQDETLAVTLYVPELENQAETFPLIVICHGFIGSRIGVNRLFVETATQLIKDGYAVLCFDYVGCGESTGEYGRSGFDQLVAQTRHVLQEAAHFPEIDSQRISLLGHSLGGPVALYTAISEPNIRKLMLWSPVAHPYKDIVRIVGVDTYQRAWQHTSVDYMGYGLTLAFFESLHSYVPLKELQKYTGDVFIAHGTADIDIPVEYCFHYYYAFRSRSTGKSDKEIILEADHTFSDGCSRTMLIDSTREWLSGERYYKQSGGAITRTIGYSI
    PEPTIDE MKRHVEIK: 0.0183349
    PEPTIDE RHVEIK: 0.0847898
    PEPTIDE RHVEIKWQDETLAVTLYVPELENQAETFPLIVICHGFIGSR: 0.00917548
    PEPTIDE HVEIKWQDETLAVTLYVPELENQAETFPLIVICHGFIGSR: 0.0854887
    PEPTIDE HVEIKWQDETLAVTLYVPELENQAETFPLIVICHGFIGSRIGVNR: 0.0086859
    """


    file_database = open(f"{database}", 'r')
    file_CPDT = open(f"{cpdt_file}", 'r')

    seq_ID = {}
    header = ''
    #getting all the headers from the original database (because CP-DT does not include this)
    #this code can easily be manipulated to get the part of the header you want as key
    for line in file_database:
        line = line.rstrip()
        if '>' in line:
            line = line.split(' ')
            #try:
            header = line[0][1:]
            #except IndexError:
                #header = line[0]
        else:
            seq_ID[line] = header
            print(header)
            header = ''

    Peptide_score_dict = {}
    CPDT_output = {}
    seq = ''
    # Goal is here to make a triple dictionary that looks like { sequence_ID : { Peptide : { Predictor : score }}}
    for line in file_CPDT:
        line = line.rstrip()
        if 'PEPTIDE' in line:
            words = line.split()
            #retrieve peptide sequence without ':' (look at output example in docstring)
            peptide = words[1][:-1]
            score = words[2]
            Peptide_score_dict[peptide] = {'CP-DT': float(score)}
        elif line.strip():
            seq = line
            CPDT_output[seq_ID[seq]] = {}
        elif Peptide_score_dict:
            CPDT_output[seq_ID[seq]] = Peptide_score_dict
            Peptide_score_dict = {}
            seq = ''

    file_database.close()
    file_CPDT.close()

    return CPDT_output

# not the cleanest way but at the moment I'm using the functions in the same script so running this script (with the parameters adjusted)
# should make it possible for you to get the scores from each predictor for each peptide in one dictionary
cpdt_dict = add_cpdt('E:\Mats\Databases\9MM\9MM_DB.fasta', 'E:\Mats\CP-DT\9MM\9MM_DB_test1.cpdt')

if cpdt_dict:
    print('CPDT done!')


# Next step is to put all the peptides in DeepMSpeptide (Predictor doesnt take sequences so peptides from CP-DT are used)
# and add the scores to the already existing dictionary created above

def add_DeepMS(DeepMS_output, cpdt_dict):
    """
    Output example DeepMSPeptide:
    Peptide	Prob	Detectability
    AAAAAAAAAAAAAAASSAGGAASTSAATAPATVPAYAGK	0.964686364	1
    AAAAAAAAAAAAAAASSAGGAASTSAATAPATVPAYAGKK	0.91497517	1
    AAAAAAAAAAAAAAASSAGGAASTSAATAPATVPAYAGKKPK	0.8730849	1
    AAAAAAAAAAAANGAGSGAVTPTAAAR	0.84135649	1
    AAAAAAAAAAAANGAGSGAVTPTAAAREGK	0.1436054	0
    AAAAAAAAAAAANGAGSGAVTPTAAAREGKIGR	0.10965574	0
    AAAAAAAAAAAGLATLPGQLIICAA	0.0040765	0
    AAAAAAAAAAEQQK	0.78591686	1
    AAAAAAAAAAEQQKR	0.82756782	1
    AAAAAAAAAAEQQKRLER	0.00558627	0
    AAAAAAAAGSNDMLEPELGR	0.83438534	1
    AAAAAAAAGSNDMLEPELGRSSPVDLSTK	0.0653287	0
    AAAAAAAAK	0.00071234	0
    AAAAAAAAKAK	0.0001681	0
    AAAAAAAAKAKNNK	5.394e-05	0
    """
    # look at output example in docstring to follow these steps
    with open(DeepMS_output, 'r') as DeepMS_results:
        next(DeepMS_results)
        for index, line in enumerate(DeepMS_results):
            line = line.rstrip()
            line = line.split('\t')
            for key in cpdt_dict:
                if line[0] in cpdt_dict[key]:
                    cpdt_dict[key][line[0]]['DeepMSPeptide'] = line[1]

    DeepMS_results.close()

    return cpdt_dict

two_predict_dict = add_DeepMS('E:\Mats\DeepMSPeptide\Datasets\Peptide_list_9MM_8_30_Predictions.txt', cpdt_dict)

if two_predict_dict:
    print('DeepMSpeptide done!')

del cpdt_dict

# Same principle as the last function
def add_AP3(AP3_output, two_predict_dict):
    """
    Output example AP3:
    Peptide sequence	Protein id	Peptide detectability
    WQDETLAVTLYVPELENQAETFPLIVICHGFIGSR	B_lat_ID_00001	0.095
    LFVETATQLIK	B_lat_ID_00001	0.79
    DGYAVLCFDYVGCGESTGEYGR	B_lat_ID_00001	0.725
    SGFDQLVAQTR	B_lat_ID_00001	0.95
    HVLQEAAHFPEIDSQR	B_lat_ID_00001	0.905
    ISLLGHSLGGPVALYTAISEPNIR	B_lat_ID_00001	0.85
    LMLWSPVAHPYK	B_lat_ID_00001	0.745
    IVGVDTYQR	B_lat_ID_00001	0.89
    AWQHTSVDYMGYGLTLAFFESLHSYVPLK	B_lat_ID_00001	0.395
    YTGDVFIAHGTADIDIPVEYCFHYYYAFR	B_lat_ID_00001	0.385
    """
    # need to loop over all the different results because the database is divided in slices of 1000 proteins for this predictor
    directories = os.listdir(AP3_output)
    for directory in directories:
        files = os.listdir(AP3_output + directory)
        # look at output example in docstring to follow these steps
        with open(AP3_output + directory + '/' + files[1], 'r') as AP3_results:
            next(AP3_results)
            for line in AP3_results:
                line = line.rstrip()
                line = line.split('\t')
                if line[1] in two_predict_dict.keys():
                    if line[0] in two_predict_dict[line[1]]:
                        two_predict_dict[line[1]][line[0]]['AP3'] = line[2]
                    else:
                        two_predict_dict[line[1]][line[0]] = {'AP3': line[2]}

            AP3_results.close()

    return two_predict_dict

three_predict_dict = add_AP3('E:/Mats/AP3/Results_9MM/', two_predict_dict)

if three_predict_dict:
    print('AP3 done!')

del two_predict_dict

# the Json file will be created in the directory where this python script is
with open('proteotypicity_scores_9MM_v4.txt', 'w+') as json_file:
    json.dump(three_predict_dict, json_file)