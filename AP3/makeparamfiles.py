import os

# You can specify your database here (mine is divided into 1000 proteins each)
# The reason for dividing this is because large database files won't be analyzed by AP3
files = os.listdir('E:/Mats/Databases/SIHUMIx/Databases_1000')


# Specifying where the parameter files for AP3 need to be saved
# This folder always needs to be named 'params' or else AP3 wont be able to find it
save_path = 'E:/Mats/AP3/Params'

# For every slice of the database a parameter file will be made and it will also directly be analyzed by AP3
for file in files:
    #os.mkdir(f"E:\Mats\AP3\Results_SIHUMIx\{file}")
    completename = os.path.join(save_path, file + '.param')
    f = open(completename, 'w+')
    f.write(f"""InputFilePath="E:/Mats/Databases/SIHUMIx/Databases_1000/{file}"
Model="E.coli"
IdentifierParsingRule=">(.*?)\s"
ResultPath="E:\Mats\AP3\Results_SIHUMIx\{file}"
AllowMinPeptideLength="8"
AllowMaxPeptideLength="30"
AllowMissingCutNumber="2"
""")
    f.close()
    os.system(f'cd E:')
    os.system(f'E:/Mats/AP3/AP3.exe E:/Mats/AP3/Params/{file}.param')


        
      
