from craft_mol.batch_feature import BatchFeature

model_path = './craft_mol/1m_checkpoint_09.pth'
batch_size = 32
config_path = './craft_mol/inference.yaml'
batch_feature = BatchFeature(model_path=model_path, config_path=config_path)
smiles = "CCO"
iupac_name = "ethanol"
mol_feature,mlg_ids, ipc_ids, sfs_ids = batch_feature.get_feature_single(smiles=smiles, iupac_name=iupac_name)
print(mlg_ids[0].x)
