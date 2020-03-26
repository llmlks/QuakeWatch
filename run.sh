#!/bin/bash

gunicorn --workers=5 index:app