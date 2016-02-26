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

	def generate_table(self, data):
		table = """ 
\\begin{table}[htbp]
\\centering
\\begin{tabular}{|c|c|c|c|}
\\hline
&precision&recall&score\\\\
\\hline
				"""
		for i in range(len(data)):
			table += str(i) + '&' + str(data[i][0]) + '&' + str(data[i][1]) + '&' + str(data[i][2]) + '\\\\\n'

		table += """
\\hline
\\end{tabular}
\\end{table}
				 """
		return table

	def generate_plot(self):
		plot = """	
\\begin{figure}[!htbp]
\centering
\includegraphics[width = 8cm]{performance.png} 
\end{figure}
\\\\"""
		
		return plot

	def generate_report(self, data):
		tmpl = self.read_tmpl()
		report_file = open(self.report_path, 'w+')
		table = self.generate_table(data)
		content = tmpl.replace('TABLE', table)
		report_file.write(content)

def main():
	generator = Report_generator()
	generator.generate_report()

if __name__ == '__main__':
	main()