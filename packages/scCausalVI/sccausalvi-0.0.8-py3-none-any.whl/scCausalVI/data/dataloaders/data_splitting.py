import pytorch_lightning as pl
from scvi.data import AnnDataManager
import numpy as np
from typing import List, Optional
from scvi import settings
from scvi.dataloaders._data_splitting import validate_data_split
from scvi.model._utils import parse_device_args
from scCausalVI.data.dataloaders.scCausalVI_dataloader import scCausalDataLoader


class scCausalVIDataSplitter(pl.LightningDataModule):
    """
    Create scCausalDataLoader for training, validation, and test set.

    Args:
    ----
        adata_manager: `~scvi.data.AnnDataManager` object that has been created via ``setup_anndata``.
        group_indices_list: List where each element is a list of indices in the adata to load.
        train_size: Proportion of data to include in the training set.
        validation_size: Proportion of data to include in the validation set. The
            remaining proportion after `train_size` and `validation_size` is used for
            the test set.
        accelerator: Use default CPU or GPU if available.
        **kwargs: Keyword args for data loader (`ContrastiveDataLoader`).
    """

    def __init__(
            self,
            adata_manager: AnnDataManager,
            group_indices_list: List[List[int]],
            train_size: float = 0.9,
            validation_size: Optional[float] = 0.1,
            accelerator: str = 'cpu',
            batch_size:  int = 128,
            **kwargs,
    ) -> None:
        super().__init__()
        self.train_idx_per_group = None
        self.val_idx_per_group = None
        self.test_idx_per_group = None
        self.adata_manager = adata_manager
        self.group_indices_list = group_indices_list
        self.train_size = train_size
        self.validation_size = validation_size
        self.accelerator = accelerator
        self.batch_size = batch_size
        self.data_loader_kwargs = kwargs

        self.train_idx_per_group = []
        self.val_idx_per_group = []
        self.test_idx_per_group = []
        self.current_dataloader = None

        self.setup()

    def __iter__(self):
        if self.current_dataloader is None:
            self.current_dataloader = self.train_dataloader()
        return iter(self.current_dataloader)

    def __next__(self):
        if self.current_dataloader is None:
            self.current_dataloader = self.train_dataloader()
        return next(self.current_dataloader)

    def setup(self, stage: Optional[str] = None):
        random_state = np.random.RandomState(seed=settings.seed)

        for i, group_indices in enumerate(self.group_indices_list):
            n_train, n_val = validate_data_split(
                len(group_indices), self.train_size, self.validation_size
            )
            group_permutation = random_state.permutation(group_indices)

            self.val_idx_per_group.append(group_permutation[:n_val])
            self.train_idx_per_group.append(
                group_permutation[n_val: (n_val + n_train)]
            )
            self.test_idx_per_group.append(
                group_permutation[(n_train + n_val):]
            )

        accelerator, self.device = parse_device_args(
            self.accelerator,
        )
        print(f'accelerator: {accelerator}')
        self.pin_memory = True if accelerator == 'cuda' else False

        self.train_idx = np.concatenate(self.train_idx_per_group)
        self.val_idx = np.concatenate(self.val_idx_per_group)
        self.test_idx = np.concatenate(self.test_idx_per_group)

    def _get_scCausal_dataloader(
            self,
            group_indices_list: List[List[int]],
            shuffle: bool = True,
    ) -> scCausalDataLoader:
        return scCausalDataLoader(
            self.adata_manager,
            indices_list=group_indices_list,
            shuffle=shuffle,
            drop_last=False,
            batch_size=self.batch_size,
            **self.data_loader_kwargs,
        )

    def train_dataloader(self) -> scCausalDataLoader:
        return self._get_scCausal_dataloader(
            self.train_idx_per_group
        )

    def val_dataloader(self) -> scCausalDataLoader:
        if np.all([len(val_idx) > 0 for val_idx in self.val_idx_per_group]):
            return self._get_scCausal_dataloader(self.val_idx_per_group)
        else:
            raise ValueError('No validation data found.')
            # pass

    def test_dataloader(self) -> scCausalDataLoader:
        if np.all([len(test_idx) > 0 for test_idx in self.test_idx_per_group]):
            return self._get_scCausal_dataloader(self.test_idx_per_group)
        else:
            pass
