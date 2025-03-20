from typing import Union
import torch
from torch import nn
from torch_model_hub.model import TextCNN, RNNAttention
from transformers import AutoModel, BertConfig, ErnieConfig, AutoTokenizer, AutoConfig
from transformers.utils.generic import PaddingStrategy


class TokenClassifier(nn.Module):

    def __init__(self, backbone, classifier):
        super().__init__()
        self.backbone = backbone
        self.classifier = classifier
        self.device = None

    def forward(self, tokenizies: dict):
        if self.device:
            return self._forward(tokenizies)
        else:    
            self.device = next(self.parameters()).device
            return self._forward(tokenizies)
    
    def _forward(self, tokenizies: dict):
        tokenizies = {k: v.to(self.device) for k, v in tokenizies.items()}
        outputs = self.backbone(**tokenizies, output_hidden_states=True)
        return self.classifier(outputs.last_hidden_state)  # 除去[cls]: outputs.last_hidden_state[:, 1:]

    def fit(self, inputs, labels: torch.Tensor):
        logits = self.forward(inputs)
        return nn.functional.cross_entropy(logits, labels), logits


class AutoCNNTokenClassifier(TokenClassifier):

    def __init__(self, pretrained_path, num_classes: int, config = None, **kwargs):
        config = config or AutoConfig.from_pretrained(pretrained_path)
        backbone = AutoModel.from_pretrained(pretrained_path)
        classifier = TextCNN(embed_dim=config.hidden_size, out_features=num_classes, **kwargs)
        for param in backbone.parameters():
            param.requires_grad_(False)
        super().__init__(backbone, classifier)

        
class BertCNNTokenClassifier(AutoCNNTokenClassifier):

    def __init__(self, pretrained_path, num_classes, **kwargs):
        config = BertConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, config, **kwargs)


class ErnieCNNTokenClassifier(AutoCNNTokenClassifier):

    def __init__(self, pretrained_path, num_classes, **kwargs):
        config = ErnieConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, config, **kwargs)


class AutoRNNAttentionTokenClassifier(TokenClassifier):

    def __init__(self, pretrained_path, num_classes, config = None, **kwargs):
        config = config or AutoConfig.from_pretrained(pretrained_path)
        backbone = AutoModel.from_pretrained(pretrained_path)
        classifier = RNNAttention(embed_dim=config.hidden_size, out_features=num_classes, **kwargs)
        for param in backbone.parameters():
            param.requires_grad_(False)
        super().__init__(backbone, classifier)


class BertRNNAttentionTokenClassifier(AutoRNNAttentionTokenClassifier):

    def __init__(self, pretrained_path, num_classes, **kwargs):
        config = BertConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, config, **kwargs)


class ErnieRNNAttentionTokenClassifier(AutoRNNAttentionTokenClassifier):

    def __init__(self, pretrained_path, num_classes: int, **kwargs):
        config = ErnieConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, config, **kwargs)


# class ModernBertCNNTokenClassifier(AutoCNNTokenClassifier):

#     def __init__(self, pretrained_path, num_classes,  max_length: int = 512, **kwargs):
#         config = ModernBertConfig.from_pretrained(pretrained_path)
#         super().__init__(pretrained_path, num_classes, max_length, config, **kwargs)


# class ModernBertRNNAttentionTokenClassifier(AutoRNNAttentionTokenClassifier):

#     def __init__(self, pretrained_path, num_classes,  max_length: int = 512, **kwargs):
#         config = ModernBertConfig.from_pretrained(pretrained_path)
#         super().__init__(pretrained_path, num_classes, max_length, config, **kwargs)


class TextClassifier(TokenClassifier):

    def __init__(self, pretrained_path, backbone, classifier, max_length: int = 512,   
			  	 padding: Union[bool, str, PaddingStrategy] = True, truncation=True, 
                 return_tensors='pt', return_token_type_ids=False, is_split_into_words=False):
        super().__init__(backbone, classifier)
        self.max_length = max_length
        self.padding = padding
        self.truncation = truncation
        self.return_tensors = return_tensors
        self.return_token_type_ids = return_token_type_ids
        self.is_split_into_words = is_split_into_words
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_path)

    def forward(self, texts):
        tokenizies = self.tokenizer.batch_encode_plus(texts,
                                                    max_length=self.max_length,
                                                    padding=self.padding,
                                                    truncation=self.truncation,
                                                    return_tensors=self.return_tensors,
                                                    return_token_type_ids=self.return_token_type_ids,
                                                    is_split_into_words=self.is_split_into_words)
        return super().forward(tokenizies)
    

