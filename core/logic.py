from utils.custom_logger import *
from core.beers_flat_manager import *
import os, time

custom_logger = CustomLogger()

"""
Main method that run logic
"""
def run_logic():
    beersFlatManager = BeersFlatManager()
    beersFlatManager.update_flat()
