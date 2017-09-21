import os
import argparse

import pandas as pd
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Download ImageNet')
    parser.add_argument('--input', '-i', default='image/original/')
    parser.add_argument('--output', '-o', default='image/resized/')
    parser.add_argument('--paths', '-p', default='image/filelist.txt')
    parser.add_argument('--size', '-s', default=(256, 256))
    parser.add_argument('--clist', default='list/clist.csv')
    args = parser.parse_args()

    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    clist = pd.read_csv(args.clist)
    labels = dict(zip(list(clist['id']), list(clist['label'])))

    for imgfile in os.listdir(args.input):
        inpath = os.path.join(args.input, imgfile)
        outpath = os.path.join(args.output, imgfile)

        try:
            img = Image.open(inpath)
            img = img.resize(args.size)
            if img.mode != 'RBG':
                img = img.convert('RGB')
            img.save(outpath, 'JPEG')
        except OSError as e:
            print(e)

    paths = []
    for imgfile in os.listdir(args.output):
        c_id, _ = imgfile.split('_')

        row = {'path': imgfile, 'label': labels[c_id]}
        paths.append(row)

    pd.DataFrame(paths).to_csv(
        args.paths, index=False, columns=['path', 'label'], header=False, sep=' ')


if __name__ == '__main__':
    main()
