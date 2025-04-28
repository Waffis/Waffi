from flask import Flask, render_template, request, jsonify
import sqlite3
import db
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from fuzzywuzzy import process
import re
import os


def problems ():
    problems= db.borwes_db()
    for row in problems:
        respone = row
        