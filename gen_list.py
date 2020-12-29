import argparse
import os

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Generate file list")
    parser.add_argument("--input", "-i", default="images/")
    parser.add_argument("--output", "-o", default="filelist.txt")
    parser.add_argument("--clist", default="list/clist.csv")
    args = parser.parse_args()

    clist = pd.read_csv(args.clist)
    labels = dict(zip(list(clist["id"]), list(clist["label"])))

    paths = []
    for imgfile in os.listdir(args.input):
        path = os.path.join(args.input, imgfile)
        if not os.path.exists(path):
            continue

        c_id, _ = imgfile.split("_")

        row = {"path": path, "label": labels[c_id]}
        paths.append(row)

    pd.DataFrame(paths).to_csv(
        args.output, index=False, columns=["path", "label"], header=False, sep=" "
    )


if __name__ == "__main__":
    main()
