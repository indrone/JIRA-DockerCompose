docker build -t classification_main .

 

docker run -p 8025:8025 -v \
~/classification/classification_main/logs:\
/classification_main/logs:rw -v \
~/classification/classification_main/classification_output:\
/classification_main/classification_output:rw -d classification_main

