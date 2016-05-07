all: p1_report.pdf throughput.png latency.png

p1_report.pdf: p1_report.tex
	pdflatex p1_report.tex
	pdflatex p1_report.tex

throughput.png: throughput.plt
	gnuplot -persist throughput.plt

latency.png: latency.plt
	gnuplot -persist latency.plt

clean:
	rm -f p1_report.pdf *.png
