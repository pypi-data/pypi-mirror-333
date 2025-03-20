import torch
from torch.utils.data import Dataset
import dgl
import numpy as np

class GraphDataset(Dataset):
    def __init__(self, graphs=None, target=None, smiles=None):
        if graphs is None: return
        self.graphs = graphs
        self.node_feature = [g.ndata['f'] for g in graphs]
        self.edge_feature = [g.edata['f'] for g in graphs]
        self.target = torch.tensor(target).float()
        self.smiles = smiles

    def __len__(self):
        return len(self.graphs)

    def __getitem__(self, idx):
        return self.graphs[idx], self.node_feature[idx], self.edge_feature[idx], self.target[idx], self.smiles[idx]
    
    # reload the dataset with new data
    def reload(self, data):
        self.graphs, self.node_feature, self.edge_feature, self.target, self.smiles = data

        self.target= torch.stack(self.target,dim=0)
        if self.target.dim() == 1:
            self.target = self.target.unsqueeze(-1)

    # get a subset of the dataset with given indices
    def get_subDataset(self, idx):
        graphs = [self.graphs[i] for i in idx]
        node_feature = [self.node_feature[i] for i in idx]
        edge_feature = [self.edge_feature[i] for i in idx]
        target = [self.target[i] for i in idx]
        smiles = [self.smiles[i] for i in idx]
        
        dataset = GraphDataset()
        dataset.reload((graphs, node_feature, edge_feature, target, smiles))
        return dataset
        

    @staticmethod
    def collate(samples):
        graphs, node_feature, edge_feature, target, smiles = map(list, zip(*samples))
        batched_graph = dgl.batch(graphs)
        return batched_graph, torch.concat(node_feature,dim=0), torch.concat(edge_feature,dim=0), torch.stack(target,dim=0), smiles
    
    @staticmethod
    def unwrapper(batch_graph, node_feature, edge_feature, target, smiles,device='cpu'):
        batch_graph = batch_graph.to(device=device)
        node_feature = node_feature.float().to(device=device)
        edge_feature = edge_feature.float().to(device=device)
        target = target.float().to(device=device)
        return {"graph":batch_graph, "node_feats":node_feature, "edge_feats":edge_feature, "target":target, "smiles":smiles}

class GraphDataset_withSolv(GraphDataset):
    def __init__(self, graphs=None, solv_graphs=None, target=None, smiles=None, solv_smiles=None):
        super().__init__(graphs, target, smiles)
        if graphs is None: return
        self.solv_graphs = solv_graphs
        self.solv_node_feature = [g.ndata['f'] for g in solv_graphs]
        self.solv_edge_feature = [g.edata['f'] for g in solv_graphs]
        self.solv_smiles = solv_smiles

    def __getitem__(self, idx):
        args = super().__getitem__(idx)
        return args + (self.solv_graphs[idx], self.solv_node_feature[idx], self.solv_edge_feature[idx], self.solv_smiles[idx])
    
    def reload(self, data):
        self.graphs, self.node_feature, self.edge_feature, self.target, self.smiles, self.solv_graphs, self.solv_node_feature, self.solv_edge_feature, self.solv_smiles = data
        
        self.target= torch.stack(self.target,dim=0)
        if self.target.dim() == 1:
            self.target = self.target.unsqueeze(-1)


    # def subDataset(self, idx):
    #     super().subDataset(idx)
    #     self.solv_graphs = [self.solv_graphs[i] for i in idx]
    #     self.solv_node_feature = [self.solv_node_feature[i] for i in idx]
    #     self.solv_edge_feature = [self.solv_edge_feature[i] for i in idx]
    #     self.solv_smiles = [self.solv_smiles[i] for i in idx]

    def get_subDataset(self, idx):
        graphs = [self.graphs[i] for i in idx]
        node_feature = [self.node_feature[i] for i in idx]
        edge_feature = [self.edge_feature[i] for i in idx]
        target = [self.target[i] for i in idx]
        smiles = [self.smiles[i] for i in idx]        
        
        solv_graphs = [self.solv_graphs[i] for i in idx]
        solv_node_feature = [self.solv_node_feature[i] for i in idx]
        solv_edge_feature = [self.solv_edge_feature[i] for i in idx]
        solv_smiles = [self.solv_smiles[i] for i in idx]

        dataset = GraphDataset_withSolv()
        dataset.reload((graphs, node_feature, edge_feature, target, smiles, solv_graphs, solv_node_feature, solv_edge_feature, solv_smiles))
        return dataset


    @staticmethod
    def collate(samples):
        graphs, node_feature, edge_feature, target, smiles, solv_graphs, solv_node_feature, solv_edge_feature, solv_smiles = map(list, zip(*samples))

        batched_graph = dgl.batch(graphs)
        batched_solv_graph = dgl.batch(solv_graphs)
        return batched_graph, torch.concat(node_feature,dim=0), torch.concat(edge_feature,dim=0), batched_solv_graph, torch.concat(solv_node_feature,dim=0), torch.concat(solv_edge_feature,dim=0), torch.stack(target,dim=0), smiles, solv_smiles
    
    @staticmethod
    def unwrapper(batch_graph, node_feature, edge_feature, batch_solv_graph, solv_node_feature, solv_edge_feature, target, smiles, solv_smiles, device='cpu'):
        batch_graph = batch_graph.to(device=device)
        node_feature = node_feature.float().to(device=device)
        edge_feature = edge_feature.float().to(device=device)
        batch_solv_graph = batch_solv_graph.to(device=device)
        solv_node_feature = solv_node_feature.float().to(device=device)
        solv_edge_feature = solv_edge_feature.float().to(device=device)
        target = target.float().to(device=device)

        return {"graph":batch_graph, "node_feats":node_feature, "edge_feats":edge_feature, "solv_graph":batch_solv_graph, "solv_node_feats":solv_node_feature, "solv_edge_feats":solv_edge_feature, "target":target, "smiles":smiles, "solv_smiles":solv_smiles}
    