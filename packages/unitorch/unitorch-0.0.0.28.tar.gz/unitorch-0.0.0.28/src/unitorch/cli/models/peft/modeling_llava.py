# Copyright (c) FULIUCANSHENG.
# Licensed under the MIT License.

import os
import logging
import torch
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from torch import autocast
from transformers.utils import is_remote_url
from unitorch.utils import pop_value, nested_dict_value
from unitorch.models.peft import (
    LlavaMistralClipLoraForClassification as _LlavaMistralClipLoraForClassification,
    LlavaMistralClipLoraForGeneration as _LlavaMistralClipLoraForGeneration,
    LlavaLlamaSiglipLoraForGeneration as _LlavaLlamaSiglipLoraForGeneration,
)
from unitorch.cli import (
    cached_path,
    add_default_section_for_init,
    add_default_section_for_function,
    register_model,
)
from unitorch.cli.models import generation_model_decorator
from unitorch.cli.models import ClassificationOutputs, GenerationOutputs, LossOutputs
from unitorch.cli.models.llava import pretrained_llava_infos


@register_model("core/model/classification/peft/lora/llava/mistral_clip")
class LlavaMistralClipLoraForClassification(_LlavaMistralClipLoraForClassification):
    """LlavaMistralClipLora model for classification tasks."""

    def __init__(
        self,
        config_path: str,
        quant_config_path: Optional[str] = None,
        image_token_index: Optional[int] = 32000,
        lora_r: Optional[int] = 16,
        lora_alpha: Optional[int] = 32,
        lora_dropout: Optional[float] = 0.05,
        fan_in_fan_out: Optional[bool] = True,
        target_modules: Optional[Union[List[str], str]] = ["q_proj", "v_proj"],
        num_classes: Optional[int] = 1,
        freeze_multi_modal_projector: Optional[bool] = True,
        freeze_classifer: Optional[bool] = True,
        gradient_checkpointing: Optional[bool] = False,
    ):
        """
        Initialize the LlavaMistralClipLoraForClassification model.

        Args:
            config_path (str): The path to the model configuration file.
            lora_r (int, optional): The number of Lora ranks. Defaults to 16.
            lora_alpha (int, optional): The Lora alpha value. Defaults to 32.
            lora_dropout (float, optional): The Lora dropout rate. Defaults to 0.05.
            fan_in_fan_out (bool, optional): Whether to use fan-in/fan-out weight initialization. Defaults to True.
            target_modules (Union[List[str], str], optional): The target modules for Lora regularization. Defaults to ["q_proj", "v_proj"].
            num_classes (int, optional): The number of classes. Defaults to 1.
            gradient_checkpointing (bool, optional): Whether to use gradient checkpointing during training. Defaults to False.
        """
        super().__init__(
            config_path=config_path,
            quant_config_path=quant_config_path,
            image_token_index=image_token_index,
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            fan_in_fan_out=fan_in_fan_out,
            target_modules=target_modules,
            num_classes=num_classes,
            freeze_multi_modal_projector=freeze_multi_modal_projector,
            freeze_classifer=freeze_classifer,
            gradient_checkpointing=gradient_checkpointing,
        )

    @classmethod
    @add_default_section_for_init(
        "core/model/classification/peft/lora/llava/mistral_clip"
    )
    def from_core_configure(cls, config, **kwargs):
        """
        Create an instance of LlavaMistralClipLoraForClassification from a core configuration.

        Args:
            config: The core configuration.
            **kwargs: Additional keyword arguments.

        Returns:
            LlavaMistralClipLoraForClassification: The initialized LlavaMistralClipLoraForClassification instance.
        """
        config.set_default_section(
            "core/model/classification/peft/lora/llava/mistral_clip"
        )
        pretrained_name = config.getoption(
            "pretrained_name", "llava-v1.6-mistral-7b-hf"
        )
        config_path = config.getoption("config_path", None)
        config_path = pop_value(
            config_path,
            nested_dict_value(pretrained_llava_infos, pretrained_name, "config"),
        )
        config_path = cached_path(config_path)

        quant_config_path = config.getoption("quant_config_path", None)
        if quant_config_path is not None:
            quant_config_path = cached_path(quant_config_path)

        image_token_index = config.getoption("image_token_index", 32000)
        lora_r = config.getoption("lora_r", 16)
        lora_alpha = config.getoption("lora_alpha", 32)
        lora_dropout = config.getoption("lora_dropout", 0.05)
        fan_in_fan_out = config.getoption("fan_in_fan_out", True)
        target_modules = config.getoption("target_modules", ["q_proj", "v_proj"])
        freeze_multi_modal_projector = config.getoption(
            "freeze_multi_modal_projector", True
        )
        freeze_classifer = config.getoption("freeze_classifer", True)
        gradient_checkpointing = config.getoption("gradient_checkpointing", False)
        num_classes = config.getoption("num_classes", 1)

        inst = cls(
            config_path,
            quant_config_path=quant_config_path,
            image_token_index=image_token_index,
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            fan_in_fan_out=fan_in_fan_out,
            target_modules=target_modules,
            num_classes=num_classes,
            freeze_multi_modal_projector=freeze_multi_modal_projector,
            freeze_classifer=freeze_classifer,
            gradient_checkpointing=gradient_checkpointing,
        )

        weight_path = []
        pretrained_weight_path = config.getoption("pretrained_weight_path", None)
        pretrained_weight_path = pop_value(
            pretrained_weight_path,
            nested_dict_value(pretrained_llava_infos, pretrained_name, "weight"),
            check_none=False,
        )
        if pretrained_weight_path is not None:
            if isinstance(pretrained_weight_path, str):
                weight_path.append(pretrained_weight_path)
            elif isinstance(pretrained_weight_path, list):
                weight_path.extend(pretrained_weight_path)

        pretrained_lora_weight_path = config.getoption(
            "pretrained_lora_weight_path", None
        )
        if pretrained_lora_weight_path is not None:
            weight_path.append(pretrained_lora_weight_path)

        if len(weight_path) > 0:
            inst.from_pretrained(
                weight_path=weight_path,
            )

        return inst

    @autocast(device_type=("cuda" if torch.cuda.is_available() else "cpu"))
    def forward(
        self,
        input_ids: torch.Tensor,
        pixel_values: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
    ):
        """
        Perform forward pass of the LlavaMistralClipLoraForClassification model.

        Args:
            input_ids (torch.Tensor): The input IDs.
            attention_mask (torch.Tensor, optional): The attention mask.
            position_ids (torch.Tensor, optional): The position IDs.

        Returns:
            ClassificationOutputs: The output of the classification task.
        """
        outputs = super().forward(
            input_ids=input_ids,
            pixel_values=pixel_values,
            attention_mask=attention_mask,
        )
        return ClassificationOutputs(outputs=outputs)


