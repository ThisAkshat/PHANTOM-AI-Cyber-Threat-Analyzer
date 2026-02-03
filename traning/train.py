import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/phishing.csv")

label_encoder = LabelEncoder()
df["label"] = label_encoder.fit_transform(df["label"])

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

class PhishingDataset(Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(texts.tolist(), truncation=True, padding=True, max_length=64)
        self.labels = labels.tolist()

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

dataset = PhishingDataset(df["text"], df["label"])
loader = DataLoader(dataset, batch_size=4, shuffle=True)

model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

model.train()

for epoch in range(2):
    for batch in loader:
        optimizer.zero_grad()
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
    print("Epoch", epoch, "done")

model.save_pretrained("model")
tokenizer.save_pretrained("model")
print("Model saved")
