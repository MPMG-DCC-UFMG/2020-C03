import json
import numpy as np

# Process the JSON input file
def get_input (file, mode='complete'):
    """
    file: path to the formated json input file

    return:
        query: list of locations(dict objects), only locations with fields 'addr'(address) or 'coord'(coordinate) are keeped
    """
    assert mode in ['download', 'complete', 'classify'], 'The mode {} is not supported.'.format(mode)

    types = {0: 'none', 1: 'aerial', 2: 'ground', 3: 'both'}

    if mode in ['download', 'complete']:
        query = []
        with open(file) as json_file:
            data = json.load(json_file)
            for p in data['input']:
                if 'addr' in p.keys() or 'coord' in p.keys():
                    query.append(p)
    else:
        query = {}
        with open(file) as json_file:
            data = json.load(json_file)
            for i, p in enumerate(data['input']):
                if 'aerial' in p.keys() or 'street' in p.keys():
                    files = [p.get('aerial', ''), p.get('street', '')]
                    t = 0
                    if files[0]: t = 1
                    if files[1]: t |= 2
                    files.append(types[t])

                    query[i] = {'id_type': 'image files', 'repr': files[:2], 'files': files, 'id': p.get('id', str(i))}
    return query

def write_final_log (results_dict, out_file, add_field=['coord']):
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
            for field in add_field:
                data['output'][-1][field] = item[field]
        else:
            data['output'].append({item['id_type'] : item['repr'], 'error': 'Coundn\'t download any image for location.'})

    with open (out_file, 'w') as outfile:
        json.dump(data, outfile, indent = 4, separators = (',', ':'))
