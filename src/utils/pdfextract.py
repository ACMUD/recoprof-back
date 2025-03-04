from PyPDF2 import PdfReader
import re


async def extract(file):
    reader = PdfReader(file)
    lines = [""]
    for page in reader.pages:
        for line in page.extract_text().split('\n'):
                if line[0].isnumeric() or line.startswith('ESPACIO ACADEMICO') or line.startswith('GRP.') or line.startswith('Cod.Espacio'):
                    lines.append(line)
                    continue
                lines[-1] += line

    for i in range(len(lines)):
        if 'POR ASIGNAR' in lines[i]:
            lines[i]=lines[i].replace('POR ASIGNAR','NONE 0')

    tmp = list(filter(lambda x: not x[-1].isnumeric() and x[0].isnumeric(), lines))

    data = "\n".join(tmp)

    PATRON = r'(\b\d+)([? A-z][A-z? ?:? ]+\d*)(LUNES|MARTES|MIERCOLES|JUEVES|VIERNES|SABADO|DOMINGO)([? ]\d+-\d+)([? A-z0-9]*\d+)([? A-z]*[ A-Z])'
    pattern = re.compile(PATRON)
    materiasProfesores = []

    for i in pattern.findall(data):
        codigo = int(i[0].strip())
        materia = i[1].strip()
        profesor = i[-1].strip()
        materiasProfesores.append((codigo, materia, profesor))
    
    nr = list(set(materiasProfesores))

    return nr


async def pdfextract(file):
    
    data = await extract(file)

    profs = {}
    for i in data:
        if i[2] not in profs:
            profs[i[2]] = []
        profs[i[2]].append(i[0])
    
    materias = list(set([(i[0],i[1]) for i in data]))

    return materias, profs