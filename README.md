## extract ppt from a video

If The video form is taught through ppt, then this tool can extract the ppt from the video and export a pdf file.

Format of image names in the export pdf: frame${timestamp}-${similarity}.jpg

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
python3 ./video2ppt/video2ppt.py --similarity 0.6 --pdfname hello.pdf ./demo ./demo/demo.mp4
```

### frame detail
![alt frame detail](./demo/demo.png "frame detail")