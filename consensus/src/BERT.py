
# Imports
from config import *
import stouputils as stp
import pandas as pd
import torch
import json
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, BatchEncoding
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from autogen_core import MessageContext, BaseAgent
import os
from src.reputation import Reputation

class TextDataset(Dataset):
    def __init__(self, encodings: BatchEncoding, labels: list):
        self.encodings: BatchEncoding = encodings
        self.labels: list = labels

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> dict:
        item: dict = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

class Bert(BaseAgent):

    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)
        self.msg: Message = Message(origin=self.__class__.__name__)
        self.model_path: str = f"{ROOT}/models/bert.pth"
        self.reputation: Reputation = Reputation()
        
        # Try to load existing model
        try:
            with stp.Muffle(mute_stderr=True):
                self.tokenizer: BertTokenizer = BertTokenizer.from_pretrained("bert-base-uncased", use_auth_token=False)
                self.model: BertForSequenceClassification = BertForSequenceClassification.from_pretrained(self.model_path)
                stp.info("Loaded existing model")
        except:
            stp.info("No existing model found, training new model...")
            with stp.Muffle(mute_stderr=True):
                # Chargement du dataset
                data: pd.DataFrame = pd.read_csv(DATASET)
                data["generated"] = data["generated"].astype(int)
                data = data.iloc[:1000] # Trop long donc on test avec moins de lignes

                # Séparer les données en train/test
                train_texts, val_texts, train_labels, val_labels = train_test_split(
                    data.iloc[:, 0].tolist(),
                    data.iloc[:, 1].tolist(),
                    test_size=0.2,
                    random_state=42
                )

                # Charger le tokenizer BERT
                self.tokenizer: BertTokenizer = BertTokenizer.from_pretrained("bert-base-uncased", use_auth_token=False)

                # Tokenization
                train_encodings: BatchEncoding = self.tokenizer(train_texts, truncation=True, padding=True, max_length=512)
                val_encodings: BatchEncoding = self.tokenizer(val_texts, truncation=True, padding=True, max_length=512)

                # Création des datasets
                train_dataset: TextDataset = TextDataset(train_encodings, train_labels)
                val_dataset: TextDataset = TextDataset(val_encodings, val_labels)

                self.model: BertForSequenceClassification = BertForSequenceClassification.from_pretrained(
                    "bert-base-uncased",
                    num_labels=len(set(data["generated"])),
                    use_auth_token=False
                )

            # Training
            os.environ["WANDB_DISABLED"] = "true"   # Désactiver le suivi des expériences
            training_args: TrainingArguments = TrainingArguments(
                output_dir="./results",
                eval_strategy="epoch",
                per_device_train_batch_size=8,
                per_device_eval_batch_size=8,
                num_train_epochs=3,
                save_strategy="epoch",
                save_total_limit=2,
                logging_dir="./logs",
                logging_strategy="steps",  # Log à intervalles réguliers
                logging_steps=10,  # Affiche une sortie toutes les 10 étapes
            )

            self.trainer: Trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=val_dataset,
            )

            self.trainer.train()

            results: dict = self.trainer.evaluate()
            stp.info(results)
            
            # Save the model
            self.model.save_pretrained(self.model_path)
            stp.info(f"Model saved to {self.model_path}")

        # Détecter si un GPU est disponible
        self.device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Charger le modèle sur l'appareil adéquat
        self.model.to(self.device)   # type: ignore
        
        # Initialize reputation with this data
        stp.info("Initializing BERT reputation...")
        for _, row in data.iterrows():
            text = row[0]
            true_class = "ai" if row[1] == 1 else "human"
            
            # Predict
            inputs: BatchEncoding = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            moved_inputs: dict[str, torch.Tensor] = {key: val.to(self.device) for key, val in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**moved_inputs)
            
            # Get prediction
            probabilities: torch.Tensor = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
            classes: list[str] = ["human", "ai"]
            class_probs = [(class_name, float(prob)) for class_name, prob in zip(classes, probabilities)]
            predicted_class, _ = max(class_probs, key=lambda x: x[1])
            
            # Update reputation
            self.reputation.update(predicted_class == true_class)
        
        stp.info(f"BERT initial reputation (beta): {self.reputation.get_beta()}")
    
    def predict(self, text: str) -> int:
        """ Predict if the text is generated by an AI """
        with stp.Muffle():
            # Tokenisation du texte
            inputs: BatchEncoding = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

            # Déplacer les entrées sur le même appareil que le modèle
            moved_inputs: dict[str, torch.Tensor] = {key: val.to(self.device) for key, val in inputs.items()}

            # Faire une prédiction
            with torch.no_grad():
                outputs: torch.Tensor = self.model(**moved_inputs)

            # Convertir la sortie en label prédictif
            logits: torch.Tensor = outputs.logits   # type: ignore
            predicted_class: int = int(torch.argmax(logits, dim=1).item())

            return int(predicted_class)

    def predict_borda(self, text: str) -> str:
        """ Predict probabilities and return Borda count string """
        with stp.Muffle():
            inputs: BatchEncoding = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            moved_inputs: dict[str, torch.Tensor] = {key: val.to(self.device) for key, val in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**moved_inputs)
            
            # Get probabilities using softmax
            probabilities: torch.Tensor = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
            
            # Create list of tuples (class_name, probability)
            classes: list[str] = ["human", "ai"]
            probas_tuple: list[tuple[str, float]] = [(class_name, float(prob)) for class_name, prob in zip(classes, probabilities)]
            
            # Sort by probability in descending order
            probas_tuple.sort(key=lambda x: x[1], reverse=True)
            
            # Build Borda count string
            to_return: str = ""
            nb_points: int = len(probas_tuple)
            for candidat, _ in probas_tuple:
                to_return += f"{candidat} {nb_points},"
                nb_points -= 1
                
            return to_return
    
    async def on_message_impl(self, message: Message, ctx: MessageContext) -> None:
        """ Receive a message and process using either majority vote or Borda count """
        stp.info(f"BERT: Received message from {message.origin}")
 
        content: str = str(message.content)
        data: dict = json.loads(message.data)
 
        if data.get("request") == "majoritaire":
            result = self.predict(content)
            self.msg.content = str(result)
            
        elif data.get("request") == "borda":
            self.msg.content = self.predict_borda(content)

        elif data.get("request") == "paxos":
            phase = data.get("phase")
            
            # Phase 1: Make a proposal with confidence
            if phase == "propose":
                # Use the model to predict
                with stp.Muffle():
                    inputs: BatchEncoding = self.tokenizer(content, return_tensors="pt", truncation=True, padding=True, max_length=512)
                    moved_inputs: dict[str, torch.Tensor] = {key: val.to(self.device) for key, val in inputs.items()}
                    
                    with torch.no_grad():
                        outputs = self.model(**moved_inputs)
                    
                    # Get probabilities using softmax
                    probabilities: torch.Tensor = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
                    
                    # Determine class with highest probability
                    classes: list[str] = ["human", "ai"]
                    class_probs = [(class_name, float(prob)) for class_name, prob in zip(classes, probabilities)]
                    predicted_class, confidence = max(class_probs, key=lambda x: x[1])
                    
                    # Send proposal with confidence
                    self.msg.content = json.dumps({
                        "class": predicted_class,
                        "confidence": confidence,
                        "beta": self.reputation.get_beta()
                    })
            
            # Phase 2: Vote for a candidate
            elif phase == "vote":
                # Get candidates and vote for the one with highest beta
                candidates = data.get("candidates", {})
                if candidates:
                    # Simple strategy: vote for highest beta candidate
                    best_candidate = max(candidates.items(), key=lambda x: x[1][1])[0]
                    self.msg.content = json.dumps({"voted_for": best_candidate})

        # Send back
        await self.send_message(self.msg, ctx.sender)    # type: ignore


