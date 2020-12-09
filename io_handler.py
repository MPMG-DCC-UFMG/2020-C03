import json
import numpy as np

# Process the JSON input file
def get_input (file):
    """
    file: path to the formated json input file

    return:
        query: list of locations(dict objects), only locations with fields 'addr'(address) or 'coord'(coordinate) are keeped
    """
    query = []
    with open(file) as json_file:
        data = json.load(json_file)
        for p in data['input']:
            if 'addr' in p.keys() or 'coord' in p.keys():
                query.append(p)
    return query

def write_final_log (results_dict, out_file):
    """
    results_dict: dict object containing the model predictions and informations of respective locations
    out_file: path of the output file
    """
    data = {}
    data ['output'] = []
    classes = ['apartment', 'house', 'school', 'parking_lot', 'hospital', 'religious', 'industrial', 'store', 'vacant_lot']

    for key, item in results_dict.items():
        i = item['softmax']
        if len(i) != 0:
            i_array = np.array(i)
            indices = i_array.argsort()[-3:][::-1]
            data['output'].append({item['id_type'] : item['repr'], 'id':item['id'],
                        'class' : classes[indices[0]], 'score': str(round(i[indices[0]],10)),
                        'top-3': [{'class' : classes[indices[0]], 'score': str(round(i[indices[0]],10))},
                                 {'class' : classes[indices[1]], 'score': str(round(i[indices[1]],10))},
                                 {'class' : classes[indices[2]], 'score': str(round(i[indices[2]],10))}]})
            data['output'][-1]['coord'] = item['coord']
        else:
            data['output'].append({item['id_type'] : item['repr'], 'error': 'Coundn\'t download any image for location.'})

    with open (out_file, 'w') as outfile:
        json.dump(data, outfile, indent = 4, separators = (',', ':'))
