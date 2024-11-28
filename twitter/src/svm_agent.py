
# Imports
from config import *
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter

class SVMAgent(Agent):
	class SVMBehaviour(CyclicBehaviour):

		async def on_start(self):
			self.vectorizer = TfidfVectorizer(max_features=SVMConfig.MAX_FEATURES)
			self.classifier = SVC(kernel=SVMConfig.KERNEL)
			self.label_mapping = {label: id for id, label in LabellerConfig.LABELS.items()}

		async def run(self):
			""" Main agent behaviour, receive database and train/predict using SVM """
			msg: Message = await self.receive(timeout=60)
			try:
				if msg:
					# Decode database
					debug(f"SVM: Receiving database...")
					database: dict[str, dict[str, str]] = json.loads(msg.body)
					
					# Prepare data for training
					texts = [tweet['content'] for tweet in database.values()]
					labels = [self.label_mapping[tweet['sentiment']] for tweet in database.values()]
					
					# Analysis of the distribution of the labels
					label_counts = Counter(labels)
					info(label_counts)
					# Balance the dataset
					rus = RandomUnderSampler(random_state=SVMConfig.RANDOM_STATE)
					texts_resampled, labels = rus.fit_resample(
						[[text] for text in texts], labels
					)
					texts = [text[0] for text in texts_resampled]
					# Analysis of the distribution of the labels (should be 50/50)
					label_counts = Counter(labels)
					info(label_counts)

					# Split into train/test sets
					X_train, X_test, y_train, y_test = train_test_split(
						texts, labels, test_size=SVMConfig.TEST_SIZE, random_state=SVMConfig.RANDOM_STATE,
						stratify=labels
					)
					#Analysis distribution(labels)
					label_counts = Counter(y_train)
					info(f"y_train: {label_counts}")
					label_counts = Counter(y_test)
					info(f"y_test: {label_counts}")
					
					# Transform text data
					X_train_vec = self.vectorizer.fit_transform(X_train)
					X_test_vec = self.vectorizer.transform(X_test)
					
					# Train the model
					debug(f"SVM: Started training with ({X_train_vec.shape}, {X_test_vec.shape})")
					self.classifier.fit(X_train_vec, y_train)
					
					# Evaluate
					accuracy = self.classifier.score(X_test_vec, y_test)
					info(f"SVM Model trained with accuracy: {accuracy:.3f}")

			except Exception as e:
				error(f"Error with request from {msg.sender}: {e}", exit=False)

	async def setup(self):
		""" Agent initialization """
		self.add_behaviour(self.SVMBehaviour())
		pass


