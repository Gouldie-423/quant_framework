import config
import DB_control
import LiveAlgorithimsV1 as LV
import algorithims
import pandas as pd
import numpy as np
import openpyxl
import csv
from datetime import timedelta,datetime
import datetime as dt

def start():
	DB_control.production_refresh_SP500()
	LV.v1()

start()


