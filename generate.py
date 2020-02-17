import numpy as np
import lorem
from yattag import Doc, indent

CSS_URL = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
CSS_SHA = "sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"


def generate_html(elements):
    doc, tag, text, line = Doc().ttl()
    doc.asis("<!DOCTYPE html>")
    with tag("html"):
        with tag("head"):
            line("title", "Output")
            doc.stag(
                "link",
                rel="stylesheet",
                href=CSS_URL,
                integrity=CSS_SHA,
                crossorigin="anonymous",
            )
        with tag("body"):
            doc.asis(generate_elements(elements))
    return indent(doc.getvalue())


def get_min_x_y(elements):
    bboxes = np.array(elements)[:, 1]
    bboxes = np.array(bboxes.tolist())
    min_x, min_y, _, _ = np.min(bboxes, axis=0)
    return min_x, min_y


def generate_elements(elements):
    doc = Doc()
    if elements[0][2][0] == "navbar":
        doc.asis(generate_navbar(None))
        elements = elements[1:]
        min_x, min_y = get_min_x_y(elements)
        min_x -= 50
        min_y -= 100
    else:
        min_x, min_y = get_min_x_y(elements)
        min_x -= 50
        min_y -= 50

    for ele in elements:
        crop, bbox, pred = ele
        category, prob = pred
        generate_function = globals()["generate_" + category]
        position = (bbox[0] - min_x, bbox[1] - min_y, bbox[2], bbox[3])
        with doc.tag("div", style=build_style_string(position)):
            doc.asis(generate_function(position))
    return doc.getvalue()


def build_style_string(bbox):
    x_pos, y_pos, width, height = bbox
    string = "position:absolute;"
    string += "overflow: hidden;"
    string += f"left:{x_pos:.0f}px;"
    string += f"top:{y_pos:.0f}px;"
    string += f"width:{width:.0f}px;"
    string += f"height:{height:.0f}px;"
    return string


def generate_button(_):
    doc = Doc()
    doc.line("button", "Button", klass="btn btn-primary w-100")
    return doc.getvalue()


def generate_checkbox(_):
    doc = Doc()
    doc.stag("input", type="checkbox")
    return doc.getvalue()


def generate_image(bbox):
    _, _, width, height = bbox
    src = f"https://source.unsplash.com/random/{width}x{height}"
    doc = Doc()
    doc.stag("img", src=src)
    return doc.getvalue()


def generate_label(_):
    doc = Doc()
    doc.text("Label")
    return doc.getvalue()


def generate_navbar(_):
    doc, tag, text, line = Doc().ttl()
    with tag("nav", klass="navbar fixed-top navbar-expand-lg navbar-dark bg-dark"):
        line("a", "Navbar", klass="navbar-brand", href="#")
        with tag("ul", klass="navbar-nav mr-auto"):
            with tag("li", klass="nav-item active"):
                line("a", "Home", klass="nav-link", href="#")
            with tag("li", klass="nav-item"):
                line("a", "About", klass="nav-link", href="#")
        with tag("form", klass="form-inline my-2 my-lg-0"):
            doc.stag(
                "input",
                klass="form-control mr-sm-2",
                type="search",
                placeholder="Search",
            )
            line(
                "button",
                "Search",
                klass="btn btn-outline-light my-2 my-sm-0",
                type="submit",
            )
    return doc.getvalue()


def generate_pagination(bbox):
    x_pos, y_pos, width, _ = bbox
    pages = int((width - 120) / 40)
    doc, tag, _, line = Doc().ttl()
    with tag("div", klass="d-flex justify-content-center"):
        with tag("nav"):
            with tag("ul", klass="pagination"):
                with tag("li", klass="page-item"):
                    line("a", "Prev", klass="page-link", href="#")
                for i in range(pages):
                    with tag("li", klass="page-item"):
                        line("a", str(i + 1), klass="page-link", href="#")
                with tag("li", klass="page-item"):
                    line("a", "Next", klass="page-link", href="#")
    return doc.getvalue()


def generate_radiobutton(_):
    doc = Doc()
    doc.stag("input", type="radio")
    return doc.getvalue()


def generate_table(bbox):
    _, _, width, height = bbox
    cols = int(width / 150)
    rows = int(height / 50) - 1
    doc, tag, _, line = Doc().ttl()
    with tag("table", klass="table table-bordered"):
        with tag("thead"):
            with tag("tr"):
                line("th", "#", scope="col")
                for _ in range(cols):
                    line("th", "Column", scope="col")
        with tag("tbody"):
            for i in range(rows):
                with tag("tr"):
                    line("th", str(i + 1), scope="row")
                    for _ in range(cols):
                        line("td", "Data")
    return doc.getvalue()


def generate_text(bbox):
    _, _, width, height = bbox
    area = width * height
    max_words = int(area / 1100)
    text = lorem.get_word(count=max_words)
    doc = Doc()
    doc.line("p", text)
    return doc.getvalue()


def generate_textinput(_):
    doc = Doc()
    doc.stag("input", klass="form-control", type="text")
    return doc.getvalue()


def align_elements(elements):
    for i in range(len(elements) - 1):
        _, bbox, _ = elements[i]
        for j in range(i + 1, len(elements)):
            _, other, _ = elements[j]
            for k in range(4):
                bbox[k] = round(bbox[k], -1)
                other[k] = round(other[k], -1)
                if abs(bbox[k] - other[k]) <= 20:
                    other[k] = bbox[k]
