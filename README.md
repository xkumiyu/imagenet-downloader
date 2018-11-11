# ImageNet Downloader

Download from [ImageNet](http://image-net.org/) Image URLs

# Preparation

* Install Python Packages

```
$ pip install -r requirements.txt
```

* Download image url list from http://image-net.org/download-imageurls
  * ex. `$ wget http://image-net.org/imagenet_data/urls/imagenet_fall11_urls.tgz`
* Download category list from http://image-net.org/archive/words.txt
  * `$ wget http://image-net.org/archive/words.txt`
* Select category and create list with one category written per line
  * ex. for ILSVRC2012, create list based on http://image-net.org/challenges/LSVRC/2012/browse-synsets
  * https://git.io/vdUng

# Usage

1. Generate Download URL List

```
$ python gen_urls.py
```

2. Download Image from URL List

```
$ cat <generated urllist> | xargs -n 2 ./download.sh
```

* It takes several hours to download about 1.3 million images, and their size is about 100 GB.
* We recommend running it in the backend, ex. `$ nohup cat list/urllist.txt | xargs -n 2 ./download.sh > download.log 2> error.log &`

3. (optionally) Generate Image File List

```
$ python gen_list.py
```
