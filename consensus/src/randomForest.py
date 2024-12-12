import numpy as np 
import pandas as pd
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn

df=pd.read_csv('/kaggle/input/air-quality-and-pollution-assessment/updated_pollution_dataset.csv')

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

rf = RandomForestClassifier(random_state=1)
rf.fit(train_X, train_y)

pred_y = rf.predict(test_X)
print(classification_report(pred_y, test_y))
accuracy = accuracy_score(test_y, pred_y)
print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", classification_report(test_y, pred_y))