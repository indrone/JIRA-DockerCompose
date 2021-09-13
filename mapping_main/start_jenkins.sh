docker build -t mapping_main .

 if sudo docker ps -a --format '{{.Names}}' | grep -Eq "^mapping_main\$"; then
  sudo docker stop mapping_main || true
fi

docker run -p 8026:8026 -v \
~/workspace/classification/mapping_main/logs:\
/mapping_main/logs:rw -v ~/workspace/classification/mapping_main/mapping_output:\
/mapping_main/mapping_output:rw -d mapping_main:latest