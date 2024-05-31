#!/bin/bash
#SBATCH --job-name=hctsa-process-patients
#SBATCH --output=/project/cama/hctsa/logs/patient_%A_%a.out
#SBATCH --error=/project/cama/hctsa/logs/patient_%A_%a.err
#SBATCH --array=1-100  # Adjust based on the number of entries in your mapping file
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --partition=standard

# Load Python module
module load python/3.8

# Path to the configuration and mapping file
CONFIG_PATH="/project/cama/hctsa/config.json"
MAPPING_FILE="/project/cama/hctsa/mapping.csv"

# Get the patient ID associated with the current SLURM_ARRAY_TASK_ID
PATIENT_ID=$(awk -v id=$SLURM_ARRAY_TASK_ID 'BEGIN {FS=","} NR==id+1 {print $2}' $MAPPING_FILE)

# Directory for data (assuming data directory path might be different or set here)
DATA_DIR="/project/cama/hctsa/data"

# Execute the Python script
python /project/cama/hctsa/process_patient.py --patient_id $PATIENT_ID --config_path $CONFIG_PATH --interval_length 120

echo "Processed patient data for patient ID: $PATIENT_ID"
