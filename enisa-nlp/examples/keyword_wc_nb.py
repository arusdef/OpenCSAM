from pathlib import Path
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
import numpy as np

from keywords import *


path = Path.cwd() / "../../pdf-reports/"
df = read_plaintext_with_keywords(path)
df = add_chapter_fields(df)

print(df['num_keywords'].value_counts())
df_keywords = df[df.num_keywords > 0]

mlb = MultiLabelBinarizer()
mlb.fit(df_keywords.keywords)
print(len(mlb.classes_))
print(mlb.classes_)

y = mlb.transform(df_keywords.keywords)
print(y.shape)

cv = CountVectorizer(ngram_range=(1, 2), preprocessor=preproc, stop_words='english')
cv1 = CountVectorizer(ngram_range=(1, 1), preprocessor=preproc, stop_words='english')
cv2 = CountVectorizer(ngram_range=(2, 2), preprocessor=preproc, stop_words='english')

#X = cv.fit_transform(df_keywords['text'])
#X1 = cv1.fit_transform(df_keywords['text'])
#X2 = cv2.fit_transform(df_keywords['text'])
X = cv.fit_transform(df_keywords['all_chapters'])
X1 = cv1.fit_transform(df_keywords['all_chapters'])
X2 = cv2.fit_transform(df_keywords['all_chapters'])

print(X.shape)
print(X1.shape)
print(X2.shape)

# Build a model for each keyword
for idx, keyword in enumerate(mlb.classes_):
    label = y[:, idx]
    # Make sure there are at least 4 (2) positive labels for the training (test) set.
    if np.sum(label) <= 6:
        continue
    print('-' * 80)
    print("Keyword: " + keyword)
    print('-' * 80)

    # Split the dataset into training and test set while preserving the proportion of labels.
    X_train, X_test, y_train, y_test = train_test_split(X, label, test_size=0.33, random_state=42, stratify=label)
    #X_train, X_test, y_train, y_test = train_test_split(X1, label, test_size=0.33, random_state=42, stratify=label)
    #X_train, X_test, y_train, y_test = train_test_split(X2, label, test_size=0.33, random_state=42, stratify=label)
    print("Number of positive labels in the train (test) set: {} ({})".format(np.sum(y_train), np.sum(y_test)))

    # Train a model.
    clf = MultinomialNB().fit(X_train, y_train)

    # Print the performance metrics on the training set.
    y_pred = clf.predict(X_train)
    y_prob = clf.predict_proba(X_train)[:, 1]
    print("Accuracy on the train set: {:.3f}".format(np.mean(y_pred == y_train)))
    print("Area under the ROC curve: {:.3f}".format(roc_auc_score(y_train, y_prob)))
    print("F1 score: {:.3f}".format(f1_score(y_train, y_pred)))
    print(confusion_matrix(y_train, y_pred))

    # Print the performance metrics on the test set.
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]
    print("Accuracy on the test set: {:.3f}".format(np.mean(y_pred == y_test)))
    print("Area under the ROC curve: {:.3f}".format(roc_auc_score(y_test, y_prob)))
    print("F1 score: {:.3f}".format(f1_score(y_test, y_pred)))
    print(confusion_matrix(y_test, y_pred))