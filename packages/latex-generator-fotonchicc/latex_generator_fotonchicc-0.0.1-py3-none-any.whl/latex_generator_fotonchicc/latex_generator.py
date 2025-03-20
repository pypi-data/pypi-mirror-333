from typing import List


def generate_latex_table(data: List[List[str]]) -> str:
    columns_format = "{" + "|c" * len(data[0]) + "|}"
    rows_data = []
    for row in data:
        rows_data.append((" & ".join(map(str, row)) + " \\\\"))

    latex_table = ("\\centering\n"
                   f"\\begin{{tabular}}{columns_format}"
                   "\n\hline\n" +
                   rows_data[0] +
                   "\n\hline \hline\n" +
                   "\n\hline\n".join(rows_data[1:]) +
                   "\n\hline\n"
                   "\\end{tabular}"
                   )
    return latex_table


def generate_latex_image(image_path: str, width: float = 0.7, position: str = "h", alignment: str = "centering",
                         caption: str = "Sample image", label: str = "fig:sample") -> str:
    latex_image = (f"\\begin{{figure}}[{position}]\n"
                   f"\\{alignment}\n"
                   f"\\includegraphics[width={width}\linewidth]{{{image_path}}}\n"
                   f"\\caption{{{caption}}}\n"
                   f"\\label{{{label}}}\n"
                   "\\end{figure}\n")
    return latex_image
