# Imports
from transformers import BertTokenizer, BertModel, BertForSequenceClassification
import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import numpy as np


# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)


class TextDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels
       
    def __len__(self):
        return len(self.texts)
   
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
       
        encoding = tokenizer(text, return_tensors='pt', padding='max_length',
                           truncation=True, max_length=512)
       
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }


# Load and process data
# Folders
import os
ROOT: str = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")	# Root folder (where the config.py file is located)
DATASET: str = f"{ROOT}/../AI_Human.csv"
df = pd.read_csv(DATASET)  # Replace with your CSV file path
df = df[:10]
texts = df['text'].values
labels = df['generated'].values  # Assuming binary labels 0/1


# Split data
train_texts, test_texts, train_labels, test_labels = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)


# Create datasets and dataloaders
train_dataset = TextDataset(train_texts, train_labels)
test_dataset = TextDataset(test_texts, test_labels)


train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=8)


# Training setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)


# Training loop
num_epochs = 3
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
   
    for batch in train_loader:
        optimizer.zero_grad()
       
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)
       
        outputs = model(input_ids=input_ids,
                       attention_mask=attention_mask,
                       labels=labels)
       
        loss = outputs.loss
        total_loss += loss.item()
       
        loss.backward()
        optimizer.step()
   
    print(f"Epoch {epoch+1}, Average loss: {total_loss/len(train_loader)}")


# Testing
model.eval()
correct = 0
total = 0


with torch.no_grad():
    for batch in test_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)
       
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits, dim=1)
       
        correct += (predictions == labels).sum().item()
        total += labels.size(0)


accuracy = correct / total
print(f"\nTest Accuracy: {accuracy:.4f}")
