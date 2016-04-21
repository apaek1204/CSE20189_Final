reset

set title "Latency of Single Connection and Forking Mode"
set auto x
set xlabel "Type"
set ylabel "Time (seconds)"
set auto y
set style data histogram
set style histogram cluster gap 2
set style line 1 lt 1 lc rgb "cyan"
set style line 2 lt 1 lc rgb "gray"
set style fill solid border -1
set key left
set boxwidth 0.9
set output "latency.png"
set term png
plot "latency_data.txt" using 2:xtic(1) ti col, '' u 3 ti col
