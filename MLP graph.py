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
from tensorflow.keras.layers import Dense




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



# 데이터를 학습 및 테스트 셋으로 분할

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#X_train = X_train * 10
#X_test = X_test * 10

print("Data type of y_train:", y_train.dtype)
print("Data type of y_test:", y_test.dtype)
y_train = y_train.astype(np.float32)
y_test = y_test.astype(np.float32)
print("Data type of y_train:", y_train.dtype)
print("Data type of y_test:", y_test.dtype)

# 모델 초기화
model = Sequential()

# 입력층 (16개의 입력 뉴런)
model.add(Dense(32, input_dim=X.shape[1], activation='relu'))  # 여기서는 예시로 32개의 뉴런을 사용

# 은닉층 추가 (예: 2개의 은닉층)
model.add(Dense(64, activation='tanh'))
model.add(Dense(32, activation='tanh'))
model.add(Dense(16, activation='tanh'))

# 출력층 (로지스틱스, 즉 시그모이드 활성화 함수 사용)
model.add(Dense(1, activation='sigmoid'))

# 모델 컴파일 (이진 분류 문제이므로 binary_crossentropy 사용)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', 'mae'])

# 모델 구조 출력
model.summary()

# 모델 훈련 전 시간 저장
start_time = time.time()
# MLP 모델 생성 및 학습

history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test,y_test), verbose = 1)

# 모델 훈련 후 시간 저장
end_time = time.time()

# 훈련에 소요된 시간 계산
elapsed_time = end_time - start_time

''' 
weights_1 = model.layers[0].get_weights()
print(weights_1)
weights_2 = model.layers[1].get_weights()
print(weights_2)
weights_3 = model.layers[2].get_weights()
print(weights_3)
'''
# 첫번째 레이어의 가중치 및 편향
first_layer_weights, first_layer_biases = model.layers[0].get_weights()
#print("\nFirst Layer Biases:")
#print(first_layer_biases)
'''
# 마지막 레이어의 가중치 및 편향
#last_layer_weights, last_layer_biases = model.layers[-1].get_weights()
#print("\nLast Layer Weights:")
print(last_layer_weights)
print("\nLast Layer Biases:")
print(last_layer_biases)
'''

# 첫번째 레이어의 가중치 값에서 가장 큰 값을 갖는 인덱스를 찾습니다.
index_max_weight = np.argmax(first_layer_weights)

# 첫번째 레이어의 가중치 값을 정렬한 후 두 번째로 큰 값을 갖는 인덱스를 찾습니다.
sorted_weights = np.argsort(first_layer_weights.ravel())
index_second_max_weight = sorted_weights[-2]

print(f"특성 index with maximum weight: {index_max_weight}")
print(f"특성 index with second maximum weight: {index_second_max_weight}")





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
print(f"Batch size used: 16")