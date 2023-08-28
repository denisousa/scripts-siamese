import json
from files_operations import get_files_in_folder
import pandas as pd

def calculate_mean(params, mean_status_rr, rr_files_json):
    for param in params:
        mean_status_rr[param] = int(mean_status_rr[param]/len(rr_files_json))
    
    return mean_status_rr

def get_mean_status():
    rr_files_json = get_files_in_folder('../reciprocal_rank_origin')

    mean_status_rr = {
        'num_queries': 0, # 322
        'mean_correct_predictions': 0,
        'mean_exact_clones': 0,
        'mean_oracle_clones_inside_siamese': 0,
        'mean_siamese_clones_inside_oracle': 0,
        'mean_not_predict': 0,
        'mean_correct_predictions_percentage': 0,
        'mean_total_prediction_clones': 0,
        'mean_wrong_prediction_clones': 0,
        'mean_hit_1': 0,
        'mean_hit_2': 0,
        'mean_hit_3': 0,
    }

    parms = list(mean_status_rr.keys())

    for rr_json in rr_files_json:
        with open(f'../reciprocal_rank_origin/{rr_json}') as json_file:
            data = json.load(json_file)

            for key in parms:
                try:
                    mean_status_rr[key] += data['status'][key.replace('mean_','')]
                except:
                    pass

    parms = list(mean_status_rr.keys())
    mean_status_rr = calculate_mean(parms, mean_status_rr, rr_files_json)

    with open('mean_status_rr.json', 'w') as fp:
        json.dump(mean_status_rr, fp, indent=4)
    
    df = pd.DataFrame(columns=parms)
    df = pd.concat([df, pd.DataFrame([mean_status_rr])], ignore_index=True)
    return df

get_mean_status()