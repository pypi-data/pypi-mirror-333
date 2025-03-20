import argparse
from cryocat import tiltstack


def main():
    parser = argparse.ArgumentParser(description="cryoCAT")

    # methods to call
    parser.add_argument("--dose_filter", action="store_true", help="Dose filter a tilt stack", required=False)
    parser.add_argument("--convert_motl", action="store_true", help="Convert motive list", required=False)

    # general arguments
    parser.add_argument("--input_file", action="store", dest="input_file", help="Input tilt series", required=False)
    parser.add_argument("--output_file", help="Path to the created output", required=False)
    parser.add_argument(
        "--pixel_size", action="store", dest="pixel_size", type=float, help="Pixel size in Angstroms", required=False
    )

    # dose filtering arguments
    parser.add_argument("--dose_file", help="File with dose to correct", required=False)

    args = vars(parser.parse_args())

    # dose filtering
    if args["dose_filter"]:
        if (
            args["input_file"] is None
            or args["pixel_size"] is None
            or args["dose_file"] is None
            or args["pixel_size"] is None
        ):
            parser.error("dose_filter requires --input_file, --pixel_size, --dose_file, and --output_file.")
        else:
            tiltstack.dose_filter(args["input_file"], args["pixel_size"], args["dose_file"], args["output_file"])


# if __name__ == "__main__":
#     main()
#     main2*()
