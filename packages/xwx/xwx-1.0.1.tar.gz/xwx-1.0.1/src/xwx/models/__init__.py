from transformers import AutoConfig, AutoModel, AutoModelForMaskedLM, AutoModelForSequenceClassification

from .bert.modeling_bert import BertModel, BertForMaskedLM, BertForSequenceClassification
from .bert.configuration_bert import BertConfig

AutoConfig.register('xwx/bert', BertConfig)
AutoModel.register(BertConfig, BertModel, exist_ok=True)
AutoModelForMaskedLM.register(BertConfig, BertForMaskedLM, exist_ok=True)
AutoModelForSequenceClassification.register(BertConfig, BertForSequenceClassification, exist_ok=True)