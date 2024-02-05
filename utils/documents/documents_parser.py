from docxtpl import DocxTemplate
from docx.shared import Mm

from utils.documents.html_to_docx import HtmlToDocx


class MyDocxTemplate(DocxTemplate):
    def init_docx(self):
        self.docx = self.template_file
        self.section = self.docx.sections[0]
        self.section.page_height = Mm(297)
        self.section.page_width = Mm(210)
        self.section.left_margin = Mm(20.0)
        self.section.right_margin = Mm(10.0)
        self.section.top_margin = Mm(10.0)
        self.section.bottom_margin = Mm(10.0)
        self.section.header_distance = Mm(12.7)
        self.section.footer_distance = Mm(12.7)
        super(MyDocxTemplate, self).init_docx()


def render_new_doc(block, context, responce):
    full_text = block

    new_parser = HtmlToDocx()

    new_doc = new_parser.parse_html_string(full_text)

    doc = MyDocxTemplate(new_doc)
    doc.render(context)
    doc.save(responce)
