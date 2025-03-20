import json
from pathlib import Path

import torch
from loguru import logger

from evotrain.models.loi import natural_sort
from ..train.model import CloudNet


def load_model_files(
    model_path: str,
    idx=-1,
    load_last=False,
    model_config_only=False,
    classes=list(range(4)),
):
    """
    Load model from model path and return model, model_class_mapping, config
    """

    model_path = Path(model_path)
    with open(model_path / "config.json", "r") as file:
        model_config = json.load(file)
    input_bands = [band[4:] for band in model_config["bands_config"]["s2_bands"]]
    model_config["bands_config"]["s2_bands"] = input_bands

    if model_config["data_config"]["classify_snow"]:
        model_class_mapping = model_config["labels_config"][
            "cloudsen12_mergedclouds_extrasnow"
        ]
    else:
        model_class_mapping = model_config["labels_config"]["cloudsen12"]

    model_checkpoint_path = model_path / "checkpoints"
    logger.debug(f"Model checkpoint path: {model_checkpoint_path}")

    assert model_checkpoint_path.exists(), (
        f"Model checkpoint path {model_checkpoint_path} does not exist"
    )

    if load_last:
        model_checkpoint = model_checkpoint_path / "last.ckpt"
    else:
        available_checkpoints = natural_sort(model_checkpoint_path.glob("ep*.ckpt"))
        logger.debug(f"Available checkpoints: {available_checkpoints}")
        model_checkpoint = available_checkpoints[idx]
        logger.debug(f"Loading model from {model_checkpoint}")

    model_state_dict = torch.load(
        model_checkpoint,
        map_location="cpu",
        weights_only=True,  # NOTE define weights for better understanding
    )["state_dict"]
    logger.info(f"Model state dict loaded from {model_checkpoint}")

    if model_config_only:
        logger.info("Returning model configuration only")
        return model_config

    logger.info("Initializing CloudNet model")
    model = CloudNet(
        bands=model_config["bands_config"]["s2_bands"],
        classes=classes,
        arch=model_config["dl_model_config"]["arch"],
        backbone=model_config["dl_model_config"]["backbone"],
        activation=model_config["dl_model_config"]["activation"],
        loss=model_config["dl_model_config"]["loss"],
        learning_rate=model_config["dl_model_config"]["learning_rate"],
        class_weights_list=model_config["dl_model_config"]["class_weights_list"],
        sample_weights=model_config["dl_model_config"]["sample_weights"],
        label_smoothing_factor=model_config["dl_model_config"][
            "label_smoothing_factor"
        ],
        dropout_rate=model_config["dl_model_config"]["dropout_rate"],
        config=model_config,
        architecture_version=model_config["dl_model_config"]["architecture_version"],
        mlp_hidden_layers=model_config["dl_model_config"]["mlp_hidden_layers"],
        head_filters_settings=model_config["dl_model_config"]["head_filters_settings"],
        bands_head=model_config["dl_model_config"]["bands_head"],
    )
    model.load_state_dict(model_state_dict, strict=False)
    logger.info("Model state dict loaded successfully")

    model.eval()
    logger.info("Model set to evaluation mode")
    return model, model_class_mapping, model_config
