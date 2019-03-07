set datafile separator ","
set terminal png size 1280,400
set title "nRF24l01+ Received Frames"
set xlabel "Time (s)"
set xdata time
set xrange [4:6]
set yrange [0:2]
set timefmt "%s"
set format x "%s"
set key left top
set grid
plot "nrf24_raw.log" using 2:($3/$3) with impulses title 'frames'

