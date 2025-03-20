def create_tex_table(table_contents):
    """
    Generates .tex code for table with given contents.

    :param table_contents: list of lists with table values. Assumes all inner lists are the same positive length.
    :return: valid compilable .tex code for table
    """

    result = '\\begin{center}\n\\begin{tabular}'
    result += '{||' + '|'.join('c' for _ in range(len(table_contents[0]))) + '||}'

    result += '\n \\hline\n' + '\n \\hline\n'.join(' &'.join(f' {str(value)}' for value in row_contents) + ' \\\\' for row_contents in table_contents) + '\n \\hline\n'

    result += '\\end{tabular}\n\\end{center}\n'

    return result


def create_text_png(path: str):
    """
    Generates .tex code for inserting a .png image with given path.

    :param path: path to .png image
    :return: valid compilable .tex code for image
    """

    return '\\begin{center}\n\\begin{figure}[H]\n\\includegraphics[width=\linewidth]{' + path + '}\n\\label{fig:mpr}\n\\end{figure}\n\\end{center}\n'
