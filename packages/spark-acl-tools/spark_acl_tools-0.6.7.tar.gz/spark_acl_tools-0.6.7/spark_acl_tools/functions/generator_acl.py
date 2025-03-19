import os
import shutil
import sys
from datetime import datetime

import pandas as pd
from spark_dataframe_tools import get_color_b

pd.options.mode.copy_on_write = True


def get_dataframe_catalog_nivel():
    df_catalogo_nivel = [
        {"CODE": "01", "DESC": "DAAS PERU SPARK", "SHOR_NAME": "SPARK", "DEFAULT": "YES"},
        {"CODE": "02", "DESC": "DAAS PERU MONITORING USER", "SHOR_NAME": "MONITORING USER", "DEFAULT": "YES"},
        {"CODE": "04", "DESC": "DAAS PERU EGRESSION DECRYPTION", "SHOR_NAME": "EGRESSION DECRYPTION", "DEFAULT": "YES"},
        {"CODE": "15", "DESC": "DAAS PERU DATAPROC USER READ", "SHOR_NAME": "DATAPROC USER READ", "DEFAULT": "YES"},
        {"CODE": "21", "DESC": "DAAS PERU DATAPROC USER", "SHOR_NAME": "DATAPROC USER", "DEFAULT": "YES"},
        {"CODE": "26", "DESC": "DAAS PERU DEVELOPER", "SHOR_NAME": "DEVELOPER", "DEFAULT": "NO"},
        {"CODE": "27", "DESC": "DAAS PERU DATA ARCHITECT", "SHOR_NAME": "DATA ARCHITECT", "DEFAULT": "NO"},
        {"CODE": "28", "DESC": "DAAS PERU GDRIVE", "SHOR_NAME": "GDRIVE", "DEFAULT": "NO"},
        {"CODE": "29", "DESC": "DAAS PERU SANDBOX XDATA", "SHOR_NAME": "XDATA", "DEFAULT": "NO"},
        {"CODE": "30", "DESC": "DAAS PERU SANDBOX DATA SCIENTIST", "SHOR_NAME": "DATA SCIENTIST", "DEFAULT": "NO"},
        {"CODE": "31", "DESC": "DAAS PERU SANDBOX PROCESS MANAGER", "SHOR_NAME": "PROCESS MANAGER", "DEFAULT": "NO"},
        {"CODE": "32", "DESC": "DAAS PERU SANDBOX MICROSTRATEGY", "SHOR_NAME": "MICROSTRATEGY", "DEFAULT": "NO"},
        {"CODE": "33", "DESC": "DAAS PERU SANDBOX DISCOVERY", "SHOR_NAME": "DISCOVERY", "DEFAULT": "NO"},
        {"CODE": "34", "DESC": "DAAS PERU VBOX", "SHOR_NAME": "VBOX", "DEFAULT": "NO"},
        {"CODE": "35", "DESC": "DAAS PERU SANDBOX ADMIN", "SHOR_NAME": "SANDBOX ADMIN", "DEFAULT": "NO"},
        {"CODE": "36", "DESC": "DAAS PERU SANDBOX HISTORY SERVER", "SHOR_NAME": "HISTORY SERVER", "DEFAULT": "NO"},
        {"CODE": "37", "DESC": "DAAS PERU SANDBOX HISTORY SERVER3", "SHOR_NAME": "HISTORY SERVER3", "DEFAULT": "NO"},
        {"CODE": "38", "DESC": "DAAS PERU SANDBOX FILE EXPLORER", "SHOR_NAME": "FILE EXPLORER", "DEFAULT": "NO"},
        {"CODE": "39", "DESC": "DAAS PERU SANDBOX VISUALIZER", "SHOR_NAME": "SANDBOX VISUALIZADOR", "DEFAULT": "NO"},
        {"CODE": "40", "DESC": "DAAS PERU SANDBOX INTELLIGENCE INSTANCE", "SHOR_NAME": "INTELLIGENCE INSTANCE", "DEFAULT": "NO"},
        {"CODE": "41", "DESC": "DAAS PERU SANDBOX INTELLIGENCE SERVICE USER", "SHOR_NAME": "INTELLIGENCE USER", "DEFAULT": "NO"},
        {"CODE": "42", "DESC": "DAAS PERU SANDBOX MIGRATION", "SHOR_NAME": "MIGRATION", "DEFAULT": "NO"},
        {"CODE": "43", "DESC": "DAAS PERU SANDBOX ARGOS", "SHOR_NAME": "ARGOS", "DEFAULT": "YES"},
        {"CODE": "44", "DESC": "DAAS PERU SANDBOX PM PRODUCTIVE", "SHOR_NAME": "PM PRODUCTIVE", "DEFAULT": "YES"},
        {"CODE": "45", "DESC": "DAAS PERU SANDBOX OWNER", "SHOR_NAME": "SANDBOX OWNER", "DEFAULT": "YES"}
    ]
    df = pd.DataFrame(df_catalogo_nivel)
    return df


def get_catalog_nivel(description):
    description = str(description).upper().strip()

    df = get_dataframe_catalog_nivel()
    result = df[df['SHOR_NAME'] == description]

    rs = dict(CODE="", DESC="")
    try:
        rs['CODE'] = result['CODE'].iloc[0]
        rs['DESC'] = result['DESC'].iloc[0]
    except BaseException:
        rs["CODE"] = ""
        rs["DESC"] = ""
    return rs


def get_uuaa(project):
    project = str(project).lower().strip()
    rs = dict(UUAA_NAME="", UUAA_DESC="")

    if project.startswith(("project", "sandbox")):
        if project.startswith("project"):
            rs["UUAA_NAME"] = str(project.split(":")[1]).upper().strip()
            rs["UUAA_DESC"] = "PROJECT"
        else:
            rs["UUAA_NAME"] = str(project.split(" ")[1]).upper().strip()
            rs["UUAA_DESC"] = "SANDBOX"
        return rs
    else:
        return rs


