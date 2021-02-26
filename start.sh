export $(egrep -v '^#' .env | xargs)

docker run --gpus all --env-file ./.env -it -p 8888:8888 -p 6006:6006 -v $(pwd):/notebooks tf:latest \
jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --notebook-dir=/notebooks --NotebookApp.token=$PASSWORD