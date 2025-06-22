import os

class Settings:
    MAIN_BASE_URL = os.getenv('BASE_URL', 'https://www.uni-rostock.de')
    BSZ_BASE_URL = os.getenv('BSZ_BASE_URL', 'https://www.bsz.uni-rostock.de')
    QIS_BASE_URL = os.getenv('QIS_BASE_URL', 'https://lsf.uni-rostock.de')
    QIS_SEARCH_URL = f"{QIS_BASE_URL}/qisserver/rds?state=change&type=5&moduleParameter=veranstaltungSearch&nextdir=change&next=search.vm&subdir=veranstaltung&_form=display&function=search&clean=y&category=veranstaltung.search&navigationPosition=lectures%2Csearch&breadcrumb=searchLectures&topitem=lectures&subitem=search"