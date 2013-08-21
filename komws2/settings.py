#!/usr/bin/env python
# coding: utf-8

import os.path
# import logging
# import sys

# Definicion de directorios
DIRNAME = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(DIRNAME, "templates")
STATIC_PATH = os.path.join(DIRNAME, "static")

# Definicion de cookies
COOKIE_SECRET = "FC+EWT0sRh+iDGsqD4xvcm6UkRUw4UuWvsKeq8x8aHk="
XSRF_COOKIES = False # Hay problemas con los procesos que se conecta por POST que no pertenecen al Frontal Web... hay que revisarlo

# Definicion del Login
LOGIN_URL = "/login"

# Definicion del debug mode
DEBUG = True 

# Logs
# logging.basicConfig(level=logging.DEBUG,
 #                   format='%(asctime)s - %(levelname)-8s - %(message)s',
  #                  datefmt='%d/%m/%Y %Hh%Mm%Ss')
# console = logging.StreamHandler(sys.stderr)
