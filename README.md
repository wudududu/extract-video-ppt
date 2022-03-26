## extract ppt from a video

If The video content is included ppt, then this tool can extract the ppt from the video and export a pdf file. Or you can just transform video to pdf -,-.

## install
``` shell
# install from pypi
pip install extract-video-ppt

# or local
python ./setup.py install

# or local user
python ./setup.py install --user
```

### useage
``` shell
# help info
evp --help
# example
evp --similarity 0.6 --pdfname hello.pdf ./ ./test.mp4
# similarity: The similarity between this frame and the previous frame is less than this value and this frame will be saveed, default: 0.6
# pdfname: the name for export pdf 
```

### example
``` shell
evp --similarity 0.6 --pdfname hello.pdf ./demo ./demo/demo.mp4
```

### frame detail
![alt frame detail](./demo/demo.png "frame detail")