@register_model(
    "core/model/generation/peft/lora/llava/mistral_clip",
    generation_model_decorator,
)
class LlavaMistralClipLoraForGeneration(_LlavaMistralClipLoraForGeneration):
    """LlavaMistralClipLora model for generation tasks."""

    def __init__(
        self,
        config_path: str,
        quant_config_path: Optional[str] = None,
        image_token_index: Optional[int] = 32000,
        lora_r: Optional[int] = 16,
        lora_alpha: Optional[int] = 32,
        lora_dropout: Optional[float] = 0.05,
        fan_in_fan_out: Optional[bool] = True,
        target_modules: Optional[Union[List[str], str]] = ["q_proj", "v_proj"],
        freeze_multi_modal_projector: Optional[bool] = True,
        gradient_checkpointing: Optional[bool] = False,
    ):
        """
        Initialize the LlavaMistralClipLoraForGeneration model.

        Args:
            config_path (str): The path to the model configuration file.
            lora_r (int, optional): The number of Lora ranks. Defaults to 16.
            lora_alpha (int, optional): The Lora alpha value. Defaults to 32.
            lora_dropout (float, optional): The Lora dropout rate. Defaults to 0.05.
            fan_in_fan_out (bool, optional): Whether to use fan-in/fan-out weight initialization. Defaults to True.
            target_modules (Union[List[str], str], optional): The target modules for Lora regularization. Defaults to ["q_proj", "v_proj"].
            gradient_checkpointing (bool, optional): Whether to use gradient checkpointing during training. Defaults to False.
        """
        super().__init__(
            config_path=config_path,
            quant_config_path=quant_config_path,
            image_token_index=image_token_index,
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            fan_in_fan_out=fan_in_fan_out,
            target_modules=target_modules,
            freeze_multi_modal_projector=freeze_multi_modal_projector,
            gradient_checkpointing=gradient_checkpointing,
        )

    @classmethod
    @add_default_section_for_init("core/model/generation/peft/lora/llava/mistral_clip")
    def from_core_configure(cls, config, **kwargs):
        """
        Create an instance of LlavaMistralClipLoraForGeneration from a core configuration.

        Args:
            config: The core configuration.
            **kwargs: Additional keyword arguments.

        Returns:
            LlavaMistralClipLoraForGeneration: The initialized LlavaMistralClipLoraForGeneration instance.
        """
        config.set_default_section("core/model/generation/peft/lora/llava/mistral_clip")
        pretrained_name = config.getoption(
            "pretrained_name", "llava-v1.6-mistral-7b-hf"
        )
        config_path = config.getoption("config_path", None)
        config_path = pop_value(
            config_path,
            nested_dict_value(pretrained_llava_infos, pretrained_name, "config"),
        )
        config_path = cached_path(config_path)
        quant_config_path = config.getoption("quant_config_path", None)
        if quant_config_path is not None:
            quant_config_path = cached_path(quant_config_path)

        image_token_index = config.getoption("image_token_index", 32000)
        lora_r = config.getoption("lora_r", 16)
        lora_alpha = config.getoption("lora_alpha", 32)
        lora_dropout = config.getoption("lora_dropout", 0.05)
        fan_in_fan_out = config.getoption("fan_in_fan_out", True)
        target_modules = config.getoption("target_modules", ["q_proj", "v_proj"])
        freeze_multi_modal_projector = config.getoption(
            "freeze_multi_modal_projector", True
        )
        gradient_checkpointing = config.getoption("gradient_checkpointing", False)

        inst = cls(
            config_path,
            quant_config_path=quant_config_path,
            image_token_index=image_token_index,
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            fan_in_fan_out=fan_in_fan_out,
            target_modules=target_modules,
            freeze_multi_modal_projector=freeze_multi_modal_projector,
            gradient_checkpointing=gradient_checkpointing,
        )

        weight_path = []
        pretrained_weight_path = config.getoption("pretrained_weight_path", None)
        pretrained_weight_path = pop_value(
            pretrained_weight_path,
            nested_dict_value(pretrained_llava_infos, pretrained_name, "weight"),
            check_none=False,
        )
        if pretrained_weight_path is not None:
            if isinstance(pretrained_weight_path, str):
                weight_path.append(pretrained_weight_path)
            elif isinstance(pretrained_weight_path, list):
                weight_path.extend(pretrained_weight_path)

        pretrained_lora_weight_path = config.getoption(
            "pretrained_lora_weight_path", None
        )
        if pretrained_lora_weight_path is not None:
            weight_path.append(pretrained_lora_weight_path)

        if len(weight_path) > 0:
            inst.from_pretrained(
                weight_path=weight_path,
            )

        return inst

    @autocast(device_type=("cuda" if torch.cuda.is_available() else "cpu"))
    def forward(
        self,
        input_ids: torch.Tensor,
        pixel_values: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
    ):
        """
        Perform forward pass of the LlavaMistralClipLoraForGeneration model.

        Args:
            input_ids (torch.Tensor, optional): The input IDs.
            attention_mask (torch.Tensor, optional): The attention mask.
            position_ids (torch.Tensor, optional): The position IDs.

        Returns:
            GenerationOutputs: The output of the generation task.
        """
        outputs = super().forward(
            input_ids=input_ids,
            pixel_values=pixel_values,
            attention_mask=attention_mask,
        )
        return GenerationOutputs(sequences=outputs)

    @add_default_section_for_function(
        "core/model/generation/peft/lora/llava/mistral_clip"
    )
    @torch.no_grad()
    @autocast(device_type=("cuda" if torch.cuda.is_available() else "cpu"))
    def generate(
        self,
        input_ids: torch.Tensor,
        pixel_values: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        num_beams: Optional[int] = 5,
        decoder_start_token_id: Optional[int] = 1,
        decoder_end_token_id: Optional[Union[int, List[int]]] = 2,
        num_return_sequences: Optional[int] = 1,
        min_gen_seq_length: Optional[int] = 0,
        max_gen_seq_length: Optional[int] = 48,
        repetition_penalty: Optional[float] = 1.0,
        no_repeat_ngram_size: Optional[int] = 0,
        early_stopping: Optional[bool] = True,
        length_penalty: Optional[float] = 1.0,
        num_beam_groups: Optional[int] = 1,
        diversity_penalty: Optional[float] = 0.0,
        do_sample: Optional[bool] = False,
        temperature: Optional[float] = 1.0,
        top_k: Optional[int] = 50,
        top_p: Optional[float] = 1.0,
    ):
        """
        Generate sequences using the LlavaMistralClip model.

        Args:
            input_ids (torch.Tensor): Input token IDs.
            num_beams (int, optional): Number of beams for beam search. Defaults to 5.
            decoder_start_token_id (int, optional): Decoder start token ID. Defaults to 0.
            decoder_end_token_id (int or List[int], optional): The ID(s) of the decoder end token(s). Defaults to 1.
            num_return_sequences (int, optional): Number of generated sequences to return. Defaults to 1.
            min_gen_seq_length (int, optional): Minimum generation sequence length. Defaults to 0.
            max_gen_seq_length (int, optional): Maximum generation sequence length. Defaults to 48.
            repetition_penalty (float, optional): Repetition penalty. Defaults to 1.0.
            no_repeat_ngram_size (int, optional): Size of n-grams to prevent repetition. Defaults to 0.
            early_stopping (bool, optional): Whether to perform early stopping. Defaults to True.
            length_penalty (float, optional): Length penalty. Defaults to 1.0.
            num_beam_groups (int, optional): Number of beam groups for diverse beam search. Defaults to 1.
            diversity_penalty (float, optional): Diversity penalty for diverse beam search. Defaults to 0.0.
            do_sample (bool, optional): Whether to use sampling for generation. Defaults to False.
            temperature (float, optional): Sampling temperature. Defaults to 1.0.
            top_k (int, optional): Top-k sampling parameter. Defaults to 50.
            top_p (float, optional): Top-p sampling parameter. Defaults to 1.0.

        Returns:
            GenerationOutputs: The generation outputs.
        """
        outputs = super().generate(
            input_ids,
            pixel_values=pixel_values,
            attention_mask=attention_mask,
            num_beams=num_beams,
            decoder_start_token_id=decoder_start_token_id,
            decoder_end_token_id=decoder_end_token_id,
            num_return_sequences=num_return_sequences,
            min_gen_seq_length=min_gen_seq_length,
            max_gen_seq_length=max_gen_seq_length,
            repetition_penalty=repetition_penalty,
            no_repeat_ngram_size=no_repeat_ngram_size,
            early_stopping=early_stopping,
            length_penalty=length_penalty,
            num_beam_groups=num_beam_groups,
            diversity_penalty=diversity_penalty,
            do_sample=do_sample,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        )

        return GenerationOutputs(
            sequences=outputs.sequences,
            sequences_scores=outputs.sequences_scores,
        )