class AutoCNNTextClassifier(TextClassifier):

    def __init__(self, pretrained_path, num_classes,  max_length: int = 512,   
			  	 padding: Union[bool, str, PaddingStrategy] = True, truncation=True, 
                 return_tensors='pt', return_token_type_ids=False, is_split_into_words=False, config = None, **kwargs):
        config = config or AutoConfig.from_pretrained(pretrained_path)
        backbone = AutoModel.from_pretrained(pretrained_path)
        classifier = TextCNN(embed_dim=config.hidden_size, out_features=num_classes, **kwargs)
        for param in backbone.parameters():
            param.requires_grad_(False)
        super().__init__(pretrained_path, backbone, classifier, max_length, padding, truncation, 
                         return_tensors, return_token_type_ids, is_split_into_words)
    

class BertCNNTextClassifier(AutoCNNTextClassifier):

    def __init__(self, pretrained_path, num_classes,  max_length: int = 512,   
			  	 padding: Union[bool, str, PaddingStrategy] = True,truncation=True, 
                 return_tensors='pt', return_token_type_ids=False, is_split_into_words=False, **kwargs):
        config = BertConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, max_length, padding, truncation, 
                         return_tensors, return_token_type_ids, is_split_into_words, config, **kwargs)


class ErnieCNNTextClassifier(AutoCNNTextClassifier):

    def __init__(self, pretrained_path, num_classes,  max_length: int = 512,   
			  	 padding: Union[bool, str, PaddingStrategy] = True, truncation=True, 
                 return_tensors='pt', return_token_type_ids=False, is_split_into_words=False, **kwargs):
        config = ErnieConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, max_length, padding, truncation, 
                         return_tensors, return_token_type_ids, is_split_into_words, config, **kwargs)


class AutoRNNAttentionTextClassifier(TextClassifier):

    def __init__(self, pretrained_path, num_classes,  max_length: int = 512,   
			  	 padding: Union[bool, str, PaddingStrategy] = True, truncation=True, 
                 return_tensors='pt', return_token_type_ids=False, is_split_into_words=False, config = None, **kwargs):
        config = config or AutoConfig.from_pretrained(pretrained_path)
        backbone = AutoModel.from_pretrained(pretrained_path)
        classifier = RNNAttention(embed_dim=config.hidden_size, out_features=num_classes, **kwargs)
        for param in backbone.parameters():
            param.requires_grad_(False)
        super().__init__(pretrained_path, backbone, classifier, max_length, padding, truncation, 
                         return_tensors, return_token_type_ids, is_split_into_words)


class BertRNNAttentionTextClassifier(AutoRNNAttentionTextClassifier):

    def __init__(self, pretrained_path, num_classes,  max_length: int = 512,   
			  	 padding: Union[bool, str, PaddingStrategy] = True, truncation=True, 
                 return_tensors='pt', return_token_type_ids=False, is_split_into_words=False, **kwargs):
        config = BertConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, max_length, padding, truncation,
                         return_tensors, return_token_type_ids, is_split_into_words, config, **kwargs)


class ErnieRNNAttentionTextClassifier(AutoRNNAttentionTextClassifier):

    def __init__(self, pretrained_path, num_classes,  max_length: int = 512,   
			  	 padding: Union[bool, str, PaddingStrategy] = True, truncation=True, 
                 return_tensors='pt', return_token_type_ids=False, is_split_into_words=False, **kwargs):
        config = ErnieConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, max_length, padding, truncation, 
                         return_tensors, return_token_type_ids, is_split_into_words, config, **kwargs)


# 需要 transformers>=4.48.3
# class ModernBertCNNTextClassifier(AutoCNNTextClassifier):

#     def __init__(self, pretrained_path, num_classes,  max_length: int = 512, **kwargs):
#         config = ModernBertConfig.from_pretrained(pretrained_path)
#         super().__init__(pretrained_path, num_classes, max_length, config, **kwargs)


# class ModernBertRNNAttentionTextClassifier(AutoRNNAttentionTextClassifier):

#     def __init__(self, pretrained_path, num_classes,  max_length: int = 512, **kwargs):
#         config = ModernBertConfig.from_pretrained(pretrained_path)
#         super().__init__(pretrained_path, num_classes, max_length, config, **kwargs)
