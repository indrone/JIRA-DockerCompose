docker build -t classification_main .


if sudo docker ps -a --format '{{.Names}}' | grep -Eq "^classification_main\$"; then
  sudo docker stop classification_main || true
fi 

docker run -p 8025:8025 -v \
~/workspace/classification/classification_main/logs:\
/classification_main/logs:rw -v \
~/workspace/classification/classification_main/classification_output:\
/classification_main/classification_output:rw -d classification_main:latest