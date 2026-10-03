"""Shared filename convention for every resume and future resume renderer."""
import re
from datetime import datetime

PREFIX = 'PRABIR_BERA_MAR_TECH_ASSOCIATE_MANAGER_12_YEARS_PUNE_'
MONTHS = ('JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC')
FILENAME_JS = """function resumeFileName(date=new Date()){const months=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];return 'PRABIR_BERA_MAR_TECH_ASSOCIATE_MANAGER_12_YEARS_PUNE_'+months[date.getMonth()]+date.getFullYear();}"""

def resume_filename(date=None):
    date = date or datetime.now()
    return PREFIX + MONTHS[date.month - 1] + str(date.year)

def apply_resume_naming(source):
    """Embed the naming rule so downloaded HTML also works offline."""
    source = re.sub(r'<title>.*?</title>', '<title>' + resume_filename() + '</title>', source, count=1, flags=re.S)
    script = '<script id="resume-filename-policy">' + FILENAME_JS + """
function updateResumeFilename(){document.title=resumeFileName();}
updateResumeFilename();
window.addEventListener('beforeprint',updateResumeFilename);
window.addEventListener('pageshow',updateResumeFilename);
window.addEventListener('focus',updateResumeFilename);
</script>"""
    source = re.sub(r'<script id="resume-filename-policy">.*?</script>', '', source, flags=re.S)
    return source.replace('</head>',script+'</head>',1)
