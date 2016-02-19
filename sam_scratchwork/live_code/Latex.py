L = '''
\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{graphicx}
\\title{TITLE}
\\date{}

\\begin{document}

\\maketitle

\\setcounter{section}{-1}
\\section{Summary}
SUMMARY
\\section{Performance Curves}
PERFORMANCE CURVES
\\section{Outliers}
OUTLIERS
\\end{document}
'''

import EvaluateBatch


def gen_latex(title, fnameout):
    PC = '''\\includegraphics[width=15cm]{TEST.png}

    \\includegraphics[width=15cm]{TEST2.png}'''
    SUM = '''%d documents analyzed.''' % len(EvaluateBatch.pair_fscores)
    myL = L.replace('TITLE',title).replace('PERFORMANCE CURVES',PC).replace('SUMMARY',SUM)
    with open(fnameout,'w') as f:
        f.write(myL)

gen_latex('Eval Results', 'EV.tex')
