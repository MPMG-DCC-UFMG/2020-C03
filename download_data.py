import urllib, os
import urllib.request
import urllib.parse
import csv
import os, sys
from collections import OrderedDict

types = {0: 'none', 1: 'aerial', 2: 'ground', 3: 'both'}

def check_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

class Downloader(object):

    def __init__(self, key, output_path,
                base_street="https://maps.googleapis.com/maps/api/streetview?size=500x500&location=",
                base_aerial = "https://maps.googleapis.com/maps/api/staticmap?size=500x500&zoom=19&maptype=satellite&center=",
                base_metadata = "https://maps.googleapis.com/maps/api/streetview/metadata?size=500x500&location="):

        self.key = "&key=" + key
        self.base_street = base_street
        self.base_aerial = base_aerial
        self.base_metadata = base_metadata

        self.output_path = output_path
        self.outf_street = os.path.join(output_path, "street")
        self.outf_aerial = os.path.join(output_path,"aerial")
        self.outf_metadata = os.path.join(output_path,"metadata")

        check_dir(self.output_path)
        check_dir(self.outf_street)
        check_dir(self.outf_aerial)
        check_dir(self.outf_metadata)

    def prep_loc(self, loc, type):
        if type == 'addr':
            return urllib.parse.quote_plus(loc)
        elif type == 'coord':
            return urllib.parse.quote_plus(loc[0] + ',' + loc[1])

    def download_loc(self, loc, type):
        formated_loc = self.prep_loc(loc, type)
        meta_url = self.base_metadata + formated_loc + self.key

        try:
            f = urllib.request.urlopen(meta_url)
        except:
            return '', '', 0

        img_type = 3
        has_aerial = True
        has_street = True
        all_data = True
        t = f.read().decode('utf-8')
        a = eval(t)

        if not a['status'] == "OK":
            return '', '', 0

        basename = a['pano_id']
        file_img_street = os.path.join(self.outf_street, basename + ".jpg")
        file_img_aerial = os.path.join(self.outf_aerial, basename + ".png")
        file_meta = os.path.join(self.outf_metadata, basename + ".json")

        meta = open(file_meta, "wb")
        meta.write(t.encode('utf-8'))

        try:
            base = self.base_street + formated_loc + self.key
            urllib.request.urlretrieve(base, file_img_street)
        except:
            has_street = False
            all_data = False

        try:
            base = self.base_aerial + formated_loc + self.key
            urllib.request.urlretrieve(base, file_img_aerial)
        except:
            has_aerial = False
            all_data = False

        if not all_data:
            if has_street:
                img_type = 2
                if os.path.exists(file_img_aerial):
                    os.remove(file_img_aerial)
                file_img_aerial = ''

            elif has_aerial:
                img_type = 1
                if os.path.exists(file_img_street):
                    os.remove(file_img_street)
                file_img_street = ''
            else:
                img_type = 0
                if os.path.exists(file_img_street):
                    os.remove(file_img_street)
                file_img_street = ''
                if os.path.exists(file_img_aerial):
                    os.remove(file_img_aerial)
                file_img_aerial = ''

        return file_img_aerial, file_img_street, img_type

    def fecth_query(self, query):
        img_dict = OrderedDict()
        for i, q in enumerate(query):
            img_type = 'coord'
            i_type = ia_type = 0
            i_aerial, i_ground = '', ''
            ia_aerial, ia_ground = '', ''
            if 'coord' in q.keys():
                i_aerial, i_ground, i_type = self.download_loc(q['coord'], 'coord')
            if 'addr' in q.keys() and i_type != 3:
                ia_aerial, ia_ground, ia_type = self.download_loc(q['addr'], 'addr')
                img_type = 'addr'

            i_aerial = i_aerial if i_aerial != '' else ia_aerial
            i_ground = i_ground if i_ground != '' else ia_ground
            i_type |= ia_type

            img_dict[i] = {'id_type': img_type, 'repr': q[img_type], 'files':[i_aerial, i_ground, types[i_type]]}

        return img_dict

if __name__ == '__main__':
    dl = Downloader("key", "c03_data")
