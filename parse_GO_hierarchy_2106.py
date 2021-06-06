
import time, os, re
from gensim.models.doc2vec import TaggedDocument
from collections import namedtuple

import io
import re

##documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]
relation_list = ["is_a:", "relationship: part_of","relationship: positively_regulates","relationship: negatively_regulates","relationship: regulates","relationship: ends_during","relationship: happens_during","relationship: has_part","relationship: never_in_taxon","relationship: occurs_in","relationship: starts_during"]

GO_documents=[]
GO_dic = {}

GO_ids = []
GO_names = []
GO_namespaces = []
GO_defs = []

GO_defs_rev = []
Exts = []

synonyms = []
relations = []

GOcount=-1

path = "C:\\Users\\kmkim\\Downloads\\research\\craft-3.1.3\\concept-annotation\\GO_BP\\GO_BP+extensions\\GO+GO_BP_extensions.obo"
path_write = "C:\\Users\\kmkim\\Downloads\\research\\craft-3.1.3\\concept-annotation\\GO_BP\\GO_BP+extensions\\GO_BP_extensions_parsed_hierarchy_2106.txt"

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
            relations.append([])

        elif (line.startswith("name:")):
            GO_name = line.replace('name:', "").strip()
            GO_names.append(GO_name)
        elif (line.startswith("synonym:")):
            synonym = re.findall(r'\"(.*?)\"', line)[0]
            synonyms[GOcount].append(synonym)


        for theRelation in relation_list:
            if (line.startswith(theRelation)):
                line = line.replace(theRelation,"")

                rel_line = line.split("!")[0]
                if ":" in rel_line:
                    #print(rel_line)
                    relatedGO = str(rel_line.split(":")[1].strip())
                    relation = [theRelation, relatedGO]
                    relations[GOcount].append(relation)


    for mod_def, mod_id1, mod_Ext in zip(GO_defs, GO_ids, Exts):

        GOs1 = re.findall(r'\'(.*?)\'', mod_def)
        GOs2 = re.findall(r'EXT:(\w+)', mod_def)
        GOs3 = re.findall(r'GO:(\w+)', mod_def)
        GOs = GOs1 + GOs2 + GOs3

        if(mod_Ext):
            for mod_name, mod_id2, mod_def2 in zip(GO_names, GO_ids, GO_defs):
                if mod_name in GOs:
                    mod_def=mod_def.replace(mod_name, mod_def2)

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

for count,(theid, thename) in enumerate(zip (GO_ids, GO_names,)):
    f.write(theid.decode('utf-8') + "\n")
    f.write(thename.decode('utf-8') + "\n")
    thesynonyms = "\t".join(synonyms[count])
    #f.write("synonyms:\t" + thesynonyms.decode('utf-8') + "\n")
    rel_toWrites=[]
    for theRelation in relations[count]:
        rel_toWrites.append(theRelation[1])
    f.write("\t".join(rel_toWrites).decode('utf-8')+"\n")

print("done!")
f.close()