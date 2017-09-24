import os
import argparse

import pandas as pd
from PIL import Image
from tqdm import tqdm


def resize(infile, outfile, size):
    if os.path.exists(outfile):
        return

    try:
        img = Image.open(infile)
        img = img.resize(size)
        if img.mode != 'RBG':
            img = img.convert('RGB')
        img.save(outfile, 'JPEG')
    except OSError:
        return
    except ZeroDivisionError:
        return


def main():
    parser = argparse.ArgumentParser(description='Resize Image')
    parser.add_argument('--input', '-i', default='image/original/')
    parser.add_argument('--output', '-o', default='image/resized/')
    parser.add_argument('--size', '-s', default=(256, 256))
    args = parser.parse_args()

    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    # joblib.Parallel(n_jobs=-1)(
    #     joblib.delayed(resize)(imgfile, args) for imgfile in os.listdir(args.input)
    # )

    for imgfile in tqdm(os.listdir(args.input)):
        inpath = os.path.join(args.input, imgfile)
        outpath = os.path.join(args.output, imgfile)
        resize(inpath, outpath, args.size)


if __name__ == '__main__':
    main()
