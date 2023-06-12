import numpy as np
import csv
import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from tensorflow import keras
input_csvlink = './dataset/sample.csv'
output_csvlink = './dataset/augmented_sample.csv'
savedmodel = './ML_optimized/tone_prediction.h5'


reconstructed_model = keras.models.load_model(savedmodel)


def read_csv(input, output):
    data_list = []
    with open(input, 'r') as input_file, open(output, 'a+', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        next(reader)
        for row in reader:
            data = np.reshape(row, (1, -1)).astype(float)
            predictions = reconstructed_model.predict(data)
            skin_tone = pred_tone(predictions[:, :3].argmax(axis=1))
            season = pred_season(predictions[:, 3:].argmax(axis=1))
            data_list.append(skin_tone)
            data_list.append(season)
            lis = list(row)
            lis.append(skin_tone)
            lis.append(season)
            writer.writerow(lis)


def pred_tone(index):
    if index == 0:
        return "white"
    elif index == 1:
        return "olive"
    elif index == 2:
        return "darkbrown"


def pred_season(index):

    if index == 0:
        return "summer"
    elif index == 1:
        return "winter"
    elif index == 2:
        return "autumn"
    elif index == 3:
        return "spring"


read_csv(input_csvlink, output_csvlink)

# data = [[255, 158, 114, 182, 141, 64, 244, 235, 208, 18, 38, 32]]
# predictions = reconstructed_model.predict(data)
# predictions = predictions*100
# Print the predictions
# print(predictions)
