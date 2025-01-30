
# Imports
import numpy as np
import pandas as pd
import stouputils as stp
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from config import *
from src.print import *
from autogen_core import MessageContext, BaseAgent

import pandas as pd

import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import TensorDataset, DataLoader



class Bert(BaseAgent):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)
        self.msg: Message = Message(origin=self.__class__.__name__)
        # charger le modèle
        # Chargement du dataset
        df = pd.read_csv(DATASET)
        #trop long donc on test avec 10 lignes
        df = df.iloc[:20]

        from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer

        # Load the dataset (train, test)
        dataset = {
            "train": df[:int(len(df) * 0.8)],  # 80% for training
            "validation": df[int(len(df) * 0.8):],  # 20% for validation
        }

        # Load the pre-trained model
        model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased')

        # Define the training arguments
        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=64,
            evaluation_strategy='epoch',
            save_strategy='epoch',
            load_best_model_at_end=True,
        )

        # Create the Trainer object and train the model
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset['train'],
            eval_dataset=dataset['validation'],
        )

        trainer.train()
    

        # # Load the dataset
        # dataset = 

        # # Load the pre-trained model
        # model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased')

        # # Define the training arguments
        # training_args = TrainingArguments(
        #     output_dir='./results',
        #     evaluation_strategy='epoch',
        #     save_strategy='epoch',
        #     load_best_model_at_end=True,
        # )

        # # Create the Trainer object and train the model
        # trainer = Trainer(
        #     model=model,
        #     args=training_args,
        #     train_dataset=dataset['train'],
        #     eval_dataset=dataset['validation'],
        # )

        # trainer.train()


        # Tokenize the text
        train_encodings = tokenizer(train_texts, truncation=True, padding=True, return_tensors='pt')

        # Create the dataset
        class CustomDataset(torch.utils.data.Dataset):
            def __init__(self, encodings, labels):
                self.encodings = encodings
                self.labels = labels

            def __getitem__(self, idx):
                item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
                item['labels'] = torch.tensor(self.labels[idx])
                return item

            def __len__(self):
                return len(self.labels)

        train_dataset = CustomDataset(train_encodings, train_labels)

        # Set up the training arguments
        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=64,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
        )

        # Create the Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
        )

        # Train the model
        trainer.train()


    #     classes = {'Human': 0, 'AI': 1}
    #     df['generated'] = df['generated'].map(classes)
        
    #     X = df['text'].tolist()  # Supposons que la colonne contenant le texte s'appelle 'text'
    #     Y = df['generated'].values
        
    #     train_X, test_X, train_y, test_y = train_test_split(X, Y, train_size=0.8, test_size=0.2, random_state=1)
        
    #     # Tokenization
    #     debug("Salut moi c'est BOB")
    #     tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', num_labels=2)
    #     train_encodings = tokenizer(train_X, truncation=True, padding=True, max_length=512, return_tensors='pt')
    #     test_encodings = tokenizer(test_X, truncation=True, padding=True, max_length=512, return_tensors='pt')
    #     debug("Salut moi c'est encore BOB")
    #     train_labels = torch.tensor(train_y)
    #     test_labels = torch.tensor(test_y)
    #     debug("j'ai créé les tensors")
        
    #     # Création des DataLoader
    #     debug("coucou c'est encore moi BOB")
    #     train_dataset = TensorDataset(train_encodings['input_ids'], train_encodings['attention_mask'], train_labels)
    #     test_dataset = TensorDataset(test_encodings['input_ids'], test_encodings['attention_mask'], test_labels)
        
    #     train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    #     test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)
    #     debug("j'ai  créé les dataloader")
        
    #     # Chargement du modèle BERT
    #     self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
    #     self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=5e-5, eps=1e-8)
        
    #     # Entraînement du modèle
    #     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #     self.model.to(device)
    #     self.model.train()
        
    #     debug("Entraînement en cours...")
    #     epochs = 3
    #     for epoch in range(epochs):
    #         for batch in train_loader:
    #             input_ids, attention_mask, labels = [b.to(device) for b in batch]
    #             self.optimizer.zero_grad()
    #             print(f"input_ids: {input_ids.shape}")
    #             print(f"attention_mask: {attention_mask.shape}")
    #             print(f"labels: {labels.shape}")
    #             outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
    #             print(f"outputs.logits: {outputs.logits.shape}")
    #             loss = outputs.loss
    #             loss.backward()
    #             self.optimizer.step()
                
    #     debug("Entraînement terminé !")

    #     # Évaluation du modèle
    #     self.model.eval()
    #     all_preds, all_labels = [], []
    #     with torch.no_grad():
    #         for batch in test_loader:
    #             input_ids, attention_mask, labels = [b.to(device) for b in batch]
    #             outputs = self.model(input_ids, attention_mask=attention_mask)
    #             logits = outputs.logits
    #             predictions = torch.argmax(logits, dim=-1)
    #             all_preds.extend(predictions.cpu().numpy())
    #             all_labels.extend(labels.cpu().numpy())
        
    #     accuracy = accuracy_score(all_labels, all_preds)
    #     report = classification_report(all_labels, all_preds, target_names=['Human', 'AI'])
    #     debug(f'Précision du modèle : {accuracy:.4f}')
    #     debug(report)

    #     # Sauvegarde du modèle
    #     self.model.save_pretrained("bert_model")
    #     print("Modèle sauvegardé !")
    
    async def on_message_impl(self, message: Message, ctx: MessageContext) -> None:
        """ Receive a message and send 1 if content is generated by AI, else 0 """
        stp.info(f"BERT: Received message from {message.origin}")
        content: str = str(message.content)
        data: list|dict = json.loads(message.data)
        if data.get("request") == "majoritaire":
            question: str = "Can you simply answer 'Yes' or 'No' if the following sentence has been generated by an AI?"
            result = self.model(question=question, context=content)
            # Get the label result
            labels: dict[str, str] = {"yes": "1","no": "0"}
            msg = Message(labels[result['answer']])

        # Send back
        await self.send_message(msg, ctx.sender)


if __name__ == "__main__":
    bert = Bert()
    bert.run()


# Entrainement (à tester mais trop long)
