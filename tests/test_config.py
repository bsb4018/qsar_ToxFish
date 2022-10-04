import json
import logging
import os
import joblib
import pytest
from prediction_service.prediction import form_response, api_response
import prediction_service

input_data = {
    "incorrect_range": 
    {"CIC0": 7, 
    "SM1_Dz(Z)": 5, 
    "GATS1i": 9, 
    "NdsCH": 6, 
    "NdssC": 7, 
    "MLOGP": 79
    },

    "correct_range":
    {"CIC0": 3.22, 
    "SM1_Dz(Z)": 1.22, 
    "GATS1i": 0.88, 
    "NdsCH": 2, 
    "NdssC": 4, 
    "MLOGP": 3.22
    },

    "incorrect_col":
    {"CICs03": 5, 
    "SM1a_Dz(Z": 1, 
    "GAcTS1i": 0.5, 
    "NdsCHE": 10, 
    "NdsssC": 0.5, 
    "MLdOGP": 3
    }
}

TARGET_range = {
    "min": 0,
    "max": 10
}

def test_form_response_correct_range(data=input_data["correct_range"]):
    res = form_response(data)
    assert  TARGET_range["min"] <= res <= TARGET_range["max"]

def test_api_response_correct_range(data=input_data["correct_range"]):
    res = api_response(data)
    assert  TARGET_range["min"] <= float(res["response"]) <= TARGET_range["max"]

def test_form_response_incorrect_range(data=input_data["incorrect_range"]):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)

def test_api_response_incorrect_range(data=input_data["incorrect_range"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInRange().message

def test_api_response_incorrect_col(data=input_data["incorrect_col"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInCols().message