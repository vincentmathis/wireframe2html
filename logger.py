from colorama import Fore, Style, init

INITIALIZED = False
if not INITIALIZED:
    init()
    INITIALIZED = True


def log_info(string, dim=False):
    if dim:
        print(f"{Style.DIM}[INFO] {string}{Style.RESET_ALL}")
    else:
        print(f"[INFO] {string}")


def log_prediction(category, prob, bbox):
    x_pos, y_pos, width, height = bbox
    if prob >= 0.9:
        color = Fore.GREEN
    elif prob >= 0.7:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    category = f"'{category}'"
    prob_str = f"(prob: {color}{prob:>4.0%}{Style.RESET_ALL})"
    bbox_str = f"(x:{x_pos:>4.0f}, y:{y_pos:>4.0f}, w:{width:>4.0f}, h:{height:>4.0f})"
    info = f"Predicted {category:13} {prob_str} at {bbox_str}"
    log_info(info)


def log_warning(string):
    print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} {string}")


def log_failure(string):
    print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} {string}")