def get_acl(path, uuaa_desc):
    path = str(path).lower().strip()
    uuaa_desc = str(uuaa_desc).upper().strip()
    path_split = path.split("/")
    path_target = str(path_split[4])
    path_target2 = str(path_split[3])

    rs = dict(ID_RECURSO="", TARGET_RECURSO="")
    if path_target == "app" and uuaa_desc == "PROJECT":
        uuaa_name = str(path_split[5])
        if len(uuaa_name) == 4:
            uuaa_name = uuaa_name
        else:
            uuaa_name = "NOT_UUAA"

        path_unique = "-".join(path_split[7:])
        if path_unique == f"dataproc-streaming":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}STRE"
        elif path_unique == f"dataproc-batch":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}BATC"
        elif path_unique == f"dataproc-resources":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RESO"
        elif path_unique == f"dataproc-resources-models":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RMO"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "data" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[5:])

        if len(path_split) > 6:
            uuaa_name = str(path_split[6])
        else:
            uuaa_name = str(path_split[5])

        if len(uuaa_name) == 4:
            uuaa_name = uuaa_name
        elif len(uuaa_name) == 2 and str(path_split[5] == "raw"):
            uuaa_name = uuaa_name
        elif uuaa_name == "sandboxes":
            uuaa_name = "KDIT"
        else:
            uuaa_name = "NOT_UUAA"

        if path_unique == f"sandboxes":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SAND"


        elif path_unique == f"raw-{uuaa_name}-refusals":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RRFL"
        elif path_unique == f"raw-{uuaa_name}-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RDAT"
        elif path_unique == f"raw-{uuaa_name}-schemas":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RSHM"
        elif path_unique == f"raw-{uuaa_name}-datatmp":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RDTM"
        elif path_unique == f"raw-{uuaa_name}-refusals-dq":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RRFD"
        elif path_unique == f"raw-{uuaa_name}-refusals-process":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RRPR"

        elif path_unique == f"raw-bg-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RBG"
        elif path_unique == f"raw-fm-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RFM"
        elif path_unique == f"raw-kn-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RKN"
        elif path_unique == f"raw-le-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RLE"
        elif path_unique == f"raw-mp-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RMP"
        elif path_unique == f"raw-pi-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RPI"
        elif path_unique == f"raw-rc-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RRC"
        elif path_unique == f"raw-sm-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RSM"
        elif path_unique == f"raw-ug-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RUG"

        elif path_unique == f"raw-external-datatmp":
            struct_acl = f"DAS_PE_DATM_REDTM"
        elif path_unique == f"raw-external-data":
            struct_acl = f"DAS_PE_DATM_REDT"
        elif path_unique == f"raw-external-schemas":
            struct_acl = f"DAS_PE_DATM_RESHM"


        elif path_unique == f"master-external-datatmp":
            struct_acl = f"DAS_PE_DATM_MEDTM"
        elif path_unique == f"master-dq-haas-t_kqpd_stats":
            struct_acl = f"DAS_PE_DATM_KQPDDQST"

        elif path_unique == f"master-data":
            struct_acl = f"DAS_PE_DATM_MDAT"
        elif path_unique == f"master-datatmp":
            struct_acl = f"DAS_PE_DATM_DTM"
        elif path_unique == f"master-dq":
            struct_acl = f"DAS_PE_DATM_MDQ"
        elif path_unique == f"master-{uuaa_name}-dq":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MDQ"
        elif path_unique == f"master-{uuaa_name}-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MDAT"
        elif path_unique == f"master-{uuaa_name}-data-":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MDAT"

        elif path_unique == f"master-{uuaa_name}-schemas":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MSHM"

        elif path_unique == f"master-{uuaa_name}-data-l1t":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}ML1T"
        elif path_unique == f"share-{uuaa_name}-datatmp":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SDTM"
        elif path_unique == f"master-{uuaa_name}-datatmp":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MDTM"
        elif path_unique == f"master-{uuaa_name}-refusals":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MRF"
        elif path_unique == f"master-{uuaa_name}-refusals-dq":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MRFD"

        elif path_unique == f"master-productsservices-pmol-data":
            struct_acl = f"DAS_PE_DATM_PRSEMDAT"
        elif path_unique == f"master-productsservices-pmol-dq":
            struct_acl = f"DAS_PE_DATM_PRSEMDQ"
        elif path_unique == f"master-productsservices-pmol-schemas":
            struct_acl = f"DAS_PE_DATM_PRSEMSHM"
        elif path_unique == f"master-productsservices-pmol-datatmp":
            struct_acl = f"DAS_PE_DATM_PRSEMDTM"
        elif path_unique == f"master-productsservices-pmol-dq-refusals":
            struct_acl = f"DAS_PE_DATM_PRSEMRFS"
        elif path_unique == f"master-productsservices-pmol-dq-stats":
            struct_acl = f"DAS_PE_DATM_PRSEMDQS"


        elif path_unique == f"master-{uuaa_name}-data-cross":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}CRS"
        elif path_unique == f"master-{uuaa_name}-data-customerinformation":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}CUI"
        elif path_unique == f"master-{uuaa_name}-data-engineering":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}ENG"
        elif path_unique == f"master-{uuaa_name}-data-finance":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}FIN"
        elif path_unique == f"master-{uuaa_name}-data-internalaudit":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}IAU"
        elif path_unique == f"master-{uuaa_name}-data-legalcompliance":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}LCP"
        elif path_unique == f"master-{uuaa_name}-data-logisticsmanagement":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}LGM"
        elif path_unique == f"master-{uuaa_name}-data-realestate":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}RLE"
        elif path_unique == f"master-{uuaa_name}-data-retailbusinessbanking":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}RBB"
        elif path_unique == f"master-{uuaa_name}-data-risk":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}RSK"
        elif path_unique == f"master-{uuaa_name}-data-talentculture":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}TCU"


        elif path_unique == f"raw-otros-data":
            struct_acl = f"DAS_PE_DATMOTHERDATA"
        elif path_unique == f"sandboxes-fina-data-projects-migracion_rorc":
            struct_acl = f"DAS_PE_DATMFINAMIGRA"
        elif path_unique == f"sandboxes-intc-targetting":
            struct_acl = f"DAS_PE_DATMINTCTARG"
        elif path_unique == f"sandboxes-vbox-historyserver":
            struct_acl = f"DAS_PE_DATMVBOXHIS"
        elif path_unique == f"others":
            struct_acl = f"DAS_PE_DATMOTHER"
        elif path_unique == f"others-khr1-datatmp-master":
            struct_acl = f"DAS_PE_DATMKHR1DTMM"
        elif path_unique == f"others-kpfm-datatmp-master":
            struct_acl = f"DAS_PE_DATMKPFM"
        elif path_unique in ("quarantine", "quarantine-"):
            struct_acl = f"DAS_PE_DATMQUARAN"

        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "in" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[5:])

        if len(path_split) == 8:
            uuaa_name = str(path_split[7])
        elif len(path_split) == 9:
            uuaa_name = str(path_split[8])
        else:
            uuaa_name = ""

        if len(uuaa_name) == 4:
            uuaa_name = uuaa_name
            uuaa_name2 = uuaa_name
        elif len(uuaa_name) == 2:
            uuaa_name = uuaa_name
            uuaa_name2 = uuaa_name[0:2]
        else:
            uuaa_name = "NOT_UUAA"
            uuaa_name2 = "NOT_UUAA"

        if path_unique == f"staging-datax":
            struct_acl = f"DAS_PE_DATM_INST"
        elif path_unique == f"staging-external":
            struct_acl = f"DAS_PE_DATM_INET"
        elif path_unique == f"staging-ratransmit-external":
            struct_acl = f"DAS_PE_DATM_INETR"
        elif path_unique == f"staging-ratransmit":
            struct_acl = f"DAS_PE_DATM_INR"
        elif path_unique == f"staging-datax-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INST"

        elif path_unique == f"staging-ratransmit-datio-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INDA"

        elif path_unique == f"staging-ratransmit-external-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INRA"

        elif path_unique == f"staging-ratransmit-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INRT"

        elif path_unique == f"staging-ratransmit-host-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INRH"

        elif path_unique == f"staging-ratransmit-host-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INHO"
        elif path_unique == f"staging-ratransmit-apx-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INAP"
        elif path_unique == f"staging-ratransmit-oracle-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INOR"
        elif path_unique == f"staging-tpt-teradata-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INTP"


        elif path_unique == f"staging-tpt-teradata-{uuaa_name2}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name2.upper()}INPI"
        elif path_unique == f"staging-ratransmit-host-{uuaa_name2}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name2.upper()}INHO"
        elif path_unique == f"staging-ratransmit-apx-{uuaa_name2}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name2.upper()}IN{uuaa_name2.upper()}"
        elif path_unique == f"staging-ratransmit-pwcv-{uuaa_name2}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name2.upper()}INPW"

        elif path_unique == f"staging-ratransmit-boo-risk-data-peba":
            struct_acl = f"DAS_PE_DATM_RABORSKP"
        elif path_unique == f"staging-ratransmit-boo-cs-data-peba":
            struct_acl = f"DAS_PE_DATM_RABOCSP"
        elif path_unique == f"staging-ratransmit-host-otros":
            struct_acl = f"DAS_PE_DATM_RAHOOTHE"
        elif path_unique == f"staging-ratransmit-kgov-seeker":
            struct_acl = f"DAS_PE_DATM_RAKGOVSE"
        elif path_unique == f"staging-ratransmit-lar-plar":
            struct_acl = f"DAS_PE_DATM_RALARPLA"

        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "logs" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[5:])
        if path_unique == f"historyserver":
            struct_acl = f"DAS_PE_DATM_LHS"
        elif path_unique == f"historyserver3":
            struct_acl = f"DAS_PE_DATM_LHS3"
        elif path_unique == f"historyserverspark3":
            struct_acl = f"DAS_PE_DATM_LHSSPK3"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "out" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[5:])
        if len(path_split) == 8:
            uuaa_name = str(path_split[7])
        elif len(path_split) == 7:
            uuaa_name = str("KECS")
        else:
            uuaa_name = "NOT_UUAA"

        if path_unique == f"staging-ratransmit-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}OUST"
        elif path_unique == f"staging-ratransmit":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}R"
        elif path_unique == f"staging-apx":
            struct_acl = f"DAS_PE_DATM_OUSTAP"
        elif path_unique == f"staging-host":
            struct_acl = f"DAS_PE_DATM_OUSTHO"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "argos-front" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[4:])
        if path_unique == f"argos-front-dcos-userland":
            struct_acl = f"DAS_PE_ARGF_DCOSUSER"
        elif path_unique == f"argos-front-jobs-report":
            struct_acl = f"DAS_PE_ARGF_JOBSREPO"
        elif path_unique == f"argos-front-jobs-status":
            struct_acl = f"DAS_PE_ARGF_JOBSSTAT"
        elif path_unique == f"argos-front-juanitor":
            struct_acl = f"DAS_PE_ARGF_JUANITOR"
        elif path_unique == f"argos-front-logs":
            struct_acl = f"DAS_PE_ARGF_LOGS"
        elif path_unique == f"argos-front-mesos-tasks":
            struct_acl = f"DAS_PE_ARGF_MESOSTAS"
        elif path_unique == f"argos-front-task-logs":
            struct_acl = f"DAS_PE_ARGF_TASKLOGS"
        elif path_unique == f"argos-front-tpt-logs":
            struct_acl = f"DAS_PE_ARGF_TPTLOGS"
        elif path_unique == f"argos-front-alerts":
            struct_acl = f"DAS_PE_ARGF_ALERTS"
        elif path_unique == f"argos-front-alerts-store":
            struct_acl = f"DAS_PE_ARGF_ALERTSST"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "dataproc-ui" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[4:])
        if path_unique == f"dataproc-ui":
            struct_acl = f"DAS_PE_DATM_DATAPRUI"
        elif path_unique == f"dataproc-ui-":
            struct_acl = f"DAS_PE_DATM_DATAPRUI"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "discovery" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[4:])
        if path_unique == f"discovery":
            struct_acl = f"DAS_PE_DATM_DISCOVER"
        elif path_unique == f"discovery-":
            struct_acl = f"DAS_PE_DATM_DISCOVER"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "microstrategy" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[4:])
        if path_unique == f"microstrategy":
            struct_acl = f"DAS_PE_DATM_MICRPSTR"
        elif path_unique == f"microstrategy-":
            struct_acl = f"DAS_PE_DATM_MICRPSTR"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "intelligence" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[5:])

        if len(path_split) == 8:
            uuaa_name = str(path_split[5])
        else:
            uuaa_name = "NOT_UUAA"

        if path_unique == f"in{uuaa_name.lower()}-analytic-users":
            struct_acl = f"DAS_PE_DATM_SINT{uuaa_name.upper()}"
        elif path_unique == f"{uuaa_name}-analytic-users":
            struct_acl = f"DAS_PE_DATM_S{uuaa_name.upper()}"
        elif path_unique == f"":
            struct_acl = f"DAS_PE_DATM_SINTG"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "sandbox" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[4:])
        if path_unique == f"sandbox":
            struct_acl = f"DAS_PE_DATM_SANDBOX"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()


    elif path_target == "in" and uuaa_desc == "SANDBOX":
        path_unique = "-".join(path_split[5:])

        if len(path_split) == 8:
            uuaa_name = str(path_split[7])
        elif len(path_split) == 9:
            uuaa_name = str(path_split[8])
        else:
            uuaa_name = ""

        if len(uuaa_name) == 4:
            uuaa_name = uuaa_name
            uuaa_name2 = uuaa_name
        elif len(uuaa_name) == 2:
            uuaa_name = uuaa_name
            uuaa_name2 = uuaa_name[0:2]
        else:
            uuaa_name = "NOT_UUAA"
            uuaa_name2 = "NOT_UUAA"

        if path_unique == f"staging-tpt-teradata-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INTP"
        elif path_unique == f"staging-tpt-teradata-{uuaa_name2}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name2.upper()}INPI"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()


    elif path_target == "out" and uuaa_desc == "SANDBOX":
        path_unique = "-".join(path_split[5:])
        if len(path_split) == 8:
            uuaa_name = str(path_split[7])
        elif len(path_split) == 7:
            uuaa_name = str("KECS")
        else:
            uuaa_name = "NOT_UUAA"

        if path_unique == f"staging-ratransmit-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}OUST"
        elif path_unique == f"staging-ratransmit":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}R"
        elif path_unique == f"staging-apx":
            struct_acl = f"DAS_PE_DATM_OUSTAP"
        elif path_unique == f"staging-host":
            struct_acl = f"DAS_PE_DATM_OUSTHO"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()


    elif path_target == "logs" and uuaa_desc == "SANDBOX":
        path_unique = "-".join(path_split[5:])
        if path_unique == f"historyserver":
            struct_acl = f"DAS_PE_DATM_LHS"
        elif path_unique == f"historyserver3":
            struct_acl = f"DAS_PE_DATM_LHS3"
        elif path_unique == f"historyserverspark3":
            struct_acl = f"DAS_PE_DATM_LHSSPK3"
        else:
            struct_acl = ""

        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "intelligence" and uuaa_desc == "SANDBOX":
        path_unique = "-".join(path_split[5:])

        if len(path_split) == 8:
            uuaa_name = str(path_split[5])
        else:
            uuaa_name = "NOT_UUAA"

        if path_unique == f"in{uuaa_name.lower()}-analytic-users":
            struct_acl = f"DAS_PE_DATM_SINT{uuaa_name.upper()}"
        elif path_unique == f"{uuaa_name}-analytic-users":
            struct_acl = f"DAS_PE_DATM_S{uuaa_name.upper()}"
        elif path_unique == f"":
            struct_acl = f"DAS_PE_DATM_SINTG"

        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "data" and uuaa_desc == "SANDBOX":
        path_unique = "-".join(path_split[5:])
        uuaa_name = "NOT_UUAA"
        table_name = ""
        table_sp = ""

        if len(path_split[5:]) == 3:
            uuaa_name = str(path_split[6])
        elif len(path_split[5:]) == 4:
            uuaa_name = str(path_split[6])
        elif len(path_split[5:]) == 5:
            uuaa_name = str(path_split[6])
            table_name = str(path_split[8])
            table_sp = str("".join(table_name.split("_")[2:])[0:6]).upper()

        else:
            uuaa_name = "NOT_UUAA"
            table_name = ""
            table_sp = ""

        if len(uuaa_name) == 4:
            uuaa_name = uuaa_name

        if path_unique == f"sandboxes-{uuaa_name}-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SDAT"
        elif path_unique == f"sandboxes-{uuaa_name}-models":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SMDS"
        elif path_unique == f"sandboxes-{uuaa_name}-archived":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SAHV"
        elif path_unique == f"sandboxes-{uuaa_name}-xdata":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SXDT"
        elif path_unique == f"sandboxes-{uuaa_name}-historyserver":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SHS"
        elif path_unique == f"sandboxes-{uuaa_name}-upload":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SUPL"
        elif path_unique == f"others-{uuaa_name}-sandboxes-sauron":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SSAU"
        elif path_unique == f"sandboxes":
            struct_acl = f"DAS_PE_DATM_SSANBOX"
            
        elif path_unique == f"master-{uuaa_name}-refusals-dq":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MRFD"

        elif path_unique == f"sandboxes-risk-mk8f_info":
            struct_acl = f"DAS_PE_DATM_SRKMFIF"
        elif path_unique == f"sandboxes-mk8f-risk_info":
            struct_acl = f"DAS_PE_DATM_SMFRKIF"

        elif path_unique == f"master-dq":
            struct_acl = f"DAS_PE_DATM_MDQ"
        elif path_unique == f"master-{uuaa_name}-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MDAT"
        elif path_unique == f"master-{uuaa_name}-data-l1t":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}ML1T"
        elif path_unique == f"master-{uuaa_name}-data-l2":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}ML2"
        elif path_unique == f"master-{uuaa_name}-data-{table_name}-l3":
            struct_acl = f"DAS_PE_DATM_{table_sp.upper()}"

        elif path_unique == f"master-{uuaa_name}-data-cross-l1t":
            struct_acl = f"DAS_PE_DTM{uuaa_name.upper()}CRSL1T"
        elif path_unique == f"master-{uuaa_name}-data-customerinformation-l1t":
            struct_acl = f"DAS_PE_DTM{uuaa_name.upper()}CUIL1T"
        elif path_unique == f"master-{uuaa_name}-data-engineering-l1t":
            struct_acl = f"DAS_PE_DTM{uuaa_name.upper()}ENGL1T"
        elif path_unique == f"master-{uuaa_name}-data-finance-l1t":
            struct_acl = f"DAS_PE_DTM{uuaa_name.upper()}FINL1T"
        elif path_unique == f"master-{uuaa_name}-data-internalaudit-l1t":
            struct_acl = f"DAS_PE_DTM{uuaa_name.upper()}IAUL1T"
        elif path_unique == f"master-{uuaa_name}-data-legalcompliance-l1t":
            struct_acl = f"DAS_PE_DTM{uuaa_name.upper()}LCPL1T"
        elif path_unique == f"master-{uuaa_name}-data-logisticsmanagement-l1t":
            struct_acl = f"DAS_PE_DTM{uuaa_name.upper()}LGML1T"
        elif path_unique == f"master-{uuaa_name}-data-realestate-l1t":
            struct_acl = f"DAS_PE_DTM{uuaa_name.upper()}RLEL1T"
        elif path_unique == f"master-{uuaa_name}-data-retailbusinessbanking-l1t":
            struct_acl = f"DAS_PE_DTM{uuaa_name.upper()}RBBL1T"
        elif path_unique == f"master-{uuaa_name}-data-risk-l1t":
            struct_acl = f"DAS_PE_DTM{uuaa_name.upper()}RSKL1T"
        elif path_unique == f"master-{uuaa_name}-data-talentculture-l1t":
            struct_acl = f"DAS_PE_DTM{uuaa_name.upper()}TCUL1T"

        elif path_unique == f"master-{uuaa_name}-data-cross":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}CRS"
        elif path_unique == f"master-{uuaa_name}-data-customerinformation":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}CUI"
        elif path_unique == f"master-{uuaa_name}-data-engineering":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}ENG"
        elif path_unique == f"master-{uuaa_name}-data-finance":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}FIN"
        elif path_unique == f"master-{uuaa_name}-data-internalaudit":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}IAU"
        elif path_unique == f"master-{uuaa_name}-data-legalcompliance":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}LCP"
        elif path_unique == f"master-{uuaa_name}-data-logisticsmanagement":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}LGM"
        elif path_unique == f"master-{uuaa_name}-data-realestate":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}RLE"
        elif path_unique == f"master-{uuaa_name}-data-retailbusinessbanking":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}RBB"
        elif path_unique == f"master-{uuaa_name}-data-risk":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}RSK"
        elif path_unique == f"master-{uuaa_name}-data-talentculture":
            struct_acl = f"DAS_PE_DATM{uuaa_name.upper()}TCU"

        elif path_unique == f"raw-otros-data":
            struct_acl = f"DAS_PE_DATMOTHERDATA"
        elif path_unique == f"sandboxes-fina-data-projects-migracion_rorc":
            struct_acl = f"DAS_PE_DATMFINAMIGRA"
        elif path_unique == f"sandboxes-intc-targetting":
            struct_acl = f"DAS_PE_DATMINTCTARG"
        elif path_unique == f"sandboxes-vbox-historyserver":
            struct_acl = f"DAS_PE_DATMVBOXHIS"
        elif path_unique == f"others":
            struct_acl = f"DAS_PE_DATMOTHER"
        elif path_unique == f"others-khr1-datatmp-master":
            struct_acl = f"DAS_PE_DATMKHR1DTMM"
        elif path_unique == f"others-kpfm-datatmp-master":
            struct_acl = f"DAS_PE_DATMKPFM"
        elif path_unique in ("quarantine", "quarantine-"):
            struct_acl = f"DAS_PE_DATMQUARAN"
        elif path_unique == f"sandboxes-fina-intc_info":
            struct_acl = f"DAS_PE_DATMINTCINFO"
        elif path_unique == f"sandboxes-intc-fina_info":
            struct_acl = f"DAS_PE_DATMFINAINFO"
        else:
            struct_acl = ""

        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "argos-front" and uuaa_desc == "SANDBOX":
        path_unique = "-".join(path_split[4:])
        if path_unique == f"argos-front-dcos-userland":
            struct_acl = f"DAS_PE_ARGF_SDCOSUSE"
        elif path_unique == f"argos-front-jobs-report":
            struct_acl = f"DAS_PE_ARGF_SJOBSREP"
        elif path_unique == f"argos-front-jobs-status":
            struct_acl = f"DAS_PE_ARGF_SJOBSSTA"
        elif path_unique == f"argos-front-juanitor":
            struct_acl = f"DAS_PE_ARGF_SJUANITO"
        elif path_unique == f"argos-front-logs":
            struct_acl = f"DAS_PE_ARGF_SLOG"
        elif path_unique == f"argos-front-mesos-tasks":
            struct_acl = f"DAS_PE_ARGF_SMESOSTA"
        elif path_unique == f"argos-front-task-logs":
            struct_acl = f"DAS_PE_ARGF_STASKLOG"
        elif path_unique == f"argos-front-tpt-logs":
            struct_acl = f"DAS_PE_ARGF_STPTLOG"
        elif path_unique == f"argos-front-alerts":
            struct_acl = f"DAS_PE_ARGF_SALERT"
        elif path_unique == f"argos-front-alerts-store":
            struct_acl = f"DAS_PE_ARGF_SALERTSS"
        elif path_unique == f"argos-front-framelive-logs":
            struct_acl = f"DAS_PE_ARGF_SFRMELOG"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target2 == "services" and uuaa_desc == "SANDBOX":
        path_unique = "-".join(path_split[3:])
        if path_unique in ("services-sandbox", "services-sandbox-"):
            struct_acl = f"DAS_PE_SERV_SDSANBOX"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "resources" and uuaa_desc == "SANDBOX":
        path_unique = "-".join(path_split[4:])
        uuaa_name = str(path_split[5])
        if len(uuaa_name) == 4:
            uuaa_name = uuaa_name
        else:
            uuaa_name = "NOT_UUAA"

        if path_unique == f"resources-{uuaa_name}-pipelines":
            struct_acl = f"DAS_PE_RESC_{uuaa_name.upper()}PIPE"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target2 == "discovery" and uuaa_desc == "SANDBOX":
        path_unique = "-".join(path_split[3:])
        if path_unique in ("discovery", "discovery-"):
            struct_acl = f"DAS_PE_DATM_SDISCOVE"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target2.upper()

    elif path_target2 == "microstrategy" and uuaa_desc == "SANDBOX":
        path_unique = "-".join(path_split[3:])
        if path_unique in ("microstrategy", "microstrategy-"):
            struct_acl = f"DAS_PE_DATM_SMICRPST"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target2.upper()
    else:
        rs["ID_RECURSO"] = ""
        rs["TARGET_RECURSO"] = ""

    return rs


