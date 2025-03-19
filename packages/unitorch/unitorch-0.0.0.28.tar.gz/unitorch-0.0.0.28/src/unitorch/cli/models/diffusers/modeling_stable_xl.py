# Copyright (c) FULIUCANSHENG.
# Licensed under the MIT License.

import torch
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from torch import autocast

from unitorch.models.diffusers import (
    StableXLForText2ImageGeneration as _StableXLForText2ImageGeneration,
    StableXLForImage2ImageGeneration as _StableXLForImage2ImageGeneration,
    StableXLForImageInpainting as _StableXLForImageInpainting,
)
from unitorch.utils import (
    pop_value,
    nested_dict_value,
    is_bfloat16_available,
    is_cuda_available,
)
from unitorch.cli import (
    cached_path,
    add_default_section_for_init,
    add_default_section_for_function,
    register_model,
)
from unitorch.cli.models import DiffusionOutputs, LossOutputs
from unitorch.cli.models import diffusion_model_decorator
from unitorch.cli.models.diffusers import (
    pretrained_stable_infos,
    pretrained_stable_extensions_infos,
    load_weight,
)


@register_model("core/model/diffusers/text2image/stable_xl", diffusion_model_decorator)
class StableXLForText2ImageGeneration(_StableXLForText2ImageGeneration):
    def __init__(
        self,
        config_path: str,
        text_config_path: str,
        text2_config_path: str,
        vae_config_path: str,
        scheduler_config_path: str,
        quant_config_path: Optional[str] = None,
        image_size: Optional[int] = None,
        in_channels: Optional[int] = None,
        out_channels: Optional[int] = None,
        num_train_timesteps: Optional[int] = 1000,
        num_infer_timesteps: Optional[int] = 50,
        freeze_vae_encoder: Optional[bool] = True,
        freeze_text_encoder: Optional[bool] = True,
        snr_gamma: Optional[float] = 5.0,
        seed: Optional[int] = 1123,
        use_fp16: Optional[bool] = True,
        use_bf16: Optional[bool] = False,
    ):
        super().__init__(
            config_path=config_path,
            text_config_path=text_config_path,
            text2_config_path=text2_config_path,
            vae_config_path=vae_config_path,
            scheduler_config_path=scheduler_config_path,
            quant_config_path=quant_config_path,
            image_size=image_size,
            in_channels=in_channels,
            out_channels=out_channels,
            num_train_timesteps=num_train_timesteps,
            num_infer_timesteps=num_infer_timesteps,
            freeze_vae_encoder=freeze_vae_encoder,
            freeze_text_encoder=freeze_text_encoder,
            snr_gamma=snr_gamma,
            seed=seed,
        )
        self.use_dtype = torch.float16 if use_fp16 else torch.float32
        self.use_dtype = (
            torch.bfloat16 if use_bf16 and is_bfloat16_available() else self.use_dtype
        )

    @classmethod
    @add_default_section_for_init("core/model/diffusers/text2image/stable_xl")
    def from_core_configure(cls, config, **kwargs):
        config.set_default_section("core/model/diffusers/text2image/stable_xl")
        pretrained_name = config.getoption("pretrained_name", "stable-xl-base")
        pretrained_infos = nested_dict_value(pretrained_stable_infos, pretrained_name)

        config_path = config.getoption("config_path", None)
        config_path = pop_value(
            config_path,
            nested_dict_value(pretrained_infos, "unet", "config"),
        )
        config_path = cached_path(config_path)

        text_config_path = config.getoption("text_config_path", None)
        text_config_path = pop_value(
            text_config_path,
            nested_dict_value(pretrained_infos, "text", "config"),
        )
        text_config_path = cached_path(text_config_path)

        text2_config_path = config.getoption("text2_config_path", None)
        text2_config_path = pop_value(
            text2_config_path,
            nested_dict_value(pretrained_infos, "text2", "config"),
        )
        text2_config_path = cached_path(text2_config_path)

        vae_config_path = config.getoption("vae_config_path", None)
        vae_config_path = pop_value(
            vae_config_path,
            nested_dict_value(pretrained_infos, "vae", "config"),
        )
        vae_config_path = cached_path(vae_config_path)

        scheduler_config_path = config.getoption("scheduler_config_path", None)
        scheduler_config_path = pop_value(
            scheduler_config_path,
            nested_dict_value(pretrained_infos, "scheduler"),
        )
        scheduler_config_path = cached_path(scheduler_config_path)

        quant_config_path = config.getoption("quant_config_path", None)
        if quant_config_path is not None:
            quant_config_path = cached_path(quant_config_path)

        image_size = config.getoption("image_size", None)
        in_channels = config.getoption("in_channels", None)
        out_channels = config.getoption("out_channels", None)
        num_train_timesteps = config.getoption("num_train_timesteps", 1000)
        num_infer_timesteps = config.getoption("num_infer_timesteps", 50)
        freeze_vae_encoder = config.getoption("freeze_vae_encoder", True)
        freeze_text_encoder = config.getoption("freeze_text_encoder", True)
        snr_gamma = config.getoption("snr_gamma", 5.0)
        seed = config.getoption("seed", 1123)
        use_fp16 = config.getoption("use_fp16", True)
        use_bf16 = config.getoption("use_bf16", False)

        inst = cls(
            config_path=config_path,
            text_config_path=text_config_path,
            text2_config_path=text2_config_path,
            vae_config_path=vae_config_path,
            scheduler_config_path=scheduler_config_path,
            quant_config_path=quant_config_path,
            image_size=image_size,
            in_channels=in_channels,
            out_channels=out_channels,
            num_train_timesteps=num_train_timesteps,
            num_infer_timesteps=num_infer_timesteps,
            freeze_vae_encoder=freeze_vae_encoder,
            freeze_text_encoder=freeze_text_encoder,
            snr_gamma=snr_gamma,
            seed=seed,
            use_fp16=use_fp16,
            use_bf16=use_bf16,
        )

        weight_path = config.getoption("pretrained_weight_path", None)

        state_dict = None
        if weight_path is None and pretrained_infos is not None:
            state_dict = [
                load_weight(
                    nested_dict_value(pretrained_infos, "unet", "weight"),
                    prefix_keys={"": "unet."},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "text", "weight"),
                    prefix_keys={"": "text."},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "text2", "weight"),
                    prefix_keys={"": "text2."},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "vae", "weight"),
                    prefix_keys={"": "vae."},
                ),
            ]

        elif weight_path is not None:
            state_dict = load_weight(weight_path)

        if state_dict is not None:
            inst.from_pretrained(state_dict=state_dict)

        pretrained_lora_names = config.getoption("pretrained_lora_names", None)
        pretrained_lora_weights = config.getoption("pretrained_lora_weights", 1.0)

        if isinstance(pretrained_lora_names, str):
            pretrained_lora_weights_path = nested_dict_value(
                pretrained_stable_extensions_infos,
                pretrained_lora_names,
                "lora",
                "weight",
            )
        elif isinstance(pretrained_lora_names, list):
            pretrained_lora_weights_path = [
                nested_dict_value(
                    pretrained_stable_extensions_infos, name, "lora", "weight"
                )
                for name in pretrained_lora_names
            ]
        else:
            pretrained_lora_weights_path = None

        lora_weights_path = config.getoption(
            "pretrained_lora_weights_path", pretrained_lora_weights_path
        )
        if lora_weights_path is not None:
            inst.load_lora_weights(
                lora_weights_path,
                pretrained_lora_weights,
                replace_keys={},
                save_base_state=False,
            )
        return inst

    def forward(
        self,
        input_ids: torch.Tensor,
        input2_ids: torch.Tensor,
        add_time_ids: torch.Tensor,
        pixel_values: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        attention2_mask: Optional[torch.Tensor] = None,
    ):
        with autocast(
            device_type=("cuda" if torch.cuda.is_available() else "cpu"),
            dtype=self.use_dtype,
        ):
            loss = super().forward(
                input_ids=input_ids,
                input2_ids=input2_ids,
                add_time_ids=add_time_ids,
                pixel_values=pixel_values,
                attention_mask=attention_mask,
                attention2_mask=attention2_mask,
            )
            return LossOutputs(loss=loss)

    @add_default_section_for_function("core/model/diffusers/text2image/stable_xl")
    def generate(
        self,
        input_ids: torch.Tensor,
        input2_ids: torch.Tensor,
        negative_input_ids: torch.Tensor,
        negative_input2_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        attention2_mask: Optional[torch.Tensor] = None,
        negative_attention_mask: Optional[torch.Tensor] = None,
        negative_attention2_mask: Optional[torch.Tensor] = None,
        height: Optional[int] = 1024,
        width: Optional[int] = 1024,
        guidance_scale: Optional[float] = 5.0,
    ):
        with autocast(
            device_type=("cuda" if torch.cuda.is_available() else "cpu"),
            dtype=self.use_dtype,
        ):
            outputs = super().generate(
                input_ids=input_ids,
                input2_ids=input2_ids,
                negative_input_ids=negative_input_ids,
                negative_input2_ids=negative_input2_ids,
                attention_mask=attention_mask,
                attention2_mask=attention2_mask,
                negative_attention_mask=negative_attention_mask,
                negative_attention2_mask=negative_attention2_mask,
                height=height,
                width=width,
                guidance_scale=guidance_scale,
            )

            return DiffusionOutputs(outputs=outputs.images)


