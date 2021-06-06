
import time, os, re
from gensim.models.doc2vec import TaggedDocument
from collections import namedtuple

import io
import re

##documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]

GO_documents=[]
GO_dic = {}

GO_ids = []
GO_names = []
GO_namespaces = []
GO_defs = []

GO_defs_rev = []
Exts = []
synonyms = []
GOcount=-1

path = "C:\\Users\\kmkim\\Downloads\\research\\craft-3.1.3\\concept-annotation\\GO_BP\\GO_BP+extensions\\GO+GO_BP_extensions.obo"
path_write = "C:\\Users\\kmkim\\Downloads\\research\\craft-3.1.3\\concept-annotation\\GO_BP\\GO_BP+extensions\\GO_BP_extensions_parsed_no_hierarchy.txt"

f = io.open(path_write,'wt',encoding='utf8')

with io.open(path,'r',encoding='utf8') as ifp:

    is_Ext = False



    Extcount=0

    for line in ifp:
        if (line.startswith("id: GO") or line.startswith("id: CHEBI_GO_EXT")):
            ##print(line.replace('id: GO:',"").strip())
            if "EXT" in line:
                is_Ext=True
            else:
                is_Ext =False
            Exts.append(is_Ext)

            GO_id = line.split(':')[2].strip()
            GO_ids.append(GO_id)
            GOcount+=1
            synonyms.append([])
            #f.write(GO_id+"\n")
        elif (line.startswith("name:")):
            ##print(line.replace('id: GO:',"").strip())
            GO_name = line.replace('name:', "").strip()
            GO_names.append(GO_name)
            #f.write(GO_name + "\n")
        elif (line.startswith("namespace:")):
            ##print(line.replace('id: GO:',"").strip())
            GO_namespace = line.replace('namespace:', "").strip()
            GO_namespaces.append(GO_namespace)
            #f.write(GO_namespace + "\n")
        elif(line.startswith("def:")):
            ##print(line.split('\"')[1].strip())
            GO_def = line.split('\"')[1].strip()
            if GO_def.startswith("CHEBI:\'biological role"):
                GO_def = "GO:biological_process"
            elif(is_Ext):
                Extcount+=1
                #print(GO_def)
                GO_def=re.sub(r'\([^()]*\)', '', GO_def)
                GO_def = re.sub(r'\([^()]*\)', '', GO_def)
                GO_def = re.sub(r'\([^()]*\)', '', GO_def)
                #print(GO_def)
                defs = GO_def.split(' or ')
                defTokens = []
                for defToken in defs:
                    if defToken.startswith("GO"):
                        #print(defToken)
                        #defToken = defToken.split(":")[1].replace("\'","")
                        defToken = defToken
                    else:
                        defToken = ""

                    if defToken == "GO:'movement of cell":  # !!!HARD-CODING!!!
                        defToken = "GO:'movement of cell or subcellular component'"
                    elif defToken=="GO:biological_process and causally_effects_or_influences some":
                        defToken = "GO:biological_process and causally_effects_or_influences"
                    elif defToken=="GO:proteolysis  and causally_effected_by some PR_EXT:trypsin":
                        defToken = "GO:proteolysis"
                    elif defToken=="GO:biological_process and realizes some PATO:adhesive)":
                        defToken = ""

                    if(defToken):
                        defTokens.append(defToken)
                GO_def = ' or '.join(defTokens)
                #print(GO_def)
            #GO_def = GO_def.replace('\([^()]*\)', "")
            GO_defs.append((GO_def))


            GO_concat = GO_name + " " + GO_namespace + " " + GO_def
            GO_concat_words = GO_concat.split(" ")
            T = TaggedDocument(GO_concat_words,[GO_id])
            GO_documents.append(T)
            GO_dic [GO_id]= GO_concat


        elif (line.startswith("synonym:")):
            synonym = re.findall(r'\"(.*?)\"', line)[0]
            synonyms[GOcount].append(synonym)
            #print(synonym)


    print(len(GO_names))
    print(len(GO_defs))
    print(Extcount)

    for mod_def, mod_id1, mod_Ext in zip(GO_defs, GO_ids, Exts):

        GOs1 = re.findall(r'\'(.*?)\'', mod_def)
        GOs2 = re.findall(r'EXT:(\w+)', mod_def)
        GOs3 = re.findall(r'GO:(\w+)', mod_def)

        GOs = GOs1 + GOs2 + GOs3
        #print(GOs)
        #print(mod_def)
        if(mod_Ext):
            for mod_name, mod_id2, mod_def2 in zip(GO_names, GO_ids, GO_defs):
                if mod_name in GOs:
                    mod_def=mod_def.replace(mod_name, mod_def2)
                    #print(mod_def)

            #GOs4 = re.findall(r'EXT:(\w+)', "GO_EXT:biological_movement or GO_SO_EXT:sequence_transposition_entity_or_process")
            GOs4 = re.findall(r'EXT:(\w+)',mod_def)
            GOs5 = re.findall(r'EXT:\'(\w+)',mod_def)
            GOs45 = GOs4 + GOs5
            print(mod_def)
            print(GOs45)
            for mod_name3, mod_id3, mod_def3 in zip(GO_names, GO_ids, GO_defs):
                if mod_id3 in GOs45:
                    print(mod_name3)
                    mod_def = mod_def.replace(mod_id3,mod_def3)
                    print(mod_def)









        mod_def = re.sub(' \(GO:[^)]*\)','',mod_def)
        mod_def = re.sub(' \(see GO:[^)]*\)', '', mod_def)
        #mod_def = mod_def.replace("GO:","").replace("\'","")\
        #    .replace("GO_PATO_EXT:","").replace("GO_RO_EXT:", "").replace("GO_SO_EXT:", "")\
        #    .replace("PR_EXT:", "").replace("GO_UBERON_EXT:", "")
        GO_defs_rev.append(mod_def)


print(len(GO_defs))

for count,(theid, thename, thenamespace, thedef) in enumerate(zip (GO_ids, GO_names, GO_namespaces, GO_defs_rev)):
    f.write(theid.decode('utf-8') + "\n")
    f.write(thename.decode('utf-8') + "\n")
    f.write(thenamespace.decode('utf-8') + "\n")
    f.write(thedef.decode('utf-8') + "\n")
    for thesynonym in synonyms[count]:
        f.write(theid.decode('utf-8') + "\n")
        f.write(thesynonym.decode('utf-8') + "\n")
        f.write(thenamespace.decode('utf-8') + "\n")
        f.write(thedef.decode('utf-8') + "\n")

print("done!")
f.close()