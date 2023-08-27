import time
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import os
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import Callback




DATA_DIRECTORY = '/content'  # 여기에 데이터가 있는 경로를 지정하세요

def load_data_from_path():
    if not os.path.exists(DATA_DIRECTORY):
        raise ValueError("The specified path does not exist.")
    X = np.load(os.path.join(DATA_DIRECTORY, 'training_data_features_20k .npy'), allow_pickle=True)
    y = np.load(os.path.join(DATA_DIRECTORY, 'training_data_labels_20k.npy'), allow_pickle=True)
    return X, y

X, y = load_data_from_path()

print("Shape of X:", X.shape)
print("\nShape of y:", y.shape)


# 데이터를 학습 및 검증 데이터로 분할
train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]
X_train = X_train + 1
X_test = X_test + 1

sequence_length = X_train.shape[1]
print("Data type of y_train:", y_train.dtype)
print("Data type of y_test:", y_test.dtype)
y_train = y_train.astype(np.float32)
y_test = y_test.astype(np.float32)
print("Data type of y_train:", y_train.dtype)
print("Data type of y_test:", y_test.dtype)

# LSTM 모델 구축
model = Sequential()
model.add(Embedding(input_dim=3, output_dim=8, input_length=sequence_length, mask_zero=True))  # 임베딩 레이어 추가
model.add(LSTM(32, return_sequences=True))
model.add(LSTM(16))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', 'mae'])
# 모델 훈련 전 시간 저장
start_time = time.time()

# 모델 훈련
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test,y_test), verbose = 1)

# 모델 훈련 후 시간 저장
end_time = time.time()

# 훈련에 소요된 시간 계산
elapsed_time = end_time - start_time


# 손실과 MAE 플롯
plt.figure(figsize=(12, 10))

# 훈련 손실 그래프
plt.subplot(2, 2, 1)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()

# 훈련 MAE 그래프
plt.subplot(2, 2, 2)
plt.plot(history.history['mae'], label='Train MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.xlabel('Epoch')
plt.ylabel('MAE')
plt.title('Training and Validation MAE')
plt.legend()

# 훈련 Accuracy 그래프
plt.subplot(2, 2, 3)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()

# show plot
plt.tight_layout()
plt.show()

def plot_confusion_matrix(y_true, y_pred, class_names):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, xticklabels=class_names, yticklabels=class_names)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')
    plt.show()

# 모델로 예측
y_pred = model.predict(X_test)
y_pred_binary = np.round(y_pred).astype(int).flatten()

# confusion matrix 그리기
class_names = [0, 1]
plot_confusion_matrix(y_test.astype(int), y_pred_binary, class_names)



# 출력
print(f"Total training time: {elapsed_time:.2f} seconds.")
print(f"Batch size used: 32")