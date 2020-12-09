import argparse
import io_handler as io
import torch
import sknet as net
import numpy as np
import os
from collections import OrderedDict
from download_data import Downloader
from scipy.special import softmax as softnorm

def main():
    parser = argparse.ArgumentParser(description='MP-C03 - Final Module')
    parser.add_argument('--google_maps_key', type=str, required=True,
                        help='API key for google maps. It is required to download aerial images.')
    parser.add_argument('--google_sview_key', type=str, required=True,
                        help='API key for google street view. It is required to download street-level images.')
    parser.add_argument('--input_file', type=str, required=True,
                        help='Path to JSON input file.')
    parser.add_argument('--output_path', type=str, required=True,
                        help='Path to save JSON output file and images downloaded.')
    parser.add_argument('--aerial_model', type=str, required=True,
                        help='Path to aerial network model file.')
    parser.add_argument('--ground_model', type=str, required=True,
                        help='Path to ground network model file.')
    parser.add_argument('--output_file', type=str, required=True,
                        help ='Name of the JSON output file.')

    # Parsing arguments
    args = parser.parse_args()
    google_maps_key = args.google_maps_key
    google_sview_key = args.google_sview_key
    input_file = args.input_file
    output_path = args.output_path
    aerial_model = args.aerial_model
    ground_model = args.ground_model
    out_file_name = args.output_file

    # Process the JSON input file, and get a list of adrresses to compute
    query = io.get_input(input_file)

    # Instantiate a Dowloader object and dowload the images present in the query
    dl = Downloader(google_maps_key, output_path)
    img_dict = dl.fetch_query(query)

    # Loop through the locations and classify them
    results_dict = OrderedDict()
    for key, infos in img_dict.items():
        softmax = []
        img_files = infos['files'] # List in the format [string: path to aerial img, string: path to street img, string: typeof imgs (i.e. none, aerial, ground, both)]
        if (img_files[2] == 'both'):
            a_model = torch.load(aerial_model)
            soft_a = net.infer(a_model, img_files[0])
            g_model = torch.load(ground_model)
            soft_b = net.infer(g_model, img_files[1])
            softmax = [np.prod(x) for x in zip(soft_a, soft_b)]
            softmax = softmax/np.sum(softmax)
        if (img_files[2] == 'aerial'):
            a_model = torch.load(aerial_model)
            softmax = net.infer(a_model, img_files[0])
        if (img_files[2] == 'ground'):
            g_model = torch.load(ground_model)
            softmax = net.infer(g_model, img_files[1])
        if (img_files[2] == 'none'):
            print ('Can not download any image for ' + str(infos['repr']) + ' using its ' + str(infos['id_type']) + '.')
            softmax = []

        results_dict[key] = {'id': infos['id'], 'id_type': infos['id_type'], 'repr': infos['repr'], 'softmax': softmax, 'coord':infos['coord']}

    # Write the output file
    io.write_final_log (results_dict, os.path.join(output_path, out_file_name))



if __name__ == '__main__':
    main()
