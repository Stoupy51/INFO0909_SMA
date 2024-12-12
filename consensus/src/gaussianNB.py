import pandas as pd
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.naive_bayes import GaussianNB

from config import *
from src.print import *
from autogen_core import MessageContext, BaseAgent

class NBAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__("SimpleAgent")
        #chargement du dataset
        df=pd.read_csv(DATASET)
        air_quality_map = {
            'Hazardous' : 0,
            'Poor' : 1,
            'Moderate': 2,
            'Good' : 3
        }
        df['Air Quality'] = df['Air Quality'].map(air_quality_map)
        X = df.drop(columns = ['Air Quality'])
        Y = df['Air Quality']
        train_X, test_X, train_y, test_y = train_test_split(X, Y, train_size=0.8, test_size=0.2, random_state=1)
        self.model = GaussianNB()
        self.model.fit(train_X, train_y)

    async def on_message_impl(self, message: Message, ctx: MessageContext) -> None:
        print(f"NB: Received message: {message.content}")

# pred_y = nb.predict_proba(X)
# pred_y = nb.predict(test_X)
# print(classification_report(pred_y, test_y))
# accuracy = accuracy_score(test_y, pred_y)
# print(f"Accuracy: {accuracy:.2f}")
# print("\nClassification Report:\n", classification_report(test_y, pred_y))
