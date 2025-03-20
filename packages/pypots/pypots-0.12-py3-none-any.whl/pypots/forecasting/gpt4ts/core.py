"""
The core wrapper assembles the submodules of GPT4TS forecasting model
and takes over the forward progress of the algorithm.

"""

# Created by Wenjie Du <wenjay.du@gmail.com>
# License: BSD-3-Clause

import torch.nn as nn

from ...nn.modules.gpt4ts import BackboneGPT4TS
from ...nn.modules.loss import Criterion, MSE


class _GPT4TS(nn.Module):
    def __init__(
        self,
        n_steps: int,
        n_features: int,
        n_pred_steps: int,
        n_pred_features: int,
        term: str,
        n_layers: int,
        patch_size: int,
        patch_stride: int,
        train_gpt_mlp: bool,
        d_ffn: int,
        dropout: float,
        embed: str,
        freq: str,
        training_loss: Criterion = MSE(),
    ):
        super().__init__()

        assert term in ["long", "short"], "forecasting term should be either 'long' or 'short'"
        self.n_pred_steps = n_pred_steps
        self.n_pred_features = n_pred_features
        self.training_loss = training_loss

        self.backbone = BackboneGPT4TS(
            term + "_term_forecast",
            n_steps,
            n_features,
            n_pred_steps,
            n_pred_features,
            n_layers,
            patch_size,
            patch_stride,
            train_gpt_mlp,
            d_ffn,
            dropout,
            embed,
            freq,
        )

    def forward(self, inputs: dict) -> dict:
        X, missing_mask = inputs["X"], inputs["missing_mask"]

        # GPT4TS backbone processing
        forecasting_result = self.backbone(X, missing_mask)
        # the raw output has length = n_steps+n_pred_steps, we only need the last n_pred_steps
        forecasting_result = forecasting_result[:, -self.n_pred_steps :]

        results = {
            "forecasting_data": forecasting_result,
        }

        # if in training mode, return results with losses
        if self.training:
            X_pred, X_pred_missing_mask = inputs["X_pred"], inputs["X_pred_missing_mask"]
            # `loss` is always the item for backward propagating to update the model
            results["loss"] = self.training_loss(X_pred, forecasting_result, X_pred_missing_mask)

        return results
