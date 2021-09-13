docker build -t mapping_main .

 

docker run -p 8026:8026 -v \
~/classification/mapping_main/logs:\
/mapping_main/logs:rw -v ~/classification/mapping_main/mapping_output:\
/mapping_main/mapping_output:rw -d mapping_main