import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
import numpy as np
from scipy.linalg import svd
import pandas as pd 
from sklearn.decomposition import PCA

def latent_semantic_indexing(X, k = None):
    """\
        Compute LSI with TF-IDF transform, i.e. SVD on document matrix

        Parameters:
            X: cell by feature(region) count matrix
        Returns:
            latent: cell latent matrix
    """
    X = X.T
    count = np.count_nonzero(X, axis=1)
    count = np.log(X.shape[1] / count)
    X = X * count[:,None]

    
    U, S, Vh = svd(X, full_matrices = False, compute_uv = True)
    if k != None:
        latent = np.matmul(Vh[:k, :].T, np.diag(S[:k]))
    else:
        latent = np.matmul(Vh.T, np.diag(S))
    return latent

class scDataset(Dataset):

    def __init__(self, atac_seq_file = "./data/expr_atac_processed.csv", rna_seq_file = "./data/expr_rna_processed.csv", dim_reduction = False):
        self.expr_ATAC = pd.read_csv(atac_seq_file, index_col=0).to_numpy()
        self.expr_RNA = pd.read_csv(rna_seq_file, index_col=0).to_numpy()
        
        if dim_reduction:
            self.expr_RNA = StandardScaler().fit_transform(self.expr_RNA)
            self.expr_RNA = PCA(n_components=100).fit_transform(self.expr_RNA)
            self.expr_ATAC = latent_semantic_indexing(self.expr_ATAC, k=100)

        # self.transform = transform
        self.expr_ATAC = torch.FloatTensor(self.expr_ATAC)
        self.expr_RNA = torch.FloatTensor(self.expr_RNA)

        
    def __len__(self):
        # number of cells
        return len(self.expr_ATAC)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        # index denote the index of the cell
        sample = {'ATAC': self.expr_ATAC[idx,:], 'RNA':self.expr_RNA[idx,:], 'index':idx}
        
        # if self.transform:
        #     sample = self.transform(sample)
        
        return sample

# # transform
# class standardize(object):

#     def __call__(self, sample):
#         sample_ATAC = StandardScaler().fit_transform(sample['ATAC'][None,:])
#         sample_RNA = StandardScaler().fit_transform(sample['RNA'][None,:])
#         return {'ATAC': torch.from_numpy(sample_ATAC.squeeze()), 'RNA':torch.from_numpy(sample_RNA.squeeze())}

class testDataset(Dataset):

    def __init__(self):

        self.expr_ATAC = torch.FloatTensor(np.random.rand(100, 1000))
        self.expr_RNA = torch.FloatTensor(np.random.rand(100, 1000))
        
    def __len__(self):
        # number of cells
        return len(self.expr_ATAC)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        # index denote the index of the cell
        sample = {'ATAC': self.expr_ATAC[idx,:], 'RNA':self.expr_RNA[idx,:], 'index':idx}
        
        # if self.transform:
        #     sample = self.transform(sample)
        
        return sample