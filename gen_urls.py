import argparse
import codecs
import pathlib

import pandas as pd
from tqdm import tqdm


def get_categories(all_list_file, category_list_file):
    all_list = pd.read_csv(all_list_file, header=None, delimiter="\t")
    all_list.columns = ["id", "name"]

    category_list = pd.read_csv(category_list_file, header=None, delimiter="\t")
    category_list.columns = ["name"]
    category_list = category_list.drop_duplicates()

    categories = pd.merge(all_list, category_list, on="name")

    label = pd.DataFrame(categories["name"].unique())
    label.columns = ["name"]
    label["label"] = label.index

    return pd.merge(categories, label, on="name")


def main():
    parser = argparse.ArgumentParser(description="Generate URL list")
    parser.add_argument(
        "--urls_file",
        default="list/fall11_urls.txt",
        type=pathlib.Path,
        help="input file path",
    )
    parser.add_argument("--words_file", default="list/words.txt", type=pathlib.Path)
    parser.add_argument(
        "--categories_file", default="list/ILSVRC2012_ClassList.txt", type=pathlib.Path
    )
    parser.add_argument("--image_dir", default="images/", type=pathlib.Path)
    parser.add_argument("--urllist_file", default="list/urllist.txt", type=pathlib.Path)
    parser.add_argument("--clist_file", default="list/clist.csv", type=pathlib.Path)
    parser.add_argument(
        "--urls_file_line", type=int, help="for fall11_urls.txt, 14197122"
    )
    args = parser.parse_args()

    # check files
    if not args.urls_file.exists():
        raise FileNotFoundError(args.urls_file)
    if not args.words_file.exists():
        raise FileNotFoundError(args.words_file)
    if not args.categories_file.exists():
        raise FileNotFoundError(args.categories_file)
    if args.urllist_file.exists():
        raise FileExistsError(args.urllist_file)
    if args.clist_file.exists():
        raise FileExistsError(args.clist_file)

    # create dir
    args.image_dir.mkdir(parents=True, exist_ok=True)

    # get categories
    df = get_categories(args.words_file, args.categories_file)
    c_ids = list(df["id"])

    # get urls
    pbar = tqdm(total=args.urls_file_line)
    urls = []
    with codecs.open(args.urls_file, "r", "utf-8", "ignore") as f:
        for line in f:
            pbar.update(1)

            fileid, fileurl, *tmp = line.strip().split("\t")
            c_id, _ = fileid.split("_")

            if c_id not in c_ids:
                continue

            row = {
                "name": args.image_dir / (fileid + ".jpg"),
                "url": '"{}"'.format(fileurl),
            }
            urls.append(row)
    pbar.close()

    # output categories
    df.to_csv(args.clist_file, index=False)

    # output urls
    pd.DataFrame(urls).to_csv(
        args.urllist_file, index=False, columns=["name", "url"], header=False, sep=" "
    )


if __name__ == "__main__":
    main()
