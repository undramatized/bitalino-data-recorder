FROM python:3

COPY . /
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./src/VideoPlayer.py" ]

# docker build -t bitalino-recorder .
# docker run bitalino-recorder
# docker run --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" bitalino-recorder