@register_model(
    "core/model/generation/peft/lora/llava/llama_siglip",
    generation_model_decorator,
)
class LlavaLlamaSiglipLoraForGeneration(_LlavaLlamaSiglipLoraForGeneration):
    """LlavaMistralClipLora model for generation tasks."""

    def __init__(
        self,
        config_path: str,
        quant_config_path: Optional[str] = None,
        image_token_index: Optional[int] = 128077,
        lora_r: Optional[int] = 16,
        lora_alpha: Optional[int] = 32,
        lora_dropout: Optional[float] = 0.05,
        fan_in_fan_out: Optional[bool] = True,
        target_modules: Optional[Union[List[str], str]] = ["q_proj", "v_proj"],
        freeze_multi_modal_projector: Optional[bool] = True,
        gradient_checkpointing: Optional[bool] = False,
    ):
        """
        Initialize the LlavaMistralClipLoraForGeneration model.

        Args:
            config_path (str): The path to the model configuration file.
            lora_r (int, optional): The number of Lora ranks. Defaults to 16.
            lora_alpha (int, optional): The Lora alpha value. Defaults to 32.
            lora_dropout (float, optional): The Lora dropout rate. Defaults to 0.05.
            fan_in_fan_out (bool, optional): Whether to use fan-in/fan-out weight initialization. Defaults to True.
            target_modules (Union[List[str], str], optional): The target modules for Lora regularization. Defaults to ["q_proj", "v_proj"].
            gradient_checkpointing (bool, optional): Whether to use gradient checkpointing during training. Defaults to False.
        """
        super().__init__(
            config_path=config_path,
            quant_config_path=quant_config_path,
            image_token_index=image_token_index,
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            fan_in_fan_out=fan_in_fan_out,
            target_modules=target_modules,
            freeze_multi_modal_projector=freeze_multi_modal_projector,
            gradient_checkpointing=gradient_checkpointing,
        )

    @classmethod
    @add_default_section_for_init("core/model/generation/peft/lora/llava/llama_siglip")
    def from_core_configure(cls, config, **kwargs):
        """
        Create an instance of LlavaMistralClipLoraForGeneration from a core configuration.

        Args:
            config: The core configuration.
            **kwargs: Additional keyword arguments.

        Returns:
            LlavaMistralClipLoraForGeneration: The initialized LlavaMistralClipLoraForGeneration instance.
        """
        config.set_default_section("core/model/generation/peft/lora/llava/llama_siglip")
        pretrained_name = config.getoption("pretrained_name", "llava-v1.6-joycaption-2")
        config_path = config.getoption("config_path", None)
        config_path = pop_value(
            config_path,
            nested_dict_value(pretrained_llava_infos, pretrained_name, "config"),
        )
        config_path = cached_path(config_path)
        quant_config_path = config.getoption("quant_config_path", None)
        if quant_config_path is not None:
            quant_config_path = cached_path(quant_config_path)

        image_token_index = config.getoption("image_token_index", 128077)
        lora_r = config.getoption("lora_r", 16)
        lora_alpha = config.getoption("lora_alpha", 32)
        lora_dropout = config.getoption("lora_dropout", 0.05)
        fan_in_fan_out = config.getoption("fan_in_fan_out", True)
        target_modules = config.getoption("target_modules", ["q_proj", "v_proj"])
        freeze_multi_modal_projector = config.getoption(
            "freeze_multi_modal_projector", True
        )
        gradient_checkpointing = config.getoption("gradient_checkpointing", False)

        inst = cls(
            config_path,
            quant_config_path=quant_config_path,
            image_token_index=image_token_index,
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            fan_in_fan_out=fan_in_fan_out,
            target_modules=target_modules,
            freeze_multi_modal_projector=freeze_multi_modal_projector,
            gradient_checkpointing=gradient_checkpointing,
        )

        weight_path = []
        pretrained_weight_path = config.getoption("pretrained_weight_path", None)
        pretrained_weight_path = pop_value(
            pretrained_weight_path,
            nested_dict_value(pretrained_llava_infos, pretrained_name, "weight"),
            check_none=False,
        )
        if pretrained_weight_path is not None:
            if isinstance(pretrained_weight_path, str):
                weight_path.append(pretrained_weight_path)
            elif isinstance(pretrained_weight_path, list):
                weight_path.extend(pretrained_weight_path)

        pretrained_lora_weight_path = config.getoption(
            "pretrained_lora_weight_path", None
        )
        if pretrained_lora_weight_path is not None:
            weight_path.append(pretrained_lora_weight_path)

        if len(weight_path) > 0:
            inst.from_pretrained(
                weight_path=weight_path,
            )

        return inst

    @autocast(device_type=("cuda" if torch.cuda.is_available() else "cpu"))
    def forward(
        self,
        input_ids: torch.Tensor,
        pixel_values: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
    ):
        """
        Perform forward pass of the LlavaMistralClipLoraForGeneration model.

        Args:
            input_ids (torch.Tensor, optional): The input IDs.
            attention_mask (torch.Tensor, optional): The attention mask.
            position_ids (torch.Tensor, optional): The position IDs.

        Returns:
            GenerationOutputs: The output of the generation task.
        """
        outputs = super().forward(
            input_ids=input_ids,
            pixel_values=pixel_values,
            attention_mask=attention_mask,
        )
        return GenerationOutputs(sequences=outputs)

    @add_default_section_for_function(
        "core/model/generation/peft/lora/llava/llama_siglip"
    )
    @torch.no_grad()
    @autocast(device_type=("cuda" if torch.cuda.is_available() else "cpu"))
    def generate(
        self,
        input_ids: torch.Tensor,
        pixel_values: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        num_beams: Optional[int] = 5,
        decoder_start_token_id: Optional[int] = 128000,
        decoder_end_token_id: Optional[Union[int, List[int]]] = [
            128001,
            128008,
            128009,
        ],
        num_return_sequences: Optional[int] = 1,
        min_gen_seq_length: Optional[int] = 0,
        max_gen_seq_length: Optional[int] = 48,
        repetition_penalty: Optional[float] = 1.0,
        no_repeat_ngram_size: Optional[int] = 0,
        early_stopping: Optional[bool] = True,
        length_penalty: Optional[float] = 1.0,
        num_beam_groups: Optional[int] = 1,
        diversity_penalty: Optional[float] = 0.0,
        do_sample: Optional[bool] = False,
        temperature: Optional[float] = 1.0,
        top_k: Optional[int] = 50,
        top_p: Optional[float] = 1.0,
    ):
        """
        Generate sequences using the LlavaMistralClip model.

        Args:
            input_ids (torch.Tensor): Input token IDs.
            num_beams (int, optional): Number of beams for beam search. Defaults to 5.
            decoder_start_token_id (int, optional): Decoder start token ID. Defaults to 0.
            decoder_end_token_id (int or List[int], optional): The ID(s) of the decoder end token(s). Defaults to 1.
            num_return_sequences (int, optional): Number of generated sequences to return. Defaults to 1.
            min_gen_seq_length (int, optional): Minimum generation sequence length. Defaults to 0.
            max_gen_seq_length (int, optional): Maximum generation sequence length. Defaults to 48.
            repetition_penalty (float, optional): Repetition penalty. Defaults to 1.0.
            no_repeat_ngram_size (int, optional): Size of n-grams to prevent repetition. Defaults to 0.
            early_stopping (bool, optional): Whether to perform early stopping. Defaults to True.
            length_penalty (float, optional): Length penalty. Defaults to 1.0.
            num_beam_groups (int, optional): Number of beam groups for diverse beam search. Defaults to 1.
            diversity_penalty (float, optional): Diversity penalty for diverse beam search. Defaults to 0.0.
            do_sample (bool, optional): Whether to use sampling for generation. Defaults to False.
            temperature (float, optional): Sampling temperature. Defaults to 1.0.
            top_k (int, optional): Top-k sampling parameter. Defaults to 50.
            top_p (float, optional): Top-p sampling parameter. Defaults to 1.0.

        Returns:
            GenerationOutputs: The generation outputs.
        """
        outputs = super().generate(
            input_ids,
            pixel_values=pixel_values,
            attention_mask=attention_mask,
            num_beams=num_beams,
            decoder_start_token_id=decoder_start_token_id,
            decoder_end_token_id=decoder_end_token_id,
            num_return_sequences=num_return_sequences,
            min_gen_seq_length=min_gen_seq_length,
            max_gen_seq_length=max_gen_seq_length,
            repetition_penalty=repetition_penalty,
            no_repeat_ngram_size=no_repeat_ngram_size,
            early_stopping=early_stopping,
            length_penalty=length_penalty,
            num_beam_groups=num_beam_groups,
            diversity_penalty=diversity_penalty,
            do_sample=do_sample,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        )

        return GenerationOutputs(
            sequences=outputs.sequences,
            sequences_scores=outputs.sequences_scores,
        )
