# ImageNet Downloader

Downloader from [ImageNet](http://image-net.org/) Image URLs

# Requirements

* Install Python Packages

```
$ pip install -r requirements.txt
```

* Download image url list from http://image-net.org/download-imageurls
* Download category list from http://image-net.org/archive/words.txt
* Select category and create list with one category written per line
  * e.g. for ILSVRC2012, create list based on http://image-net.org/challenges/LSVRC/2012/browse-synsets
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

3. Generate Image File List

```
$ python gen_list.py
```
