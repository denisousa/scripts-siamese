import json
from files_operations import get_files_in_folder

rr_files_json = get_files_in_folder('../reciprocal_rank')
mean_status_rr = {"oracle_clones": 551,
                  'mean_queries': 0,
                  'mean_correct_predictions': 0,
                  'mean_wrong_predictions': 0,
                  'mean_hit_1': 0,
                  }

for rr_json in rr_files_json:
    with open(f'../reciprocal_rank/{rr_json}') as json_file:
        data = json.load(json_file)

        mean_status_rr['mean_queries'] += data['status']['siamese']['siamese_queries']
        mean_status_rr['mean_correct_predictions'] += data['status']['siamese']['siamese_correct_predictions']
        mean_status_rr['mean_wrong_predictions'] += data['status']['siamese']['siamese_wrong_predictions']
        mean_status_rr['mean_hit_1'] += data['status']['reciprocal_rank']['hit_1']

        number = data['status']['reciprocal_rank'][f'attempts_number']
        try:
            mean_status_rr[f'attempts_number_only_{number}'] += 1
        except:
            mean_status_rr[f'attempts_number_only_{number}'] = 1
        
mean_status_rr['mean_queries'] = int(mean_status_rr['mean_queries']/len(rr_files_json))
mean_status_rr['mean_correct_/predictions'] = int(mean_status_rr['mean_correct_predictions']/len(rr_files_json))
mean_status_rr['mean_wrong_predictions'] = int(mean_status_rr['mean_wrong_predictions']/len(rr_files_json))
mean_status_rr['mean_hit_1'] = int(mean_status_rr['mean_hit_1']/len(rr_files_json))

for i in range(20):
    if f'attempts_number_only_{i}' in mean_status_rr:
        mean_status_rr[f'attempts_number_only_{i}'] = int(mean_status_rr[f'attempts_number_only_{i}']/len(rr_files_json))

with open('mean_status_rr.json', 'w') as fp:
    json.dump(mean_status_rr, fp, indent=4)



