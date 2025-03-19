# -*- coding: utf-8 -*-

from transformers import AutoConfig, AutoModel, AutoModelForCausalLM

from rwkvfla.models.transformer.configuration_transformer import TransformerConfig
from rwkvfla.models.transformer.modeling_transformer import (
    TransformerForCausalLM, TransformerModel)

AutoConfig.register(TransformerConfig.model_type, TransformerConfig)
AutoModel.register(TransformerConfig, TransformerModel)
AutoModelForCausalLM.register(TransformerConfig, TransformerForCausalLM)


__all__ = ['TransformerConfig', 'TransformerForCausalLM', 'TransformerModel']
