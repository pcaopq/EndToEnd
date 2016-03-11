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
				algorithm&precision&recall&score\\\\
				\\hline
				"""
		for i, name in enumerate(alg_name):
			r = eval_results[name]
			table += name + '&' + str(r['precision']) + '&' + str(r['recall']) + \
				'&' + str(r['score']) + '\\\\\n'

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

	def generate_report(self, alg_name, eval_results):
		tmpl = self.read_tmpl()
		report_file = open(self.report_path, 'w+')
		table = self.generate_table(alg_name, eval_results)
		content = tmpl.replace('TABLE', table)
		report_file.write(content)

def main():
	generator = Report_generator()
	generator.generate_report()

if __name__ == '__main__':
	main()