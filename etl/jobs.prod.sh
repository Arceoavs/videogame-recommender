#!/bin/sh

sh jobs/setup.sh
sh jobs/load_csv_files.sh
sh jobs/integrate_data.sh
sh jobs/prepare_presentation.sh