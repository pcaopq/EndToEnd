import re

class Report_generator():
	tmpl_path = './template.tex'
	report_path = './report.tex'

	def __init__(self, tmpl_path, report_path):
		self.tmpl_path = tmpl_path
		self.report_path = report_path

	def read_tmpl(self):
		tmpl_file = open(self.tmpl_path)
		tmpl_content = tmpl_file.read()
		return tmpl_content

	def generate_table(self, alg_name, eval_results):

		table = """
				\\begin{table}[htbp]
				\\centering
				\\begin{tabular}{|c|c|c|c|}
				\\hline
				algorithm&precision&recall&fscore\\\\
				\\hline
				"""
		for i, name in enumerate(alg_name):
			r = eval_results[name]
			table += name + '&' + str(r['precision']) + '&' + str(r['recall']) + \
				'&' + str(r['fscore']) + '\\\\\n'

		table += """
				\\hline
				\\end{tabular}
				\\end{table}
				 """
		return table

	def generate_table_outlier(self, scores):

		table = """
				\\begin{table}[htbp]
				\\centering
				\\begin{tabular}{|c|c|c|}
				\\hline
				filename&algorithm&score\\\\
				\\hline
				"""
		print(scores)
		for counter,score in enumerate(scores):
			#r = eval_results[name]
			table +=  str(score[0]) + '&'  + str(score[1]) + '&' + str(score[2]) + '\\\\\n'

		table += """
				\\hline
				\\end{tabular}
				\\end{table}
				 """
		return table
	def generate_plot(self):
		plot =  """
				\\begin{figure}[!htbp]
				\centering
				\includegraphics[width = 8cm]{performance.png}
				\end{figure}
				\\\\
				"""

		return plot

	def generate_outlier(self, alg_name):
		outlier = ''
		for alg in alg_name:
			b_name = alg+'.best.png'
			b_gt_name = alg+'.gt.best.png'
			w_name = alg+'.worst.png'
			w_gt_name = alg+'.gt.worst.png'
			fig =   """
					\\begin{figure}
					\centering
					\\begin{subfigure}{.5\\textwidth}
					  \centering
					  \includegraphics[width=10cm]
					"""+'{'+b_name+'}'+\
					"""
					  \caption{best result}
					  \label{fig:sub1}
					\end{subfigure}%
					\\begin{subfigure}{.5\\textwidth}
					  \centering
					  \includegraphics[width=10cm]
					"""+'{'+b_gt_name+'}'+\
					"""
					  \caption{ground truth}
					  \label{fig:sub2}
					\end{subfigure}
					\caption
					"""+'{best result of '+alg+'}'+\
					"""
					\label{fig:test}
					\end{figure}
					"""
			outlier += fig
			fig =   """
					\\begin{figure}
					\centering
					\\begin{subfigure}{.5\\textwidth}
					  \centering
					  \includegraphics[width=10cm]
					"""+'{'+w_name+'}'+\
					"""
					  \caption{worst result}
					  \label{fig:sub1}
					\end{subfigure}%
					\\begin{subfigure}{.5\\textwidth}
					  \centering
					  \includegraphics[width=10cm]
					"""+'{'+w_gt_name+'}'+\
					"""
					  \caption{ground truth}
					  \label{fig:sub2}
					\end{subfigure}
					\caption
					"""+'{worst result of '+alg+'}'+\
					"""
					\label{fig:test}
					\end{figure}
					"""
			outlier += fig
		return outlier

	def generate_report(self, alg_name, eval_results, good_scores, bad_scores,filter_good,filter_bad):
		tmpl = self.read_tmpl()
		report_file = open(self.report_path, 'w+')
		table = self.generate_table(alg_name, eval_results)
		outlier = self.generate_outlier(alg_name)
		good_outlier = self.generate_table_outlier(good_scores)
		bad_outlier = self.generate_table_outlier(bad_scores)
		content = tmpl.replace('TABLE', table).replace('OUTLIERS', outlier)\
					.replace('NUMBER', str(eval_results[alg_name[0]]['num_images']))
		content = content.replace('GOOD', good_outlier)
		content = content.replace('GSCORE', str(filter_good))
		content = content.replace('BAD', bad_outlier)
		content = content.replace('BSCORE', str(filter_bad))
		report_file.write(content)

def main():
	generator = Report_generator()
	generator.generate_report()

if __name__ == '__main__':
	main()
