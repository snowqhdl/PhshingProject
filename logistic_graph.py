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
    X = np.load(os.path.join(DATA_DIRECTORY, 'training_data_features_100k.npy'), allow_pickle=True)
    y = np.load(os.path.join(DATA_DIRECTORY, 'training_data_labels_100k.npy'), allow_pickle=True)
    return X, y

X, y = load_data_from_path()

print("Shape of X:", X.shape)
print("\nShape of y:", y.shape)


#특성 추출로 변환된 데이터를 학습 데이터와 테스트 데이터로 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#print(f"Shape of {X}: {X_train.shape}")
#print(f"Content of {X}:\n{X_train}\n")

# NaN 값을 대체하기 위한 imputer 생성
#imputer = SimpleImputer(strategy='mean')  # 평균값으로 NaN 값을 대체
#X_train_imputed = imputer.fit_transform(X_train)
#X_test_imputed = imputer.transform(X_test)

# 모델 훈련 전 시간 저장
start_time = time.time()
# 로지스틱 회귀 모델 생성 및 학습
# solver로 'saga'를 사용하고 max_iter를 증가시켜 수렴까지의 반복 횟수를 늘립니다.
# verbose=True로 설정하면 학습 과정에서 손실의 변화를 출력할 수 있습니다.
logistic_model = LogisticRegression(solver='saga', max_iter=10000)   #verbose=True)
logistic_model.fit(X_train, y_train)

#clf = LogisticRegression().fit(X, y)

# 가중치 및 절편 출력
#print("Weights (coefficients):", clf.coef_)
#print("Intercept:", clf.intercept_)

# 모델 훈련 후 시간 저장
end_time = time.time()

# 훈련에 소요된 시간 계산
elapsed_time = end_time - start_time


# 예측
y_pred = logistic_model.predict(X_test)
confusion = confusion_matrix(y_test, y_pred)
# 성능 평가
accuracy = accuracy_score(y_test, y_pred)
print(f"Total training time: {elapsed_time:.2f} seconds.")
print("Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))


# 그래프 설정
plt.figure(figsize=(12, 8))

# 1. Confusion Matrix
plt.subplot(2, 2, 1)
sns.heatmap(confusion, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')


# ROC Curve 계산
y_test = y_test.astype(int)
fpr, tpr, thresholds = roc_curve(y_test, logistic_model.predict_proba(X_test)[:,1])
roc_auc = auc(fpr, tpr)


# 2. ROC Curve and AUC
plt.subplot(2, 2, 2)
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")


from sklearn.metrics import precision_recall_curve, average_precision_score

# Precision-Recall Curve 계산
precision, recall, _ = precision_recall_curve(y_test, logistic_model.predict_proba(X_test)[:,1])
average_precision = average_precision_score(y_test, logistic_model.predict_proba(X_test)[:,1])


# 3. Precision-Recall Curve
plt.subplot(2, 2, 3)
plt.plot(recall, precision, color='b', lw=2, label=f'Precision-Recall curve (AP = {average_precision:.2f})')
plt.fill_between(recall, precision, alpha=0.2, color='b')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="upper right")

from sklearn.model_selection import learning_curve

# 4. Learning Curve
plt.subplot(2, 2, 4)
train_sizes, train_scores, test_scores = learning_curve(logistic_model, X_train, y_train, cv=5)
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)
plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color="r")
plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1, color="g")
plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training score")
plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation score")
plt.title("Learning Curve")
plt.xlabel("Training examples")
plt.ylabel("Score")
plt.legend(loc="best")

# 그래프 표시
plt.tight_layout()
plt.show()