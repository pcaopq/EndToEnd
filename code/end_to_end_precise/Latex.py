import EvaluateBatch
import os

with open('LatexTemplate.tex') as f:
    latex_template = f.read()

def replace_dict(string, replacements):
    for k,v in replacements.items():
        string = string.replace(k,v)
    return string

def gen_latex(title, fnameout):
    PC = '''\\includegraphics[width=15cm]{PrecisionRecallScatter.png}
            \\includegraphics[width=15cm]{PerformanceCurve.png}'''
    SUM = '''%d documents analyzed.''' % len(EvaluateBatch.pair_fscores)
    latex = replace_dict(latex_template, {'TITLE':title,
                                          'PERFORMANCE CURVES':PC,
                                          'SUMMARY':SUM})
    with open(fnameout,'w') as f:
        f.write(latex)

def gen_pdf(fnametex, fnamepdf):
    os.system('pdflatex %s %s' % (fnametex,fnamepdf))
