# 이미지 분석을 통한 식단 유사도 평가
한국식 식단 관리 프로그램에 사용될 식단 유사도 평가 모델입니다. 새롭게 입력된 식단 이미지와 유사한 식단 이미지들을 사용자의 과거 식단 이미지들로부터 추출하여 일관성 있는 식단 평가에 도움을 줄 수 있습니다.
## Overview
- **Description** : Custom Tensorflow 2 Object Detection API 와 Tessorflow hub의 image feature vector model를 활용하여 과거 식단 이미지 중 새롭게 입력한 식단과 동일한 식단의 이미지를 유사한 순으로 나열해주는 모델을 개발하였습니다.   
식단 이미지 데이터를 수집하기 위해, Web-Scraper을 만들어 Pinterest에서 한식 밥상 이미지를 스크래핑하였고, 스크래핑한 이미지들을 바탕으로 Tensorflow 2 Object Detection API를 Retrain하였습니다.   
Tensorflow hub에서 image feature vector model를 불러와 식단 이미지들 간의 Cosine similarity를 분석하는 함수를 만들었습니다.   
한식 식단 이미지를 바탕으로 Custom한 Tensorflow 2 Object Detection API와 Cosine similarity 분석을 통해, 식단 이미지를 새롭게 입력하면 이미 입력된 이미지들 중 동일한 식단의 이미지들을 유사한 순으로 출력해줍니다.
- **Author** : 김홍엽
- **Date** : 20/09/01 ~ 20/09/05
## Dataset
- **식단 이미지** : Web-Scraper를 통해 Pinterest에서 식단 이미지 250개 스크래핑함.
## Tech
- **Python**
- **Selenium**
- **labelImg**
- **Tensorflow 2**
## Consisting of:
- [Pinterest Web Scraper](https://github.com/hngyb/Project/blob/master/Diet-image-analysis/Diet-image-Scraper.py)
- [Image similarity](https://github.com/hngyb/Project/blob/master/Diet-image-analysis/Image-similarity.ipynb)
- [Overall Colab](https://colab.research.google.com/drive/1rq6bCdX2KkgVKMmwrwdtnO52DTkD4TMD?usp=sharing)
## Contents
### 식단 유사성 판단 기준: 식단일 이루고 있는 음식들의 종류 또는 식품군
- 일반적인 식단표를 보면 1)음식 종류 2)총 칼로리 3)재료 4)영양소 등이 명시되어 있다.
- 음식의 종류를 알면 대략적인 칼로리와, 재료, 영양소 등은 파악이 가능하므로, 식단을 이루고 있는 음식들의 종류 또는 식품군을 파악하는 것이 식단 유사성을 판단하는데 가장 중요할 것으로 본다.
### 모델 설계
- 입력된 이미지의 식단을 이루고 있는 음식의 종류와 개수를 파악한 후,과거 식단 이미지들에서 같은 종류의 음식들을 포함하고 있는 것들을 추출하여 보여주는 모델을 설계한다.
- 이미지의 식단을 이루고 있는 음식의 종류와 개수를 파악하기 위해 “TensorFlow 2 Object Detection API”를 활용한다.
- 같은 종류의 음식들을 포함하고 있는 이미지들을 입력된 이미지와 더욱 유사한 순으로 나열하기 위해 TensorFlow hub의 “image feature vector model”를 활용하여 유사도를 분석한다.   
    ![Model Flow](https://user-images.githubusercontent.com/68726615/92483858-48106580-f224-11ea-8b33-c08e2441a8d5.png)   
### Training Data 준비
- Pinterest에서 한식 밥상 이미지 250개를 스크래핑하여 사용한다.
- labelImg를 이용하여 이미지들을 labeling한다.
- 한식 식단 이미지들에서 공통적으로 많이 보이는 음식 종류 "rice", "soup", "fish", "kimchi", "greens", "tofu", "egg", "curd", "beans", "meat", "fishcake" "squid", "potato", "pickles", "noodle", "pancake", "seaweed" 17가지를 class로 설정한다.
- Roboflow를 통해 Data augumentation을 진행하여 training data를 600장으로 만들고, custom data에 대한 TFRecords와 label_map을 생성한다.
- Train은 525장, Valid는 50장, Test는 23장으로 분류하였다.   
    ![labeling](https://user-images.githubusercontent.com/68726615/92483860-48106580-f224-11ea-9811-167a8b97eb33.png)   
    ![Roboflow](https://user-images.githubusercontent.com/68726615/92483848-45157500-f224-11ea-94cd-a0dafb16a7dd.png)
### 모델 검정
- 타겟 이미지 식단 분석 결과   
    ![](https://user-images.githubusercontent.com/68726615/92483845-43e44800-f224-11ea-9257-236408c26229.png)   
    - 탐지된 클래스로는 "greens", "greens", "greens", "fish", "kimchi", "rice", "soup" 으로 총 7가지 이다.
- 테스트 결과   
    - Roboflow의 Test 23장과 학습되지 않은 식단 이미지 101장을 더해 총 124의 이미지를 테스트하였다.
    ![](https://user-images.githubusercontent.com/68726615/92483832-40e95780-f224-11ea-93cd-db92dde524a6.png)   
    ![](https://user-images.githubusercontent.com/68726615/92483825-3e86fd80-f224-11ea-8928-0839066b25fa.png)   
    ![](https://user-images.githubusercontent.com/68726615/92483815-3c24a380-f224-11ea-91a8-a1734ab40450.png)   
    ![](https://user-images.githubusercontent.com/68726615/92483802-39c24980-f224-11ea-940b-bfb6e448d8d4.png)   
    - 총 124개의 이미지 중 4장의 이미지가 유사도가 높은 순으로 출력되었다.
    - 4장의 사진 모두 타겟 이미지와 동일한 음식의 종류와 개수를 가지고 있다.
- 한계점
    - 학습시킨 데이터가 충분히 많지 않았고, efficientdet 모델 중 가장 lightweight하고 작은 모델이 사용되었다.
    - TensorBoard를 확인해보면, Object detection 모델이 충분히 학습되지 않았음을 알 수 있다.
    - 라벨링한 class들이 구체적이지 않고, class 분류 기준이 모호하다.
### Conclusion
- 모델 검정 결과, 본 모델이 일관성 있는 식단 평가를 충분히 도울 수 있을 것이라 생각한다. 다만, 많은 양의 데이터를 충분히 학습시키고, 라벨링을 진행하기 전에 사진 자료를 분석하여 확실한 기준을 두고 class를 더욱 세분화하여 설정하는 것이 필요할 것 같다.
- 음식의 칼로리, 재료, 영양소 데이터를 더욱 추가하여 구현한다면 식단을 더욱 정확하고 구체적으로 분석할 수 있는 식단 관리 프로그램이 될 것이다.
## Reference
|#|title|source|note|
|:---:|:--------:|:---------:|:---------|
|1|[당근이 이미지 탐지기](https://medium.com/daangn/이미지-탐지기-쉽게-구현하기-abd967638c8e)|당근마켓|이미지 유사도 평가 참고|
|2|[How to Train YOLOv4 on a Custom Dataset](https://blog.roboflow.com/training-yolov4-on-a-custom-dataset/)|roboflow|Tensorflow 2 object detection train 참고|
