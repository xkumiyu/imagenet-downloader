import os
import io
import argparse

import requests
from PIL import Image
import pandas as pd
from tqdm import tqdm


def read_error_urls(error_urls_file):
    error_urls = pd.read_csv(error_urls_file, header=None, delimiter='\t')
    error_urls = error_urls.drop_duplicates()
    error_urls.columns = ['status_code', 'url']
    return list(error_urls['url'])


def download_image(fileurl, filepath, f, warn_print=False, timeout=1):
    try:
        res = requests.get(fileurl, allow_redirects=True, timeout=timeout)
    except requests.ConnectionError as e:
        if warn_print:
            print('[Warning]\n  ConnectionError: {}\n  URL: {}'.format(e, fileurl))
        return
    except requests.exceptions.ReadTimeout as e:
        if warn_print:
            print('[Warning]\n  ReadTimeout: {}\n  URL: {}'.format(e, fileurl))
        return
    except requests.exceptions.TooManyRedirects as e:
        if warn_print:
            print('[Warning]\n  TooManyRedirects: {}\n  URL: {}'.format(e, fileurl))
        return

    if res.status_code != 200:
        f.write('{}\t{}\n'.format(res.status_code, fileurl))
        if warn_print:
            print('[Warning]\n  HTTP status: {}\n  URL: {}'.format(
                res.status_code, fileurl))
        return

    if 'content-type' not in res.headers.keys():
        return

    content_type = res.headers['content-type']
    if 'image' not in content_type:
        if warn_print:
            print(
                '[Warning]\n  Content-Type: {}\n  URL: {}'.format(content_type, fileurl))
        return

    try:
        img = Image.open(io.BytesIO(res.content))
    except OSError as e:
        if warn_print:
            print('[Warning]\n  OSError: {}\n  URL: {}'.format(e, fileurl))
        return

    # img = img.resize()(256, 256))
    if img.mode != 'RBG':
        img = img.convert('RGB')
    img.save(filepath, 'JPEG')


def main():
    parser = argparse.ArgumentParser(description='Download ImageNet')
    parser.add_argument('--urls', '-i', default='list/ilsvrc2011_urls.csv')
    parser.add_argument('--error_urls', default='list/error_urls.txt')
    parser.add_argument('--out', '-o', default='image/')
    args = parser.parse_args()

    if not os.path.isdir(args.out):
        os.mkdir(args.out)

    if os.path.isfile(args.error_urls):
        error_urls = read_error_urls(args.error_urls)
    else:
        error_urls = []

    df = pd.read_csv(args.urls)
    with tqdm(total=len(df.index)) as pbar:
        with open(args.error_urls, 'a') as f:
            for _, row in df.iterrows():
                pbar.update(1)

                if row['url'] in error_urls:
                    continue

                dirpath = os.path.join(args.out, row['dirname'])
                if not os.path.isdir(dirpath):
                    os.mkdir(dirpath)

                filepath = os.path.join(dirpath, row['basename'])
                if os.path.isfile(filepath):
                    continue

                download_image(row['url'], filepath, f)


if __name__ == '__main__':
    main()
