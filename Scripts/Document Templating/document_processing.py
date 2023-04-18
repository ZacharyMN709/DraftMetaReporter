from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import docx.opc.constants
import docx.oxml.ns

import config as cfg
import caching
import tier_parsing
import image_processing


def new_document(hori_margin=3.18, vert_margin=2.54):
    document = Document()
    sections = document.sections
    for section in sections:
        section.top_margin = Cm(vert_margin)
        section.bottom_margin = Cm(vert_margin)
        section.left_margin = Cm(hori_margin)
        section.right_margin = Cm(hori_margin)
    return document


def apply_default_font(font):
    font.name = cfg.FONT_NAME
    font.size = Pt(cfg.FONT_SIZE)
    font.color.rgb = RGBColor(*cfg.FONT_COLOR)


def add_hyperlink(document, run, url):
    r_id = document.part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    r = run._r
    r_hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
    r_hyperlink.set(docx.oxml.shared.qn('r:id'), r_id)
    r_hyperlink.set(docx.oxml.shared.qn('w:history'), '1')

    new_run = docx.oxml.shared.OxmlElement('w:r')
    r_properties = docx.oxml.shared.OxmlElement('w:rPr')

    new_run.append(r_properties)
    new_run.text = run.text
    r_hyperlink.append(new_run)

    run._r.getparent().replace(run._r, r_hyperlink)
    apply_default_font(run.font)

    return run


def set_cell_margins(cell, **kwargs):
    """
    provided values are in twentieths of a point (1/1440 of an inch).
    read more here: http://officeopenxml.com/WPtableCellMargins.php
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = docx.oxml.shared.OxmlElement('w:tcMar')

    for m in ["top", "start", "bottom", "end"]:
        if m in kwargs:
            node = docx.oxml.shared.OxmlElement("w:{}".format(m))
            node.set(docx.oxml.ns.qn('w:w'), str(kwargs.get(m)))
            node.set(docx.oxml.ns.qn('w:type'), 'dxa')
            tcMar.append(node)

    tcPr.append(tcMar)


def add_images(cell, card_name):
    height, width = image_processing.download_card_image(card_name)
    set_cell_margins(cell, top=0, start=0, bottom=0, end=0)
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    paragraph.add_run().add_picture(cfg.TEMP_LOC, height=Inches(height), width=Inches(width))


def add_grade(cell, card_name, grader):
    grade = tier_parsing.SET_GRADES.loc[card_name][grader].strip()
    if grade.startswith('BA'):
        grade = f"{grade[2:]}, \nBuild-Around"
    if grade.startswith('SYN'):
        grade = f"{grade[3:]}, \nSynergy"

    cell.text = f"{grader}: {grade}"
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = paragraph.runs[0]
    run.bold = True
    font = run.font
    font.name = cfg.FONT_NAME
    font.size = Pt(12)
    font.color.rgb = RGBColor(0x00, 0x00, 0x00)


def add_card_to_document(document, card_name):
    style = document.styles['Heading 3']
    apply_default_font(style.font)

    heading = document.add_heading("", level=3)
    heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = heading.add_run(card_name)
    card_data = caching.get_card_data(card_name)
    card_url = card_data["scryfall_uri"]

    add_hyperlink(document, run, card_url)
    table = document.add_table(rows=3, cols=4)
    add_images(table.cell(0, 0), card_name)
    table.cell(0, 0).merge(table.cell(1, 2))

    add_grade(table.cell(0, 3), card_name, 'Marc')
    add_grade(table.cell(1, 3), card_name, 'Alex')

    paragraph = table.cell(2, 0).paragraphs[0]
    paragraph.style = 'List Bullet'
    table.cell(2, 0).merge(table.cell(2, 3))