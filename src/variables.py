import os,sys
import datetime

from src.data import *

BASE_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

G_TEXT_EXTENSION = ["Text file (*.txt *.tps *.topas", "Data files (*.dat *.yaml)"]
G_EXCEL_EXTENSION = ["Excel files (*.xsl *.xlms)"]

G_OUTDIR = os.path.join(BASE_PATH, 'prod', datetime.date.today().strftime('%y%m%d'))

G_NOZZLE_TYPE = None
G_TEMPLATE = []
G_PARAMETER = {}
G_COMPONENT = []
G_PATIENT = Patient()
G_PHASE = {}
G_FILTER = []