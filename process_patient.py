
import argparse
import json
from PatientData import PatientData

def load_config(path):
    """Load configuration from JSON file."""
    with open(path, 'r') as file:
        return json.load(file)

def main():
    parser = argparse.ArgumentParser(description="Process patient data")
    parser.add_argument('--patient_id', type=int, required=True, help="Patient ID")
    parser.add_argument('--config_path', type=str, required=True, help="Path to configuration JSON file")
    parser.add_argument('--interval_length', type=int, required=True, help="Interval length in seconds", default=5*60)
    args = parser.parse_args()

    config = load_config(args.config_path)
    patient = PatientData(args.patient_id, config, args.interval_length)
    patient.analyze_and_save()

if __name__ == '__main__':
    main()
