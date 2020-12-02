# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from tkinter import filedialog
from draw import draw
import csv


if __name__ == "__main__":

    filename = input("Type the name of the new file: ")

    # Set up the new PDF file

    pdf = canvas.Canvas("{}.pdf".format(filename))
    pdf.setPageSize((10 * cm, 14.8 * cm))

    # Register Japanese fonts

    registerFont(TTFont(
        "SourceHanSerif-Regular",
        "fonts/SourceHanSerifJP-Regular.ttf"
    ))
    registerFont(TTFont(
        "SourceHanSerif-Light",
        "fonts/SourceHanSerifJP-Light.ttf"
    ))

    # Ask for the from_data

    from_data = dict()

    from_data["name"] = input("Your name: ")
    from_data["postcode"] = input("Postcode: ")
    from_data["address1"] = input("Address (prefecture, state and city): ")
    from_data["address2"] = input("Address (more specified info): ")
    from_data["address3"] = input("Address (unit or room number [optional]): ")

    # Input dest_data from a csv file

    while True:
        try:
            filetype = [("CSV File", "*.csv")]
            filename = filedialog.askopenfilename(filetypes=filetype)

            with open(filename, "rt", encoding="shift_jis") as fin:
                reader = csv.reader(fin)

                for row in reader:
                    dest_data = {
                            "name": row[0],
                            "postcode": row[7],
                            "address1": row[8],
                            "address2": row[9],
                            "address3": row[10]
                            }

                    draw(pdf, dest_data, from_data)

        except FileNotFoundError:
            print("File not found. Please check and specify it again.")

        else:
            break

    pdf.save()