def classification_uuaa_name(project):
    project = str(project).lower().strip()
    if project not in ("", None):
        id_uuaa = get_uuaa(project)
        return id_uuaa["UUAA_NAME"]
    else:
        return ""


def classification_uuaa_desc(project):
    project = str(project).lower().strip()
    if project not in ("", None):
        id_uuaa = get_uuaa(project)
        return id_uuaa["UUAA_DESC"]
    else:
        return ""


def classification_type_resource(permission):
    if permission == "R":
        return "DAAS RESOURCE READ ONLY"
    else:
        return "DAAS RESOURCE READ AND WRITE"


def classification_id_collective(description, group):
    description = str(description).lower()
    group = str(group).upper()
    if description.strip() in ('spark', 'egression decryption', 'monitoring user', 'dataproc user', 'vbox',
                               "developer", 'dataproc user read', 'data scientist', 'process manager', 'xdata',
                               'file explorer', 'discovery', 'microstrategy', 'argos', 'intelligence instance',
                               'pm productive', 'history server', 'sandbox owner', 'sandbox visualizador'):

        id_colectivo = f"D_{group[6:8]}{group[9:15]}"
        return id_colectivo
    else:
        return ""


def classification_name_collective(group):
    if group not in ("", None):
        nombre_colectivo = f"DAAS PERU {group.upper()}"
        return nombre_colectivo
    else:
        return ""


