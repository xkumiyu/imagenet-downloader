import argparse
import pathlib

from PIL import Image
from tqdm import tqdm


def resize(infile, outfile, size):
    try:
        img = Image.open(infile)
        img = img.resize(size)
        if img.mode != "RBG":
            img = img.convert("RGB")
        img.save(outfile, "JPEG")
    except OSError:
        return
    except ZeroDivisionError:
        return


def main():
    parser = argparse.ArgumentParser(description="Image Converter")
    parser.add_argument("--input", "-i", default="images/original/", type=pathlib.Path)
    parser.add_argument("--output", "-o", default="images/resized/", type=pathlib.Path)
    parser.add_argument(
        "--min_size",
        help=(
            "resize side of min(H, W) to min_size, "
            "aspect ratio of another side is maintained."
        ),
    )
    parser.add_argument("--size")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    for imgfile in tqdm(args.input.glob(".")):
        inpath = args.input / imgfile
        outpath = args.output / imgfile
        if not outpath.exists:
            resize(inpath, outpath, args.size)


if __name__ == "__main__":
    main()
