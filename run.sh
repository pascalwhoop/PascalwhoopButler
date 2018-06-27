docker rm butler
docker run \
--name=butler \
    -v /home/pascalwhoop/Documents/Dropbox/reading:/reading \
    -v /home/pascalwhoop/Documents/Code/website/pascalbrokmeier.de:/pascalbrokmeier.de \
    -u 1000:1000 \
    pascalwhoop/butler

