# ImageNet Downloader

Download from [ImageNet](http://image-net.org/) Image URLs

## Preparation

Install Python Packages:

```sh
pip install -r requirements.txt
```

Download image url list from <http://image-net.org/download-imageurls>.
For example, do the following:

```sh
wget http://image-net.org/imagenet_data/urls/imagenet_fall11_urls.tgz
```

**NOTE**: This URL is currently dead link. See also [#21](https://github.com/xkumiyu/imagenet-downloader/issues/21).

Download category list from <http://image-net.org/archive/words.txt>:

```sh
wget http://image-net.org/archive/words.txt
```

Select category and create list with one category written per line.
For example, for ILSVRC2012, create list based on <http://image-net.org/challenges/LSVRC/2012/browse-synsets>.
If you want to use the ILSVRC2012 list that we created, you can do the following:

```sh
wget https://git.io/vdUng -O urllist.txt
```

## Usage

1. Generate Download URL List

    ```sh
    python gen_urls.py
    ```

1. Download Image from URL List

    ```sh
    cat <generated urllist> | xargs -n 2 ./download.sh
    ```

    - It takes several hours to download about 1.3 million images, and their size is about 100 GB.
    - We recommend running it in the backend, ex. `nohup cat list/urllist.txt | xargs -n 2 ./download.sh > download.log 2> error.log &`

1. (optionally) Generate Image File List

    ```sh
    python gen_list.py
    ```
