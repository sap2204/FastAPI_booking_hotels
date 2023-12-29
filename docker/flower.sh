#!/bin/bash

celery --app=app.tasks.celery_setup:celery flower