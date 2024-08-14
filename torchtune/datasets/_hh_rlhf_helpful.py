# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from typing import Dict, Optional

from torchtune.data import ChosenRejectedToMessages, PromptTemplate
from torchtune.datasets._preference import PreferenceDataset
from torchtune.modules.tokenizers import ModelTokenizer


def hh_rlhf_helpful_dataset(
    tokenizer: ModelTokenizer,
    *,
    source: str = "RLHFlow/HH-RLHF-Helpful-standard",
    column_map: Optional[Dict[str, str]] = None,
    prompt_template: Optional[PromptTemplate] = None,
    train_on_input: bool = False,
    split: str = "train",
) -> PreferenceDataset:
    """
    Constructs preference datasets similar to `Anthropic's helpful/harmless RLHF
    data
    <https://huggingface.co/datasets/RLHFlow/HH-RLHF-Helpful-standard>`_. This is
    the processed helpful subset of the original dataset in a standardized format.

    Args:
        tokenizer (ModelTokenizer): Tokenizer used by the model that implements the ``tokenize_messages`` method.
        source (str): path to dataset repository on Hugging Face. For local datasets,
            define source as the data file type (e.g. "json", "csv", "text") and pass
            in the filepath in ``data_files``. See Hugging Face's ``load_dataset``
            (https://huggingface.co/docs/datasets/en/package_reference/loading_methods#datasets.load_dataset.path)
            for more details. Default is ``RLHFlow/HH-RLHF-Helpful-standard``.
        column_map (Optional[Dict[str, str]]): a mapping from the expected columns in the prompt template
            to the new column names in the dataset. If None, assume these are identical.
        prompt_template (Optional[PromptTemplate]): optional template used to format the prompt. Default
            is None.
        train_on_input (bool): Whether the model is trained on the prompt or not. Default is False.
        split (str): ``split`` argument for ``datasets.load_dataset``. You can use this argument to load a subset
            of a given split, e.g. ``split="train[:10%]"``. Default is "train".

    Returns:
        PreferenceDataset: The preference dataset built from source paired data.
    """

    message_transform = ChosenRejectedToMessages(
        train_on_input=train_on_input, column_map=column_map
    )

    return PreferenceDataset(
        source=source,
        message_transform=message_transform,
        tokenizer=tokenizer,
        prompt_template=prompt_template,
        split=split,
    )