def classification_id_content(uuaa_name, uuaa_desc):
    if uuaa_name not in ("", None):
        if uuaa_name == "VBOX" or uuaa_desc == "SANDBOX":
            id_contenido = f"SAND{uuaa_name.upper()}"
        else:
            id_contenido = f"P{uuaa_name.upper()}"
        return id_contenido
    else:
        return ""


def classification_name_content(uuaa_name):
    if uuaa_name not in ("", None):
        nombre_contenido = f"DAAS PERU {uuaa_name.upper()}"
        return nombre_contenido
    else:
        return ""


def classification_id_nivel(uuaa_name, description):
    description = str(description).lower().strip()
    if uuaa_name not in ("", None):
        catalog_nivel = get_catalog_nivel(description)
        return catalog_nivel["CODE"]
    else:
        return ""


def classification_name_nivel(uuaa_name, description):
    description = str(description).lower().strip()
    if uuaa_name not in ("", None):
        catalog_nivel = get_catalog_nivel(description)
        return catalog_nivel["DESC"]
    else:
        return ""


def classification_id_resource(path_name, uuaa_desc):
    path_name = str(path_name).lower().strip()
    if path_name not in ("", None):
        acl_name = get_acl(path_name, uuaa_desc)
        return acl_name["ID_RECURSO"]
    else:
        return ""


