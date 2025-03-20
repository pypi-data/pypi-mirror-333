import random
import numpy as np
import torch
import torch.nn as nn
from typing import Dict, Optional, List, Tuple
from onad.base.model import BaseModel
from operator import itemgetter


class LSTMAutoencoderModel(nn.Module):
    def __init__(
        self,
        input_size: int,
        encoder_units: List[int],
        latent_size: int,
        decoder_units: List[int],
        dropout: float,
    ):
        super().__init__()

        self.encoder_lstms = nn.ModuleList()
        self.encoder_dropouts = nn.ModuleList()
        in_features = input_size
        for i, units in enumerate(encoder_units):
            self.encoder_lstms.append(
                nn.LSTM(input_size=in_features, hidden_size=units, batch_first=True)
            )
            if i < len(encoder_units) - 1:  # Add dropout between layers
                self.encoder_dropouts.append(nn.Dropout(dropout))
            in_features = units

        # Latent projection
        self.latent = nn.Linear(in_features, latent_size)

        # Decoder network
        decoder_layers = []
        in_features = latent_size
        for units in decoder_units:
            decoder_layers.append(nn.Linear(in_features, units))
            decoder_layers.append(nn.LeakyReLU(0.01))
            decoder_layers.append(nn.Dropout(dropout))
            in_features = units
        decoder_layers.append(nn.Linear(in_features, input_size))
        self.decoder = nn.Sequential(*decoder_layers)

    def forward(
        self,
        x: torch.Tensor,
        hidden: Optional[List[Tuple[torch.Tensor, torch.Tensor]]] = None,
    ) -> Tuple[torch.Tensor, List[Tuple[torch.Tensor, torch.Tensor]]]:
        new_hidden = []
        for i, lstm in enumerate(self.encoder_lstms):
            layer_hidden = hidden[i] if hidden else None
            x, layer_state = lstm(x, layer_hidden)
            new_hidden.append((layer_state[0].detach(), layer_state[1].detach()))
            if i < len(self.encoder_dropouts):
                x = self.encoder_dropouts[i](x)

        latent = self.latent(x)
        decoded = self.decoder(latent.squeeze(1)).unsqueeze(1)
        return decoded, new_hidden


class LSTMAutoencoder(BaseModel):
    def __init__(
        self,
        encoder_units: List[int] = [64],
        decoder_units: List[int] = [64],
        latent_size: int = 32,
        learning_rate: float = 0.001,
        dropout: float = 0.1,
        seed: Optional[int] = None,
    ):
        self.encoder_units = encoder_units
        self.decoder_units = decoder_units
        self.latent_size = latent_size
        self.learning_rate = learning_rate
        self.dropout = dropout
        self.seed = seed
        self.feature_names = None
        self.feature_getter = None  # Use itemgetter for optimized access
        self.model = None
        self.optimizer = None
        self.criterion = nn.MSELoss()
        self.hidden_state = None

        if self.seed is not None:
            self._set_seed(seed)

    @staticmethod
    def _set_seed(seed: int):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = False
        torch.backends.cudnn.benchmark = True  # Enables fast algorithm selection
        torch.backends.cudnn.enabled = True  # Optimized CUDA kernels (if applicable)

    def _initialize_model(self, x: Dict[str, float]):
        self.feature_names = sorted(x.keys())
        self.feature_getter = itemgetter(
            *self.feature_names
        )  # Optimized feature lookup
        input_size = len(self.feature_names)

        self.model = LSTMAutoencoderModel(
            input_size=input_size,
            encoder_units=self.encoder_units,
            latent_size=self.latent_size,
            decoder_units=self.decoder_units,
            dropout=self.dropout,
        )

        self.model = torch.compile(self.model, mode="max-autotune")

        self.optimizer = torch.optim.Adam(
            self.model.parameters(), lr=self.learning_rate
        )
        self.hidden_state = None

    def _convert_x_to_tensor(self, x: Dict[str, float]) -> torch.Tensor:
        if sorted(x.keys()) != self.feature_names:
            raise ValueError("Features do not match initial features")
        values = self.feature_getter(x)  # Faster lookup using itemgetter
        return torch.tensor(values, dtype=torch.float32).unsqueeze(0).unsqueeze(0)

    def learn_one(self, x: Dict[str, float]) -> None:
        if self.feature_names is None:
            self._initialize_model(x)
        x_tensor = self._convert_x_to_tensor(x)
        self.model.train()
        self.optimizer.zero_grad()

        output, new_hidden = self.model(x_tensor, self.hidden_state)
        loss = self.criterion(output, x_tensor)

        loss.backward()
        self.optimizer.step()
        self.hidden_state = [(h.detach(), c.detach()) for h, c in new_hidden]

    def score_one(self, x: Dict[str, float]) -> Optional[float]:
        if self.feature_names is None:
            self._initialize_model(x)
        x_tensor = self._convert_x_to_tensor(x)
        self.model.eval()
        with torch.no_grad():
            output, _ = self.model(x_tensor, self.hidden_state)
            loss = self.criterion(output, x_tensor)
        return loss.item()
