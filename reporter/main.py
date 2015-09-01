#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape

import csv


def go(data_file):
    attendee_data = csv.reader(open(data_file, 'rb'))
    for row in attendee_data:
        last_name, first_name, course_name = row

        #  pdf_filename = '_'.join((course_name, last_name, first_name)) + '.pdf'
        pdf_filename = "report.pdf"
        generate_cert(first_name, last_name, course_name, pdf_filename)


def generate_cert(first_name, last_name, course_name, pdffirst_name):
    c = canvas.Canvas(pdffirst_name, pagesize=landscape(letter))

    # Header text

    # Requires it to be locally installed
    c.setFont('Times-Roman', 48, leading=None)

    # What do these mean? 500 is from bottom of page?
    c.drawCentredString(415, 500, "Certificate of Completion")

    c.setFont('Times-Roman', 24, leading=None)
    c.drawCentredString(415, 450, "This certificate is presented to:")

    # attendee name
    attendee_name = first_name + ' ' + last_name
    c.setFont('Times-Bold', 34, leading=None)
    c.drawCentredString(415, 395, attendee_name)

    c.setFont('Times-Roman', 24, leading=None)
    c.drawCentredString(415, 350, "for completing the following course:")

    # Course name
    c.setFont('Times-Bold', 20, leading=None)
    c.drawCentredString(415, 310, course_name)

    # seal
    seal = 'tx-appleseed-logo.png'
    c.drawImage(seal, 340, 50, width=146, height=196)

    c.showPage()
    c.save()


def main():
    """Run main."""
    import argparse
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('data_file', metavar='FILENAME',
                        help='The file to processs')
    args = parser.parse_args()
    go(args.data_file)

    return 0

if __name__ == '__main__':
    main()
