FROM docker:dind

RUN apk add --no-cache python3 && pip3 install --upgrade pip

COPY . nita-cli/

RUN pip3 install -I nita-cli/ --no-binary :all:

LABEL net.juniper.image.release="20.0.0" \
      net.juniper.framework="NITA"

VOLUME /project

# Run the nita command by default.
ENTRYPOINT ["nita"]
CMD ["--help"]
