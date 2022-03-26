import os
from fpdf import FPDF

def images2pdf(outpath, images, w = 1920, h = 1080):
    pdf = FPDF()
    pdf.compress = False
    titleH = 60
    size=(h + titleH, w)
    for image in images:
        pdf.add_page(orientation = 'L', format=size, same=False)
        pdf.set_font('helvetica', size = titleH)
        pdf.cell(400, titleH, os.path.basename(image), 1, 1, 'C')
        pdf.image(image, 0, titleH + 10, w, h, 'JPG')

    pdf.output(outpath, "F")
    
if __name__ == '__main__': 
 images=['data/frame00:00:01-0.jpg', 'data/frame00:00:06-0.56.jpg']
 images2pdf('data/test.pdf', images)