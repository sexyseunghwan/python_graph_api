from telegram.ext import *
import json
import requests
import logging
import logging.handlers
from datetime import datetime, timedelta
import calendar
import pytz
import time
from dateutil import parser
from dateutil.relativedelta import relativedelta
import os
import uuid
from dotenv import load_dotenv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from collections import OrderedDict
from matplotlib import font_manager, rc
import numpy as np
from flask import Flask, request, jsonify
