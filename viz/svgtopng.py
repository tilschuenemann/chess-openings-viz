from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

drawing = svg2rlg("diagram.svg")
renderPDF.drawToFile(drawing, "Chess_Tree.pdf")


