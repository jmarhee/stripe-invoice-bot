import tabulate

def generate_table(data):
	headings = data[0].keys()
	rows = [x.values() for x in data]
	return "```\n" + tabulate.tabulate(rows,headings) + "\n```"
