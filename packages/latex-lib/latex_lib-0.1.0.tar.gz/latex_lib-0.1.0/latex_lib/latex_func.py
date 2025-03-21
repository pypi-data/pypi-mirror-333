def latex_table(data, use_header=False, use_hlines=False):
    """
    Генерирует код LaTeX для таблицы
    На вход: двойной список (список списков) с данными таблицы
    На выходе: строка с кодом LaTeX
    use_header: отделяет первую строку в заголовок
    use_hlines: добавляет горизонтальные линии
    """

    num_columns = len(data[0])
    col_format = " | " + " | ".join(["c"] * num_columns) + " | "

    table_latex = ["\\documentclass{article}",
                   "\\usepackage[english, russian]{babel}",
                   "\\begin{document}",
                   "\\begin{table}[h!]",
                   "\\centering",
                   "\\begin{tabular}{" + col_format + "}",
                   " \\hline"]

    if use_header:
        table_latex.append("    " + " & ".join(map(str, data[0])) + " \\\\" + "[1ex]")
        table_latex.append("    \\hline\\hline")
        data = data[1:]

    for row in data:
        table_latex.append("    " + " & ".join(map(str, row)) + " \\\\")
        if use_hlines:
            table_latex.append("    \\hline")

    if not use_hlines:
        table_latex.append(" \\hline")

    table_latex.append("\\end{tabular}")
    table_latex.append("\\end{table}")
    table_latex.append("\\end{document}")

    return "\n".join(table_latex)


def latex_picture(path):
    """
    Генерирует код LaTeX для вставки картинки из репозитория
    На вход: путь из корня репы
    На выходе: строка с кодом LaTeX
    """

    picture_latex = ["\\documentclass{article}",
                     "\\usepackage{graphicx}%Вставка картинок правильная",
                     "\\usepackage{float}%Плавающие картинки",
                     "\\usepackage{wrapfig}%Обтекание фигур (таблиц, картинок и прочего)",
                     "\\begin{document}",
                     "\\begin{figure}[h]",
                     "\\centering",
                     "\\includegraphics[width=0.8\linewidth]{" + path + "}",
                     "\\end{figure}",
                     "\\end{document}"]

    return "\n".join(picture_latex)
