import numpy as np
import pandas as pd
from collections import OrderedDict
import argparse


def getTruthDict(fr_truth):
    dict = {}
    for line in fr_truth:
        lines = line.split('\t')
        user = lines[0];
        movie = lines[1];
        rating = lines[2].replace('\n', '');

        if user in dict:
            dict[user][movie]=rating
        else:
            dict[user]={}
            dict[user][movie]=rating

    return dict

def getPredictionDict(fr_prediction):
    dict = {}
    for line in fr_prediction:
        lines = line.split('\t')
        user = lines[0].replace("'",'')
        movie = lines[1].replace("'",'')
        rating = lines[2].replace('\n','')

        if user in dict:
            dict[user][movie] = rating
        else:
            dict[user] = {}
            dict[user][movie] = rating

    return dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=''' Get Precision and Recall Scores''')

    parser.add_argument('--truth', type=str, dest='truth_file', default='data/kgRec/recommend_truth.txt')
    parser.add_argument('--predictions', type=str, dest='prediction_file', default='cli/inferred-predicates/RECOMMEND.txt')

    parsed_args = parser.parse_args()

    prediction_file = parsed_args.prediction_file
    truth_file = parsed_args.truth_file

    fr_prediction = open(prediction_file, 'r')
    fr_truth = open(truth_file, 'r')

    truth_dict = getTruthDict(fr_truth)
    prediction_dict = getPredictionDict(fr_prediction)

    precisionFinal1 = 0.0
    c1 =0
    precisionFinal3 = 0.0
    c3=0
    precisionFinal5 = 0.0
    c5=0
    mrr3 = 0.0
    mrr5 = 0.0
    cMRR3 = 0.0
    cMRR5 = 0.0
    MRR = 0.0
    cMRR = 0.0

    for user in prediction_dict:

        relevant_dict = OrderedDict(sorted(truth_dict[user].items(), key=lambda x: x[1], reverse = True))
        recommend_dict = OrderedDict(sorted(prediction_dict[user].items(), key=lambda x: x[1], reverse = True))

        precision1 = 0.0
        precision3 = 0.0
        precision5 = 0.0
        m3=0.0
        m5=0.0
        cm3=0.0
        cm5=0.0
        cmrr =0.0
        mrr=0

        relevant_list = list(relevant_dict.keys())

        recommend_list = list(recommend_dict.keys())
        l1 = relevant_list[0]
        if l1 == recommend_list[0]:
            precision1 = precision1 + 1
        c1= c1+1
        l3 = []
        if len(relevant_list)>=3:
            l3 = relevant_list[0:3]
            for i in range(0, 3):
                m = recommend_list[i]
                if m in l3:
                    precision3 = precision3+1

                if m==l3[i]:
                    if m3==0.0:
                        m3 = m3+(1/(i+1))
                    cm3 = cm3 + (1 / (i + 1))
            c3=c3+1


        l5 = []
        if len(relevant_list) >=5:
            l5 = relevant_list[0:5]
            for i in range(0, 5):
                m = recommend_list[i]
                if m in l5:
                    precision5 = precision5+1

                if m==l5[i]:
                    if m5==0.0:
                        m5 = m5+(1/(i+1))
                    cm5 = cm5 + (1 / (i + 1))
            c5=c5+1

        l = len(relevant_list)

        for i in range(0, l):
            m = recommend_list[i];
            if m == relevant_list[i]:
                cmrr = cmrr + (1/(i+1))
                if mrr == 0.0:
                    mrr = mrr + (1/(i+1))

        precisionFinal1 = precisionFinal1 + precision1
        p3 = float(precision3 / 3)
        precisionFinal3 = precisionFinal3 + p3
        p5 = float(precision5/5)
        precisionFinal5 = precisionFinal5 + p5
        mrr3 = mrr3 + m3
        mrr5 = mrr5 + m5
        cMRR3 = cMRR3 + cm3
        cMRR5 = cMRR5 + cm5
        MRR = MRR + mrr
        cMRR = cMRR + cmrr


    precisionFinal1 = precisionFinal1/c1
    precisionFinal3 = precisionFinal3/c3
    precisionFinal5 = precisionFinal5/c5
    mrr3 = mrr3/c3
    mrr5 = mrr5/c5
    cMRR3 = cMRR3/c3
    cMRR5 = cMRR5/c5
    length = len(prediction_dict)
    MRR = MRR/length
    cMRR = cMRR/length


    print("precision@1 :", precisionFinal1, c1)
    print("precision@3 :", precisionFinal3, c3)
    print("precision@5 :", precisionFinal5, c5)
    print("MRR@3 :", mrr3)
    print("MRR@5 :", mrr5)
    print("Corrected MRR@3 :", mrr3)
    print("Corrected MRR@5 :", mrr5)
    print("MRR :", MRR)
    print("Corrected MRR :", cMRR)



    fr_prediction.close()
    fr_truth.close()