def classification_target_resource(path_name, uuaa_desc):
    path_name = str(path_name).lower().strip()
    if path_name not in ("", None):
        acl_name = get_acl(path_name, uuaa_desc)
        return acl_name["TARGET_RECURSO"]
    else:
        return ""


def transformation_columns(df):
    df['UUAA_NAME'] = df.apply(lambda x: classification_uuaa_name(project=x["PROJECT"]), axis=1)
    df['UUAA_DESC'] = df.apply(lambda x: classification_uuaa_desc(project=x["PROJECT"]), axis=1)
    df['TARGET_RECURSO'] = df.apply(lambda x: classification_target_resource(path_name=x["PATH"], uuaa_desc=x["UUAA_DESC"]), axis=1)
    df['ID_RECURSO'] = df.apply(lambda x: classification_id_resource(path_name=x["PATH"], uuaa_desc=x["UUAA_DESC"]), axis=1)
    df['TIPO_RECURSO'] = df['PERMISSIONS'].apply(classification_type_resource)
    df['LONGITUD_RECURSO'] = df['ID_RECURSO'].apply(lambda x: len(str(x)))
    df['ID_COLECTIVO'] = df.apply(lambda x: classification_id_collective(description=x["DESCRIPTION"], group=x["GROUP"]), axis=1)
    df['NOMBRE_COLECTIVO'] = df.apply(lambda x: classification_name_collective(group=x["GROUP"]), axis=1)
    df['ID_CONTENIDO'] = df.apply(lambda x: classification_id_content(uuaa_name=x["UUAA_NAME"], uuaa_desc=x["UUAA_DESC"]), axis=1)
    df['NOMBRE_CONTENIDO'] = df.apply(lambda x: classification_name_content(uuaa_name=x["UUAA_NAME"]), axis=1)
    df['ID_NIVEL'] = df.apply(lambda x: classification_id_nivel(uuaa_name=x["UUAA_NAME"], description=x["DESCRIPTION"]), axis=1)
    df['NOMBRE_NIVEL'] = df.apply(lambda x: classification_name_nivel(uuaa_name=x["UUAA_NAME"], description=x["DESCRIPTION"]), axis=1)
    df['RECURSO_TIPORECURSO'] = df['ID_RECURSO'] + "-" + df["TIPO_RECURSO"]
    df['GROUP_PATH'] = df['GROUP'] + "-" + df["PATH"]
    df['IS_DUPLICATES_1'] = df['RECURSO_TIPORECURSO'].duplicated()
    df['IS_DUPLICATES_2'] = df['GROUP_PATH'].duplicated()
    df = df.sort_values(['GROUP'], ascending=[True])
    return df


