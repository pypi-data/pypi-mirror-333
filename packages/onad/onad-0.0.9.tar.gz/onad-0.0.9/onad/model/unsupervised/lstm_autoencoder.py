import random
import numpy as np
import torch
import torch.nn as nn
from typing import Dict, Optional, Tuple
from onad.base.model import BaseModel


class LSTMAutoencoderModel(nn.Module):
    def __init__(
        self,
        input_size: int,
        encoder_hidden_size: int,
        latent_size: int,
        num_layers: int,
        dropout: float,
    ):
        super().__init__()
        self.encoder = nn.LSTM(
            input_size=input_size,
            hidden_size=encoder_hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True,
        )
        self.latent = nn.Linear(encoder_hidden_size, latent_size)
        self.decoder = nn.Linear(latent_size, input_size)

    def forward(
        self,
        x: torch.Tensor,
        hidden: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
    ) -> Tuple[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        # x shape: (batch_size, seq_len, input_size)
        encoder_output, hidden = self.encoder(x, hidden)
        latent = self.latent(encoder_output)
        decoded = self.decoder(latent)
        return decoded, hidden


class LSTMAutoencoder(BaseModel):
    def __init__(
        self,
        encoder_hidden_size: int,
        latent_size: int,
        num_layers: int = 1,
        learning_rate: float = 0.001,
        dropout: float = 0.0,
        warmup: int = 0,
        seed: Optional[int] = None,
    ):
        self.encoder_hidden_size = encoder_hidden_size
        self.latent_size = latent_size
        self.num_layers = num_layers
        self.learning_rate = learning_rate
        self.dropout = dropout
        self.warmup = warmup
        self.seed = seed
        self.feature_names = None
        self.model = None
        self.optimizer = None
        self.criterion = nn.MSELoss()
        self.encoder_hidden = None  # Stores (h_n, c_n) for encoder

        if self.seed is not None:
            self._set_seed(seed)

    @staticmethod
    def _set_seed(seed: int):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    def _initialize_model(self, x: Dict[str, float]):
        self.feature_names = sorted(x.keys())
        input_size = len(self.feature_names)
        self.model = LSTMAutoencoderModel(
            input_size=input_size,
            encoder_hidden_size=self.encoder_hidden_size,
            latent_size=self.latent_size,
            num_layers=self.num_layers,
            dropout=self.dropout,
        )
        self.optimizer = torch.optim.Adam(
            self.model.parameters(), lr=self.learning_rate
        )
        self.encoder_hidden = None  # Reset hidden state on initialization

    def _convert_x_to_tensor(self, x: Dict[str, float]) -> torch.Tensor:
        if sorted(x.keys()) != self.feature_names:
            raise ValueError("Features do not match initial features")
        values = [x[key] for key in self.feature_names]
        # Shape: (batch_size=1, seq_len=1, input_size)
        return torch.tensor(values, dtype=torch.float32).unsqueeze(0).unsqueeze(0)

    def learn_one(self, x: Dict[str, float]) -> None:
        if self.feature_names is None:
            self._initialize_model(x)
        x_tensor = self._convert_x_to_tensor(x)
        self.model.train()
        self.optimizer.zero_grad()
        output, new_hidden = self.model(x_tensor, self.encoder_hidden)
        loss = self.criterion(output, x_tensor)
        loss.backward()
        self.optimizer.step()
        # Detach hidden state to prevent backprop through entire history
        self.encoder_hidden = tuple(h.detach() for h in new_hidden)

    def score_one(self, x: Dict[str, float]) -> Optional[float]:
        if self.feature_names is None:
            self._initialize_model(x)
        x_tensor = self._convert_x_to_tensor(x)
        self.model.eval()
        with torch.no_grad():
            output, _ = self.model(x_tensor, self.encoder_hidden)
            loss = self.criterion(output, x_tensor)
        return loss.item()
