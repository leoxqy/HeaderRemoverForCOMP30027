import argparse
from PIL import Image
from pathlib import Path
from pdf2image import convert_from_path
import os

def parse_args():
    descriptions = "pdf header remover "
    epilog = "by Leo Xinqi Yu from UniMelb COMP30027 Machine Learning"
    parser = argparse.ArgumentParser(description=descriptions, epilog=epilog)

    parser.add_argument('-ipath', '--input folder', dest="in_folder",
                        help="The path containing the target PDFs.")
    parser.add_argument('-opath', '--variable mode', dest="out_folder",
                        help="The output folder")
    
    op = parser.parse_args()

    return op

def makePDF(imgs, oPath):
    images = [Image.open(f) for f in imgs ]
    oPath = oPath / "converted.pdf"
    images[0].save(oPath, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])

def core(pdf, oPath):
    print("====== Converting PDF to images ======")
    images = convert_from_path(pdf)
    imgs = []

    for i in range(len(images)):
        # Save pages as images in the pdf
        imgPath = oPath / ('temp_' + str(i) + '.jpeg')
        imgs.append(oPath / ('changed_' + str(i) + '.png'))
        images[i].save(imgPath, 'JPEG')
        convert(imgPath, oPath, i)

    makePDF(imgs, oPath)
    print("--- Header removed! ---")

    # for i in range(len(images)):
    #     # Save pages as images in the pdf
    #     images[i].save('page'+ str(i) +'.jpg', 'JPEG')

def convert(target_img, oPath,i):
    image = Image.open(target_img)
    image_data = image.load()
    height, width = image.size
    tar_color = image_data[5, 220]
    for loop1 in range(height):
        for loop2 in range(30,430):
            c = image_data[loop1,loop2]
            if c == tar_color:
                image_data[loop1,loop2] = 255,255,255
    image.save(oPath / ('changed_' + str(i) + '.png'))

    

if __name__ == "__main__":

    op = parse_args()
    if not (op.in_folder and op.out_folder):
        print("Missing args - Remember to enter in and out folder : headerRemover.py -ipath path_to_input_folder -opath path_to_output_folder ")
        exit()

    iPath = op.in_folder
    oPath = op.out_folder
    
    # get all potentially existing input files
    filelist = os.listdir(iPath)
    pdfs = []
    iPath = Path(iPath)
    oPath = Path(oPath)
    pdfIdx = 0
    for f in filelist:
        if f.endswith(".pdf"):
                pdfs.append( iPath / f)

    for pdf in pdfs:
        curOPath = oPath / str(pdfIdx)
        try:
            os.mkdir(curOPath)
        except FileExistsError:
            print("Folder already exist, pleast clear your out folder and try again.")
            exit()
        core(pdf, curOPath)
        pdfIdx+=1

