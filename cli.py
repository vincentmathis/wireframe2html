import argparse
import os
import webbrowser

import extract
import generate
import logger
import predict


def generate_from_image(args):
    _, elements = extract.get_elements_from_path(args.image)

    for ele in elements:
        ele.append(predict.get_prediction(ele))

    if not args.no_align:
        generate.align_elements(elements)
        logger.log_info("Tried aligning bounding boxes", dim=True)

    html = generate.generate_html(elements)
    logger.log_info("Generated HTML for classified elements", dim=True)

    with open(args.output_file, "w+") as html_file:
        html_file.write(html)
    logger.log_info(f"Written HTML to '{args.output_file}'")

    logger.log_info(f"Opening '{args.output_file}' in browser", dim=True)
    webbrowser.open("file://" + os.path.realpath(args.output_file))


def main():
    parser = argparse.ArgumentParser(description="Generate HTML from wireframe image.")
    parser.add_argument("image")
    parser.add_argument("-o", "--output-file", default="output.html")
    parser.add_argument("-na", "--no-align", action="store_true")
    generate_from_image(parser.parse_args())


if __name__ == "__main__":
    main()
