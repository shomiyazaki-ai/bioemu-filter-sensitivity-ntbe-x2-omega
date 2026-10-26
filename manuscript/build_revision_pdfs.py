"""Render the versioned Markdown sources with ReportLab and mathtext.
Run from any directory. Dependencies: reportlab, matplotlib, Pillow.
The Markdown files, not this renderer, contain the editable scientific text.
"""
from pathlib import Path
import re,html,hashlib
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,Table,TableStyle,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
import matplotlib
matplotlib.use('Agg')
from matplotlib import mathtext
from PIL import Image as PILImage
ROOT=Path(__file__).resolve().parents[1]
FONTS=Path('/usr/share/fonts/truetype/dejavu')
for n,filename in [('Body','DejaVuSerif.ttf'),('BodyBold','DejaVuSerif-Bold.ttf'),('Sans','DejaVuSans.ttf'),('SansBold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:pdfmetrics.registerFont(TTFont(n,str(FONTS/filename)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')
W,H=595.28,841.89;M=49;CW=W-2*M
styles={
'body':ParagraphStyle('body',fontName='Body',fontSize=9.7,leading=14.0,spaceAfter=7,splitLongWords=True,allowWidows=0,allowOrphans=0),
'h1':ParagraphStyle('h1',fontName='SansBold',fontSize=18.5,leading=23,spaceAfter=16,textColor=colors.HexColor('#133647'),keepWithNext=True),
'h2':ParagraphStyle('h2',fontName='SansBold',fontSize=11.5,leading=15,spaceBefore=13,spaceAfter=7,keepWithNext=True,textColor=colors.HexColor('#133647')),
'h3':ParagraphStyle('h3',fontName='SansBold',fontSize=10,leading=14,spaceBefore=9,spaceAfter=5,keepWithNext=True),
'caption':ParagraphStyle('caption',fontName='Sans',fontSize=8.3,leading=11.4,spaceAfter=10),
'cell':ParagraphStyle('cell',fontName='Sans',fontSize=8.0,leading=10.7,splitLongWords=True),
'ref':ParagraphStyle('ref',fontName='Body',fontSize=8.5,leading=12,spaceAfter=7,splitLongWords=True),
'meta':ParagraphStyle('meta',fontName='Sans',fontSize=9.0,leading=13,spaceAfter=4,textColor=colors.HexColor('#536672'))}
def inline(s):
    s=html.escape(s,quote=False)
    s=re.sub(r'`([^`]+)`',r'<font name="Mono" size="8.4">\1</font>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    def link(m):
        raw=m[1];url=raw.rstrip('.,;');trail=raw[len(url):]
        return '<link href="'+url+'" color="#235d77">'+url+'</link>'+trail
    s=re.sub(r'(https?://[^\s]+)',link,s)
    return s

def equation(s):
    tmp=ROOT/'manuscript/_equations';tmp.mkdir(exist_ok=True)
    p=tmp/(hashlib.sha256(s.encode()).hexdigest()[:12]+'.png')
    if not p.exists():mathtext.math_to_image('$'+s+'$',p,dpi=350,format='png',color='#111111')
    im=PILImage.open(p);w,h=im.size;scale=min(CW/w,0.25)
    return Image(str(p),width=w*scale,height=h*scale,hAlign='CENTER')

def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#cdd8dd'));c.setLineWidth(.4);c.line(M,38,W-M,38)
    c.setFont('Sans',7);c.setFillColor(colors.HexColor('#536672'))
    c.drawString(M,26,'NT-BE / X2-ω | Version 1.1.0')
    c.drawRightString(W-M,26,str(d.page));c.restoreState()

def render(path):
    lines=path.read_text().splitlines();story=[];i=0;metadata=True
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('!['):
            m=re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)',line);p=(path.parent/m[2]).resolve();im=PILImage.open(p);w,h=im.size
            cap=[];i+=1
            while i<len(lines) and not lines[i].strip():i+=1
            if i<len(lines) and lines[i].startswith('**Figure '):
                cap.append(Paragraph(inline(lines[i]),styles['caption']));i+=1
            story.append(KeepTogether([Spacer(1,5),Image(str(p),width=CW,height=CW*h/w),Spacer(1,6)]+cap));continue
        if line.startswith('$$'):
            story.extend([Spacer(1,4),equation(line[2:-2]),Spacer(1,10)]);i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                ln=lines[i].strip();cells=[x.strip() for x in ln[1:-1].split('|')]
                if not all(re.fullmatch(r':?-+:?',x) for x in cells):rows.append(cells)
                i+=1
            n=len(rows[0]);widths=([.17,.26,.57] if n==3 and 'Source' in rows[0][0] else [.15,.19,.27,.18,.21] if n==5 else [1/n]*n)
            data=[[Paragraph(inline(x),styles['cell']) for x in row] for row in rows]
            table=Table(data,colWidths=[CW*x for x in widths],repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8eff2')),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#87a0ad')),('LINEBELOW',(0,-1),(-1,-1),.4,colors.HexColor('#b6c6cf')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f7f8')])]))
            caption=[]
            if story and getattr(story[-1],'is_table_caption',False):caption=[story.pop()]
            story.append(KeepTogether(caption+[table,Spacer(1,10)]));continue
        if line.startswith('# '):story.append(Paragraph(inline(line[2:]),styles['h1']));i+=1;continue
        if line.startswith('## '):metadata=False;story.append(Paragraph(inline(line[3:]),styles['h2']));i+=1;continue
        if line.startswith('### '):story.append(Paragraph(inline(line[4:]),styles['h3']));i+=1;continue
        para=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','![','$$')):para.append(lines[i].strip());i+=1
        s=' '.join(para)
        st='meta' if metadata else 'caption' if s.startswith(('**Figure','**Table')) else 'ref' if re.match(r'^\[\d+\]',s) else 'body'
        para=Paragraph(inline(s),styles[st])
        if s.startswith('**Table'):
            para.keepWithNext=True
            para.is_table_caption=True
        story.append(para)
    target=path.with_suffix('.pdf')
    doc=SimpleDocTemplate(str(target),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=43,bottomMargin=52,title='NT-BE / X2-omega: '+('Supplementary Information' if 'Supplementary' in path.name else 'Technical Note'),author='Sho Miyazaki',pageCompression=1,invariant=1)
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(target)
if __name__=='__main__':
    render(ROOT/'manuscript/Technical_Note_v1.1.0_rc1.md');render(ROOT/'supplement/Supplementary_Information_v1.1.0_rc1.md')
