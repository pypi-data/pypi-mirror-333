import enum
import json
import math
from dataclasses import dataclass
from typing import Optional

import huggingface_hub


@dataclass
class GPUTypeMixin:
    memory_gb: int
    uid: str
    vendor: str


class GPUType(GPUTypeMixin, enum.Enum):
    NV_A10G = 24, "a10g", "nvidia"


def _fetch_model_config(hub_model_id: str) -> dict:
    """Fetch model configuration from Hugging Face hub."""
    with open(huggingface_hub.hf_hub_download(hub_model_id, "config.json")) as file:
        return json.load(file)


def _get_attention_head_count(hub_model_id: str) -> int:
    """Get the number of attention heads from the model config."""
    config = _fetch_model_config(hub_model_id)
    return config.get("num_attention_heads")


def _get_max_position_embeddings(hub_model_id: str) -> int:
    """Get the maximum position embeddings from the model config."""
    config = _fetch_model_config(hub_model_id)
    return config.get("max_position_embeddings")


def _calculate_safetensors_size(hub_model_id: str) -> int:
    """Calculate the total size of safetensors files in the model repository."""
    safetensors_size = 0
    files = huggingface_hub.HfApi().list_repo_tree(hub_model_id)
    for file in files:
        if isinstance(file, huggingface_hub.hf_api.RepoFile) and file.path.endswith(
            ".safetensors"
        ):
            safetensors_size += file.size
        elif safetensors_size:
            break
    return safetensors_size


def recommend_gpu_count(
    hub_model_id: str,
    gpu_type: GPUType = GPUType.NV_A10G,
    model_len: Optional[int] = None,
) -> int:
    """
    Recommend the number of GPUs based on the model and GPU type.

    Args:
        hub_model_id (str): The model identifier.
        gpu_type (GPUType): The GPU type.
        model_len (Optional[int]): The sequence length of the model (optional).

    Returns:
        int: The recommended GPU count.

    Raises:
        RuntimeError: If more than 8 GPUs are recommended.
    """
    attention_head_count = _get_attention_head_count(hub_model_id)
    sequence_length = model_len or _get_max_position_embeddings(hub_model_id)
    safetensors_size = _calculate_safetensors_size(hub_model_id)

    recommended_gpu_memory = (
        attention_head_count * sequence_length * sequence_length * 2 / 1024**3
    ) + (safetensors_size / 10**9)

    recommended_gpu_count = math.ceil(recommended_gpu_memory / gpu_type.memory_gb)

    if recommended_gpu_count > 8:
        raise RuntimeError(
            f"More than 8 GPUs needed for GPU type {gpu_type.__repr__()}"
        )

    return recommended_gpu_count


def recommend_max_model_len(
    hub_model_id: str,
    gpu_count: int,
    gpu_type: GPUType = GPUType.NV_A10G,
) -> int:
    """
    Recommend the maximum model sequence length based on the available GPU count.

    Args:
        hub_model_id (str): The model identifier.
        gpu_count (int): The available GPU count.
        gpu_type (GPUType): The GPU type.

    Returns:
        int: The recommended maximum model sequence length.
    """
    max_model_len = _get_max_position_embeddings(hub_model_id)
    max_gpu_count = recommend_gpu_count(
        hub_model_id,
        gpu_type=gpu_type,
        model_len=max_model_len,
    )

    while max_gpu_count > gpu_count:
        max_model_len = int(max_model_len / 2)
        max_gpu_count = recommend_gpu_count(
            hub_model_id,
            gpu_type=gpu_type,
            model_len=max_model_len,
        )

    return max_model_len