@register_model("core/model/diffusers/image2image/stable_xl", diffusion_model_decorator)
class StableXLForImage2ImageGeneration(_StableXLForImage2ImageGeneration):
    def __init__(
        self,
        config_path: str,
        text_config_path: str,
        text2_config_path: str,
        vae_config_path: str,
        scheduler_config_path: str,
        quant_config_path: Optional[str] = None,
        image_size: Optional[int] = None,
        in_channels: Optional[int] = None,
        out_channels: Optional[int] = None,
        num_train_timesteps: Optional[int] = 1000,
        num_infer_timesteps: Optional[int] = 50,
        freeze_vae_encoder: Optional[bool] = True,
        freeze_text_encoder: Optional[bool] = True,
        snr_gamma: Optional[float] = 5.0,
        seed: Optional[int] = 1123,
        use_fp16: Optional[bool] = True,
        use_bf16: Optional[bool] = False,
    ):
        super().__init__(
            config_path=config_path,
            text_config_path=text_config_path,
            text2_config_path=text2_config_path,
            vae_config_path=vae_config_path,
            scheduler_config_path=scheduler_config_path,
            quant_config_path=quant_config_path,
            image_size=image_size,
            in_channels=in_channels,
            out_channels=out_channels,
            num_train_timesteps=num_train_timesteps,
            num_infer_timesteps=num_infer_timesteps,
            freeze_vae_encoder=freeze_vae_encoder,
            freeze_text_encoder=freeze_text_encoder,
            snr_gamma=snr_gamma,
            seed=seed,
        )
        self.use_dtype = torch.float16 if use_fp16 else torch.float32
        self.use_dtype = (
            torch.bfloat16 if use_bf16 and is_bfloat16_available() else self.use_dtype
        )

    @classmethod
    @add_default_section_for_init("core/model/diffusers/image2image/stable_xl")
    def from_core_configure(cls, config, **kwargs):
        config.set_default_section("core/model/diffusers/image2image/stable_xl")
        pretrained_name = config.getoption("pretrained_name", "stable-xl-base")
        pretrained_infos = nested_dict_value(pretrained_stable_infos, pretrained_name)

        config_path = config.getoption("config_path", None)
        config_path = pop_value(
            config_path,
            nested_dict_value(pretrained_infos, "unet", "config"),
        )
        config_path = cached_path(config_path)

        text_config_path = config.getoption("text_config_path", None)
        text_config_path = pop_value(
            text_config_path,
            nested_dict_value(pretrained_infos, "text", "config"),
        )
        text_config_path = cached_path(text_config_path)

        text2_config_path = config.getoption("text2_config_path", None)
        text2_config_path = pop_value(
            text2_config_path,
            nested_dict_value(pretrained_infos, "text2", "config"),
        )
        text2_config_path = cached_path(text2_config_path)

        vae_config_path = config.getoption("vae_config_path", None)
        vae_config_path = pop_value(
            vae_config_path,
            nested_dict_value(pretrained_infos, "vae", "config"),
        )
        vae_config_path = cached_path(vae_config_path)

        scheduler_config_path = config.getoption("scheduler_config_path", None)
        scheduler_config_path = pop_value(
            scheduler_config_path,
            nested_dict_value(pretrained_infos, "scheduler"),
        )
        scheduler_config_path = cached_path(scheduler_config_path)

        quant_config_path = config.getoption("quant_config_path", None)
        if quant_config_path is not None:
            quant_config_path = cached_path(quant_config_path)

        image_size = config.getoption("image_size", None)
        in_channels = config.getoption("in_channels", None)
        out_channels = config.getoption("out_channels", None)
        num_train_timesteps = config.getoption("num_train_timesteps", 1000)
        num_infer_timesteps = config.getoption("num_infer_timesteps", 50)
        freeze_vae_encoder = config.getoption("freeze_vae_encoder", True)
        freeze_text_encoder = config.getoption("freeze_text_encoder", True)
        snr_gamma = config.getoption("snr_gamma", 5.0)
        seed = config.getoption("seed", 1123)
        use_fp16 = config.getoption("use_fp16", True)
        use_bf16 = config.getoption("use_bf16", False)

        inst = cls(
            config_path=config_path,
            text_config_path=text_config_path,
            text2_config_path=text2_config_path,
            vae_config_path=vae_config_path,
            scheduler_config_path=scheduler_config_path,
            quant_config_path=quant_config_path,
            image_size=image_size,
            in_channels=in_channels,
            out_channels=out_channels,
            num_train_timesteps=num_train_timesteps,
            num_infer_timesteps=num_infer_timesteps,
            freeze_vae_encoder=freeze_vae_encoder,
            freeze_text_encoder=freeze_text_encoder,
            snr_gamma=snr_gamma,
            seed=seed,
            use_fp16=use_fp16,
            use_bf16=use_bf16,
        )

        weight_path = config.getoption("pretrained_weight_path", None)

        state_dict = None
        if weight_path is None and pretrained_infos is not None:
            state_dict = [
                load_weight(
                    nested_dict_value(pretrained_infos, "unet", "weight"),
                    prefix_keys={"": "unet."},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "text", "weight"),
                    prefix_keys={"": "text."},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "text2", "weight"),
                    prefix_keys={"": "text2."},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "vae", "weight"),
                    prefix_keys={"": "vae."},
                ),
            ]

        elif weight_path is not None:
            state_dict = load_weight(weight_path)

        if state_dict is not None:
            inst.from_pretrained(state_dict=state_dict)

        pretrained_lora_names = config.getoption("pretrained_lora_names", None)
        pretrained_lora_weights = config.getoption("pretrained_lora_weights", 1.0)

        if isinstance(pretrained_lora_names, str):
            pretrained_lora_weights_path = nested_dict_value(
                pretrained_stable_extensions_infos,
                pretrained_lora_names,
                "lora",
                "weight",
            )
        elif isinstance(pretrained_lora_names, list):
            pretrained_lora_weights_path = [
                nested_dict_value(
                    pretrained_stable_extensions_infos, name, "lora", "weight"
                )
                for name in pretrained_lora_names
            ]
        else:
            pretrained_lora_weights_path = None

        lora_weights_path = config.getoption(
            "pretrained_lora_weights_path", pretrained_lora_weights_path
        )
        if lora_weights_path is not None:
            inst.load_lora_weights(
                lora_weights_path,
                pretrained_lora_weights,
                replace_keys={},
                save_base_state=False,
            )
        return inst

    def forward(
        self,
    ):
        raise NotImplementedError

    @add_default_section_for_function("core/model/diffusers/image2image/stable_xl")
    def generate(
        self,
        input_ids: torch.Tensor,
        input2_ids: torch.Tensor,
        negative_input_ids: torch.Tensor,
        negative_input2_ids: torch.Tensor,
        pixel_values: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        attention2_mask: Optional[torch.Tensor] = None,
        negative_attention_mask: Optional[torch.Tensor] = None,
        negative_attention2_mask: Optional[torch.Tensor] = None,
        strength: Optional[float] = 1.0,
        guidance_scale: Optional[float] = 7.5,
    ):
        with autocast(
            device_type=("cuda" if torch.cuda.is_available() else "cpu"),
            dtype=self.use_dtype,
        ):
            outputs = super().generate(
                input_ids=input_ids,
                input2_ids=input2_ids,
                negative_input_ids=negative_input_ids,
                negative_input2_ids=negative_input2_ids,
                pixel_values=pixel_values,
                attention_mask=attention_mask,
                attention2_mask=attention2_mask,
                negative_attention_mask=negative_attention_mask,
                negative_attention2_mask=negative_attention2_mask,
                strength=strength,
                guidance_scale=guidance_scale,
            )

            return DiffusionOutputs(outputs=outputs.images)


