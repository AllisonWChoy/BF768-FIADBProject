import pandas as pd

species = pd.read_csv("/var/www/html/students_22/Group_F/REF_SPECIES.csv")
tree = pd.read_csv("/var/www/html/students_22/Group_F/MA_TREE.csv")
tree_net = pd.read_csv("/var/www/html/students_22/Group_F/MA_files/MA_TREE_GRM_COMPONENT.csv")

location = tree[["STATECD", "INVYR", "UNITCD", "COUNTYCD", "PLOT", "SUBP", "TREE"]]
location.to_csv("/var/www/html/students_22/Group_F/location.csv", index=False)

species = species[["SPCD", "COMMON_NAME", "GENUS", "SPECIES", "VARIETY", "SUBSPECIES", "SPECIES_SYMBOL"]].sort_values(by="SPCD")
species.to_csv("/var/www/html/students_22/Group_F/species.csv", index=False)

tree_table = tree.copy()[["TREE", "CN", "SPCD", "DIA", "HT", "TPA_UNADJ", "TPAMORT_UNADJ", 
"TPAREMV_UNADJ", "TPAGROW_UNADJ", "CCLCD", "UNCRCD","CPOSCD",
"CLIGHTCD","CVIGORCD", "CDENCD", "CDIEBKCD", "CREATED_DATE", "MODIFIED_DATE"]]
tree_table.to_csv("/var/www/html/students_22/Group_F/tree_table.csv", index=False)

biomass = tree.copy()[["DRYBIO_BOLE" , "DRYBIO_TOP","DRYBIO_STUMP", "DRYBIO_SAPLING",
 "DRYBIO_WDLD_SPP", "DRYBIO_BG", "CARBON_AG", "CARBON_BG", "TREE"]]
biomass.to_csv("/var/www/html/students_22/Group_F/biomass.csv", index=False)

growth = tree.copy()[["GROWCFGS", "GROWBFSL", "GROWCFAL", "TREE"]]
tree_net = tree_net[['DIA_BEGIN', 'DIA_MIDPT','DIA_END', 'ANN_DIA_GROWTH', 
'HT_BEGIN', 'HT_MIDPT', 'HT_END','ANN_HT_GROWTH']]
growth = growth.join(tree_net)
temp = growth.pop("TREE")
growth.insert(11, "TREE", temp)

growth.to_csv("/var/www/html/students_22/Group_F/growth.csv", index=False)

mortality = tree.copy()[["MORTCFGS", "MORTBFSL","MORTCFAL","AGENTCD", "TREE"]]
mortality.to_csv("/var/www/html/students_22/Group_F/mortality.csv", index=False)

damage = tree.copy()[["DAMLOC1","DAMTYP1", "DAMSEV1","DAMLOC2" ,"DAMTYP2","DAMSEV2", "DECAYCD", "TREE"]]
damage.to_csv("/var/www/html/students_22/Group_F/damage.csv", index=False)