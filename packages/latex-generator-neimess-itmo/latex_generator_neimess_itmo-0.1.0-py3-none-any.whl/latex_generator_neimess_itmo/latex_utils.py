from typing import List
import os

def mtx(matrix: List[List[object]], **kwargs) -> str:
    """
    Convert a matrix into a valid LaTeX-formatted table string.

    Args:
        matrix (List[List[object]]): The matrix to convert, containing elements convertible to str.
        **kwargs: Additional optional arguments:
            - hlines (bool): Include horizontal lines. Default: True.
            - vlines (bool): Include vertical lines. Default: True.
            - col_align (str): Alignment for each column (e.g. "c", "l", "r"). Default: "c".
            - table_env (bool): If True, wrap the tabular in a table environment. Default: False.
            - pos (str): Positioning option for the table environment (e.g. "h", "H", "t", "b", "p"). Default: "h".
            - caption (str): Caption for the table. Default: None.
            - label (str): Label for referencing the table. Default: None.

    Returns:
        str: A string containing LaTeX-formatted table code.
    """

    if not matrix or not matrix[0]:
        return ""

    hlines = kwargs.get("hlines", True)
    vlines = kwargs.get("vlines", True)
    col_align = kwargs.get("col_align", "c")
    table_env = kwargs.get("table_env", False)
    pos = kwargs.get("pos", "h")
    caption = kwargs.get("caption", None)
    label = kwargs.get("label", None)

    cols = len(matrix[0])
    table_format = ("|" if vlines else "") + (col_align + ("|" if vlines else "")) * cols

    header = f"\\begin{{tabular}}{{{table_format}}}\n" + ("\\hline\n" if hlines else "")
    body = "\n".join(
        " & ".join(map(str, row)) + " \\\\" + ("\\hline" if hlines else "")
        for row in matrix
    )
    tabular_code = header + body + "\n" + "\\end{tabular}"

    if table_env:
        table_header = f"\\begin{{table}}[{pos}]\n"
        table_footer = "\\end{table}"
        caption_code = f"\\caption{{{caption}}}\n" if caption else ""
        label_code = f"\\label{{{label}}}\n" if label else ""
        latex_code = table_header + tabular_code + "\n" + caption_code + label_code + table_footer
    else:
        latex_code = tabular_code

    return generate_latex(latex_code, False)


def image_latex(image_path: str, **kwargs) -> str:
    """
    Generates LaTeX code for embedding an image with optional parameters.
    Args:
        image_path (str): Path to the image file.
        **kwargs: Additional optional arguments:
            - centering (bool): Whether to center the image (default: True).
            - position (str): Positioning option for figure ('h', 't', 'b', 'p', !,  etc.). Default: "h".
            - caption (str): Caption for the image (default: "").
            - label (str): Label for referencing the image (default: "fig:my_label").
            - width (str): Width of the image (default: "\textwidth").
            

    Returns:
        str: A string containing LaTeX-formatted image code.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"File {image_path} not found!")
    
    centering = kwargs.get("centering", True)
    position = kwargs.get("position", "h")
    caption = kwargs.get("caption", False)
    label = kwargs.get("label", "fig:my_label")
    position = kwargs.get("position", "h")
    width = kwargs.get("width", r"\textwidth")
    
    header = rf"\begin{{figure}}[{position}]" + "\n"
    center = r"\centering" + "\n" if centering else ""
    body = rf"\includegraphics[width={width}]{{{image_path}}}" + "\n"
    caption_text = rf"\caption{{{caption}}}" + "\n" if caption else ""
    label_text = rf"\label{{{label}}}" + "\n"
    footer = r"\end{figure}"
    latex_code = header + center + body + caption_text + label_text + footer
    return generate_latex(latex_code, True)

def generate_latex(latex_code: str, graphicx: bool = False) -> str:
    """
    Generates a basic LaTeX document with an optional graphicx package.

    Args:
        latex_code (str): The main body LaTeX code (e.g., figure, table).
        graphicx (bool): Whether to include the graphicx package (default: True).

    Returns:
        str: A LaTeX document as a string.
    """
    graphicx_package = "\\usepackage{graphicx}" if graphicx else ""

    tex_doc = f"""
\\documentclass{{article}}
{graphicx_package}
\\begin{{document}}
{latex_code}
\\end{{document}}"""

    return tex_doc