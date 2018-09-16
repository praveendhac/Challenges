#!/usr/bin/env python

import pytest
import logging

import inviteForFoodAndDrinks

def test_get_distance_same_srcdst():
  assert inviteForFoodAndDrinks.get_distance([53.339428, -6.257664],[53.339428, -6.257664]) == 0.0

def test_get_distance_same_gr100():
  assert inviteForFoodAndDrinks.get_distance([53.339428, -6.257664],[51.92893,-10.27699]) >= 100.0

def test_get_distance_same_lt100():
  assert inviteForFoodAndDrinks.get_distance([53.339428, -6.257664],[53.2451022,-6.238335]) <= 100.0

def test_get_distance_same_invalid_coordinates1():
  assert inviteForFoodAndDrinks.get_distance([91, -6.257664],[53.2451022,-6.238335]) > 4000.0

def test_validate_user_id_with_int():
  assert inviteForFoodAndDrinks.validate_user_id(1) == True

def test_validate_user_id_with_str1():
  assert inviteForFoodAndDrinks.validate_user_id("1") == True

def test_validate_user_id_with_str2():
  assert inviteForFoodAndDrinks.validate_user_id("aa") == False

def test_validate_user_id_with_float():
  assert inviteForFoodAndDrinks.validate_user_id("1.0") == False

def test_str2json_invalidjson1(caplog):
  caplog.clear()
  inviteForFoodAndDrinks.str2json("----")
  assert "No JSON object" in caplog.text

def test_str2json_invalidjson2(caplog):
  caplog.clear()
  invalid_json_str = """{"m":}"""
  inviteForFoodAndDrinks.str2json(invalid_json_str)
  assert "No JSON object" in caplog.text

def test_validate_coordinates_invalid_lat(caplog):
  caplog.clear()
  inviteForFoodAndDrinks.validate_coordinates([91,-6])
  assert "Invalid Latitude" in caplog.text

def test_validate_coordinates_invalid_long(caplog):
  caplog.clear()
  inviteForFoodAndDrinks.validate_coordinates([80,200])
  assert "Invalid Longitude" in caplog.text
