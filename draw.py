# -*- coding: utf-8 -*-

from reportlab.lib.units import cm


def draw(pdf, dest_data, from_data):

    # Draw a name

    vertical_draw(
            pdf,
            dest_data['name'] + ' 様',
            font_size=28,
            x=5*cm,
            y=7*cm + 14 * (len(dest_data) + 2)
            )

    # Draw an address(dest_data)

    if len(dest_data['address1'] + dest_data['address2']) > 20:
        font_size = 12
    else:
        font_size = 14

    vertical_draw(
            pdf,
            dest_data['address1'] + dest_data['address2'],
            font_size=font_size,
            x=8.5*cm,
            y=12*cm,
            space=0.1*cm
            )

    vertical_draw(
            pdf,
            dest_data["address3"],
            font_size=font_size,
            x=7.5*cm,
            y=2*cm + 14 * len(dest_data["address3"]),
            space=0.1*cm
            )

    postcode = dest_data["postcode"]
    postcode = postcode[0:3] + postcode[4:]
    postcode = '     '.join(tuple(postcode))

    pdf.setFont("SourceHanSerif-Regular", 11.25)
    pdf.drawString(4.5*cm, 12.75*cm, postcode)

    # Draw an address(from_data)

    height = 5 + 0.1 * cm
    height *= len(from_data['address1'] + from_data['address2'])
    height += 2 * cm

    vertical_draw(
            pdf,
            from_data['address1'] + from_data['address2'],
            font_size=5,
            x=2*cm,
            y=height,
            space=0.1*cm
            )

    vertical_draw(
            pdf,
            from_data['address3'],
            font_size=5,
            x=1.75*cm,
            y=0.2 * cm + (5 + 0.1 * cm) * len(from_data['address3']),
            space=0.1*cm
            )

    pdf.setFont("SourceHanSerif-Regular", 8)
    pdf.drawString(1.75*cm - 34, height + 10, '〒' + from_data['postcode'])

    vertical_draw(
            pdf,
            from_data['name'],
            font_size=8,
            x=1.15*cm,
            y=height-1*cm,
            space=0.1*cm
            )

    pdf.showPage()


def vertical_draw(
        pdf,
        text,
        font="SourceHanSerif-Regular",
        font_size=24,
        x=0,
        y=0,
        space=0.2*cm
        ):

    # Convert to numeric kanjis

    text = convert_to_numeric_kanjis(text)

    # Draw text

    pdf.setFont(font, font_size)

    for i, c in enumerate(text):

        if c == ' ':
            y += font_size * 0.75
            continue
        elif c == '　':
            y += font_size * 0.5
            continue

        pdf.drawString(x - (font_size / 2), y - i * (font_size + space), c)


def convert_to_numeric_kanjis(s):

    table = dict(zip((ord('0') + n for n in range(10)),
                     (ord(c) for c in '〇一二三四五六七八九')))
    table.update(dict(zip((ord('０') + n for n in range(10)),
                          (ord(c) for c in '〇一二三四五六七八九'))))

    res = list(s.translate(table))

    numeric_kanjis = '〇一二三四五六七八九十'

    for i, c in enumerate(res):
        if c == '｜' or c == '|' or c == 'ー' or c == '−' or c == '-':
            if (i > 0 and res[i - 1] in numeric_kanjis) and\
               (i < (len(s) - 1) and res[i + 1] in numeric_kanjis):
                res[i] = 'の'
            else:
                res[i] = '｜'

    return ''.join(res)