@register_model("core/model/diffusers/inpainting/stable_xl", diffusion_model_decorator)
class StableXLForImageInpainting(_StableXLForImageInpainting):
    def __init__(
        self,
        config_path: str,
        text_config_path: str,
        text2_config_path: str,
        vae_config_path: str,
        scheduler_config_path: str,
        quant_config_path: Optional[str] = None,
        image_size: Optional[int] = None,
        in_channels: Optional[int] = None,
        out_channels: Optional[int] = None,
        num_train_timesteps: Optional[int] = 1000,
        num_infer_timesteps: Optional[int] = 50,
        freeze_vae_encoder: Optional[bool] = True,
        freeze_text_encoder: Optional[bool] = True,
        snr_gamma: Optional[float] = 5.0,
        seed: Optional[int] = 1123,
        use_fp16: Optional[bool] = True,
        use_bf16: Optional[bool] = False,
    ):
        super().__init__(
            config_path=config_path,
            text_config_path=text_config_path,
            text2_config_path=text2_config_path,
            vae_config_path=vae_config_path,
            scheduler_config_path=scheduler_config_path,
            quant_config_path=quant_config_path,
            image_size=image_size,
            in_channels=in_channels,
            out_channels=out_channels,
            num_train_timesteps=num_train_timesteps,
            num_infer_timesteps=num_infer_timesteps,
            freeze_vae_encoder=freeze_vae_encoder,
            freeze_text_encoder=freeze_text_encoder,
            snr_gamma=snr_gamma,
            seed=seed,
        )
        self.use_dtype = torch.float16 if use_fp16 else torch.float32
        self.use_dtype = (
            torch.bfloat16 if use_bf16 and is_bfloat16_available() else self.use_dtype
        )

    @classmethod
    @add_default_section_for_init("core/model/diffusers/inpainting/stable_xl")
    def from_core_configure(cls, config, **kwargs):
        config.set_default_section("core/model/diffusers/inpainting/stable_xl")
        pretrained_name = config.getoption("pretrained_name", "stable-xl-base")
        pretrained_infos = nested_dict_value(pretrained_stable_infos, pretrained_name)

        config_path = config.getoption("config_path", None)
        config_path = pop_value(
            config_path,
            nested_dict_value(pretrained_infos, "unet", "config"),
        )
        config_path = cached_path(config_path)

        text_config_path = config.getoption("text_config_path", None)
        text_config_path = pop_value(
            text_config_path,
            nested_dict_value(pretrained_infos, "text", "config"),
        )
        text_config_path = cached_path(text_config_path)

        text2_config_path = config.getoption("text2_config_path", None)
        text2_config_path = pop_value(
            text2_config_path,
            nested_dict_value(pretrained_infos, "text2", "config"),
        )
        text2_config_path = cached_path(text2_config_path)

        vae_config_path = config.getoption("vae_config_path", None)
        vae_config_path = pop_value(
            vae_config_path,
            nested_dict_value(pretrained_infos, "vae", "config"),
        )
        vae_config_path = cached_path(vae_config_path)

        scheduler_config_path = config.getoption("scheduler_config_path", None)
        scheduler_config_path = pop_value(
            scheduler_config_path,
            nested_dict_value(pretrained_infos, "scheduler"),
        )
        scheduler_config_path = cached_path(scheduler_config_path)

        quant_config_path = config.getoption("quant_config_path", None)
        if quant_config_path is not None:
            quant_config_path = cached_path(quant_config_path)

        image_size = config.getoption("image_size", None)
        in_channels = config.getoption("in_channels", None)
        out_channels = config.getoption("out_channels", None)
        num_train_timesteps = config.getoption("num_train_timesteps", 1000)
        num_infer_timesteps = config.getoption("num_infer_timesteps", 50)
        freeze_vae_encoder = config.getoption("freeze_vae_encoder", True)
        freeze_text_encoder = config.getoption("freeze_text_encoder", True)
        snr_gamma = config.getoption("snr_gamma", 5.0)
        seed = config.getoption("seed", 1123)
        use_fp16 = config.getoption("use_fp16", True)
        use_bf16 = config.getoption("use_bf16", False)

        inst = cls(
            config_path=config_path,
            text_config_path=text_config_path,
            text2_config_path=text2_config_path,
            vae_config_path=vae_config_path,
            scheduler_config_path=scheduler_config_path,
            quant_config_path=quant_config_path,
            image_size=image_size,
            in_channels=in_channels,
            out_channels=out_channels,
            num_train_timesteps=num_train_timesteps,
            num_infer_timesteps=num_infer_timesteps,
            freeze_vae_encoder=freeze_vae_encoder,
            freeze_text_encoder=freeze_text_encoder,
            snr_gamma=snr_gamma,
            seed=seed,
            use_fp16=use_fp16,
            use_bf16=use_bf16,
        )

        weight_path = config.getoption("pretrained_weight_path", None)

        state_dict = None
        if weight_path is None and pretrained_infos is not None:
            state_dict = [
                load_weight(
                    nested_dict_value(pretrained_infos, "unet", "weight"),
                    prefix_keys={"": "unet."},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "text", "weight"),
                    prefix_keys={"": "text."},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "text2", "weight"),
                    prefix_keys={"": "text2."},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "vae", "weight"),
                    prefix_keys={"": "vae."},
                ),
            ]

        elif weight_path is not None:
            state_dict = load_weight(weight_path)

        if state_dict is not None:
            inst.from_pretrained(state_dict=state_dict)

        pretrained_lora_names = config.getoption("pretrained_lora_names", None)
        pretrained_lora_weights = config.getoption("pretrained_lora_weights", 1.0)

        if isinstance(pretrained_lora_names, str):
            pretrained_lora_weights_path = nested_dict_value(
                pretrained_stable_extensions_infos,
                pretrained_lora_names,
                "lora",
                "weight",
            )
        elif isinstance(pretrained_lora_names, list):
            pretrained_lora_weights_path = [
                nested_dict_value(
                    pretrained_stable_extensions_infos, name, "lora", "weight"
                )
                for name in pretrained_lora_names
            ]
        else:
            pretrained_lora_weights_path = None

        lora_weights_path = config.getoption(
            "pretrained_lora_weights_path", pretrained_lora_weights_path
        )
        if lora_weights_path is not None:
            inst.load_lora_weights(
                lora_weights_path,
                pretrained_lora_weights,
                replace_keys={},
                save_base_state=False,
            )
        return inst

    def forward(
        self,
        input_ids: torch.Tensor,
        input2_ids: torch.Tensor,
        add_time_ids: torch.Tensor,
        pixel_values: torch.Tensor,
        pixel_masks: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        attention2_mask: Optional[torch.Tensor] = None,
    ):
        with autocast(
            device_type=("cuda" if torch.cuda.is_available() else "cpu"),
            dtype=self.use_dtype,
        ):
            loss = super().forward(
                input_ids=input_ids,
                input2_ids=input2_ids,
                add_time_ids=add_time_ids,
                pixel_values=pixel_values,
                pixel_masks=pixel_masks,
                attention_mask=attention_mask,
                attention2_mask=attention2_mask,
            )
            return LossOutputs(loss=loss)

    @add_default_section_for_function("core/model/diffusers/inpainting/stable_xl")
    def generate(
        self,
        input_ids: torch.Tensor,
        input2_ids: torch.Tensor,
        negative_input_ids: torch.Tensor,
        negative_input2_ids: torch.Tensor,
        pixel_values: torch.Tensor,
        pixel_masks: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        attention2_mask: Optional[torch.Tensor] = None,
        negative_attention_mask: Optional[torch.Tensor] = None,
        negative_attention2_mask: Optional[torch.Tensor] = None,
        strength: Optional[float] = 1.0,
        guidance_scale: Optional[float] = 7.5,
    ):
        with autocast(
            device_type=("cuda" if torch.cuda.is_available() else "cpu"),
            dtype=self.use_dtype,
        ):
            outputs = super().generate(
                input_ids=input_ids,
                input2_ids=input2_ids,
                negative_input_ids=negative_input_ids,
                negative_input2_ids=negative_input2_ids,
                pixel_values=pixel_values,
                pixel_masks=pixel_masks,
                attention_mask=attention_mask,
                attention2_mask=attention2_mask,
                negative_attention_mask=negative_attention_mask,
                negative_attention2_mask=negative_attention2_mask,
                strength=strength,
                guidance_scale=guidance_scale,
            )

            return DiffusionOutputs(outputs=outputs.images)