def generate_profiling(file_excel=None):
    data = pd.read_excel(file_excel, sheet_name="ACLs_Envios_A_OFP", engine='openpyxl')
    df1 = data.iloc[:, 0:7]
    df1.columns = map(lambda x: str(x).strip().upper(), df1.columns)
    df1['TIPO'] = df1['TIPO'].apply(lambda x: x.upper())
    date_now = datetime.today().strftime('%Y%m%d%H%M')

    df_acl_create = df1[df1['TIPO'] == "CREAR"]
    df_acl_create = transformation_columns(df_acl_create)

    df_catalog_nivel = get_dataframe_catalog_nivel()
    df_catalog_nivel.loc[:, 'NOMBRE'] = df_catalog_nivel["DESC"]
    df_catalog_nivel.loc[:, 'DESCRIPCION'] = df_catalog_nivel["DESC"]
    df_catalog_nivel.loc[:, 'NRO MAX USUARIO'] = "0"
    df_catalog_nivel.loc[:, 'TOLERANCIA'] = "ACTIVA"

    df_contenido = df_acl_create[['ID_CONTENIDO', 'ID_NIVEL', 'NOMBRE_CONTENIDO', 'NOMBRE_NIVEL']]
    df_contenido = df_contenido.drop_duplicates().reset_index(drop=True)
    df_contenido = df_contenido.sort_values(['ID_CONTENIDO', 'ID_NIVEL'], ascending=[True, True])
    df_contenido['RANK'] = df_contenido[['ID_CONTENIDO']].rank(method='dense').astype(int)

    df_colectivo = df_acl_create[['ID_COLECTIVO', 'NOMBRE_COLECTIVO']]
    df_colectivo.loc[:, 'GESTOR RESPONSABLE COLECTIVO'] = "PAIS - PERU"
    df_colectivo.loc[:, 'DESCRIPCION COLECTIVO'] = df_colectivo["NOMBRE_COLECTIVO"]
    df_colectivo = df_colectivo.drop_duplicates().reset_index(drop=True)
    df_colectivo = df_colectivo.sort_values(['ID_COLECTIVO'], ascending=[True])

    df_recurso = df_acl_create[['ID_RECURSO', 'TIPO_RECURSO', 'PATH']]
    df_recurso.loc[:, 'NOMBRE AMBIENTE'] = "DATA AS SERVICE PERU"
    df_recurso.loc[:, 'NOMBRE RECURSO'] = df_recurso["PATH"]
    df_recurso.loc[:, 'NOMBRE RECURSO EXTENDIDO'] = " " + df_recurso["PATH"]
    df_recurso.loc[:, 'UUAA'] = "9993"
    del df_recurso["PATH"]
    df_recurso.columns = ["COD_RECURSO", "NOMBRE_TIPO_RECURSO", "NOMBRE_AMBIENTE", "NOMBRE_RECURSO", "NOMBRE_RECURSO_EXTENDIDO", "UUAA"]
    df_recurso = df_recurso.drop_duplicates().reset_index(drop=True)
    df_recurso = df_recurso.sort_values(['COD_RECURSO', 'NOMBRE_TIPO_RECURSO'], ascending=[True, True])

    df_recurso_pre_assigment = df_acl_create[['ID_CONTENIDO', 'ID_NIVEL', 'ID_RECURSO', 'TIPO_RECURSO']]
    df_recurso_pre_assigment.loc[:, 'AMBIENTE'] = "DATA AS SERVICE PERU"
    df_recurso_pre_assigment.loc[:, 'COD CONEXION'] = "MONO"
    df_recurso_pre_assigment.columns = ["COD_CONTENIDO", "COD_NIVEL", "COD_RECURSO", "TIPO_RECURSO", "AMBIENTE", "COD CONEXION"]
    df_recurso_pre_assigment = df_recurso_pre_assigment.drop_duplicates().reset_index(drop=True)
    df_recurso_pre_assigment = df_recurso_pre_assigment.sort_values(['COD_CONTENIDO', 'COD_NIVEL', 'COD_RECURSO'], ascending=[True, True, True])

    df_contenido_previous = df_acl_create[['ID_CONTENIDO', 'ID_NIVEL', 'ID_RECURSO', 'TIPO_RECURSO']]
    df_contenido_previous.loc[:, 'AMBIENTE'] = "DATA AS SERVICE PERU"
    df_contenido_previous.loc[:, 'COD CONEXION'] = "MONO"
    df_contenido_previous.loc[:, 'ENTORNO DESTINO'] = "E.PREVIOS"
    df_contenido_previous.columns = ["COD_CONTENIDO", "COD_NIVEL", "COD_RECURSO", "TIPO_RECURSO", "AMBIENTE", "COD CONEXION", "ENTORNO_DESTINO"]
    df_contenido_previous = df_contenido_previous.drop_duplicates().reset_index(drop=True)
    df_contenido_previous = df_contenido_previous.sort_values(['COD_CONTENIDO', 'COD_NIVEL', 'COD_RECURSO'], ascending=[True, True, True])

    df_contenido_production = df_acl_create[['ID_CONTENIDO', 'ID_NIVEL', 'ID_RECURSO', 'TIPO_RECURSO']]
    df_contenido_production.loc[:, 'AMBIENTE'] = "DATA AS SERVICE PERU"
    df_contenido_production.loc[:, 'COD CONEXION'] = "MONO"
    df_contenido_production.loc[:, 'ENTORNO DESTINO'] = "PRODUCCIÓN"
    df_contenido_production.columns = ["COD_CONTENIDO", "COD_NIVEL", "COD_RECURSO", "TIPO_RECURSO", "AMBIENTE", "COD CONEXION", "ENTORNO_DESTINO"]
    df_contenido_production = df_contenido_production.drop_duplicates().reset_index(drop=True)
    df_contenido_production = df_contenido_production.sort_values(['COD_CONTENIDO', 'COD_NIVEL', 'COD_RECURSO'], ascending=[True, True, True])

    df_colectivo_grupo = df_acl_create[['GROUP', 'ID_COLECTIVO', 'ID_CONTENIDO', 'ID_NIVEL', 'NOMBRE_CONTENIDO', 'NOMBRE_NIVEL', 'NOMBRE_COLECTIVO']]
    df_colectivo_grupo = df_colectivo_grupo.drop_duplicates().reset_index(drop=True)
    df_colectivo_grupo = df_colectivo_grupo.sort_values(['GROUP', 'ID_COLECTIVO', 'ID_CONTENIDO', 'ID_NIVEL'], ascending=[True, True, True, True])

    df_contenido_nivel_colectivo = df_acl_create[['ID_CONTENIDO', 'ID_NIVEL', 'ID_COLECTIVO', 'NOMBRE_CONTENIDO', 'NOMBRE_NIVEL', 'NOMBRE_COLECTIVO']]
    df_contenido_nivel_colectivo = df_contenido_nivel_colectivo.drop_duplicates().reset_index(drop=True)
    df_contenido_nivel_colectivo = df_contenido_nivel_colectivo.sort_values(['ID_CONTENIDO', 'ID_NIVEL', 'ID_COLECTIVO'], ascending=[True, True, True])

    try:
        df_acl_delete = df1[df1['TIPO'] == "ELIMINAR"]
        df_acl_delete = transformation_columns(df_acl_delete)
        df_recurso_pre_assigment_delete = df_acl_delete[['ID_CONTENIDO', 'ID_NIVEL', 'ID_RECURSO', 'TIPO_RECURSO']]
        df_recurso_pre_assigment_delete.loc[:, 'AMBIENTE'] = "DATA AS SERVICE PERU"
        df_recurso_pre_assigment_delete.loc[:, 'COD CONEXION'] = "MONO"
        df_recurso_pre_assigment_delete.columns = ["COD_CONTENIDO", "COD_NIVEL", "COD_RECURSO", "TIPO_RECURSO", "AMBIENTE", "COD CONEXION"]
        df_recurso_pre_assigment_delete = df_recurso_pre_assigment_delete.drop_duplicates().reset_index(drop=True)
        df_recurso_pre_assigment_delete = df_recurso_pre_assigment_delete.sort_values(['COD_CONTENIDO', 'COD_NIVEL', 'COD_RECURSO'], ascending=[True, True, True])

    except BaseException:
        df_acl_delete = None

    is_windows = sys.platform.startswith('win')
    path_directory = os.path.join("DIRECTORY_PROFILING")
    path_profiling = os.path.join(path_directory, f"profiling_acl_{date_now}.xlsx")

    if is_windows:
        path_profiling = path_profiling.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)

    writer = pd.ExcelWriter(f"{path_profiling}", engine="xlsxwriter")
    data.to_excel(writer, sheet_name="original", index=False)
    df_acl_create.to_excel(writer, sheet_name="create_processing", index=False)
    try:
        df_acl_delete.to_excel(writer, sheet_name="delete_processing", index=False)
    except BaseException:
        pass
    df_catalog_nivel.to_excel(writer, sheet_name="catalog_nivel", index=False)
    df_contenido.to_excel(writer, sheet_name="contenido", index=False)
    df_colectivo.to_excel(writer, sheet_name="colectivo", index=False)
    df_recurso.to_excel(writer, sheet_name="recurso", index=False)
    df_recurso_pre_assigment.to_excel(writer, sheet_name="recurso_preasignacion", index=False)
    df_contenido_previous.to_excel(writer, sheet_name="contenido_previous", index=False)
    df_contenido_production.to_excel(writer, sheet_name="contenido_production", index=False)
    df_colectivo_grupo.to_excel(writer, sheet_name="colectivo_grupo", index=False)
    df_contenido_nivel_colectivo.to_excel(writer, sheet_name="contenido_nivel_colectivo", index=False)
    try:
        df_recurso_pre_assigment_delete.to_excel(writer, sheet_name="delete_recurso_preasignacion", index=False)
    except BaseException:
        pass

    writer.close()
    print(get_color_b(f'Create file: {path_profiling}'))

    shutil.make_archive("DIRECTORY_PROFILING", "zip", "DIRECTORY_PROFILING")
    shutil.move("DIRECTORY_PROFILING.zip", f"{path_directory}.zip")
