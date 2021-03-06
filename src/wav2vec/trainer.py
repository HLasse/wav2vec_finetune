"""Subclassed Huggingface Trainer to allow for class weights to handle unbalanced groups"""


from torch import nn
from transformers import Trainer


class TrainerWithWeights(Trainer):
    def __init__(self, *args, class_loss_weights, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_loss_weights = class_loss_weights

    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.get("labels")
        # forward pass
        ### something weird happens during one evaluation pass 
        outputs = model(**inputs)
        logits = outputs.get("logits")
        # compute custom weighted loss
        loss_fct = nn.CrossEntropyLoss(weight=self.class_loss_weights)
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss
