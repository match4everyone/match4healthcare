
from faker import Faker
import uuid, json
import random
from random import randint
from datetime import datetime, timedelta
#from mapview.utils import get_plzs
import csv
plzs = {}
with open("mapview/PLZ.tab", encoding='utf-8') as tsvfile:
  reader = csv.DictReader(tsvfile, dialect='excel-tab')
  for row in reader:
      plzs[row["plz"]] = (float(row["lon"]), float(row["lat"]), row["Ort"])

german_fake = Faker(['de_DE'])
multikulti_fake = Faker(['de_DE', 'es_ES', 'en_GB', 'ar_SA'])
true_false = [True, False]
big_city_plzs = ['01067','01069','01097','01099','01109','01127','01129','01139','01157','01159','01169','01187','01189','01217','01219','01237','01239','01257','01259','01277','01279','01307','01309','01324','01326','04103','04105','04107','04109','04129','04155','04157','04158','04159','04177','04178','04179','04205','04207','04209','04229','04249','04275','04277','04279','04288','04289','04299','04315','04316','04317','04318','04328','04329','04347','04349','04356','04357','06108','06110','06112','06114','06116','06118','06120','06122','06124','06126','06128','06130','06132','10115','10117','10119','10178','10179','10243','10245','10247','10249','10315','10317','10318','10319','10365','10367','10369','10405','10407','10409','10435','10437','10439','10551','10553','10555','10557','10559','10585','10587','10589','10623','10625','10627','10629','10707','10709','10711','10713','10715','10717','10719','10777','10779','10781','10783','10785','10787','10789','10823','10825','10827','10829','10961','10963','10965','10967','10969','10997','10999','12043','12045','12047','12049','12051','12053','12055','12057','12059','12099','12101','12103','12105','12107','12109','12157','12159','12161','12163','12165','12167','12169','12203','12205','12207','12209','12247','12249','12277','12279','12305','12307','12309','12347','12349','12351','12353','12355','12357','12359','12435','12437','12439','12459','12487','12489','12524','12526','12527','12529','12555','12557','12559','12587','12589','12619','12621','12623','12625','12627','12629','12679','12681','12683','12685','12687','12689','13051','13053','13055','13057','13059','13086','13088','13089','13125','13127','13129','13156','13158','13159','13187','13189','13347','13349','13351','13353','13355','13357','13359','13403','13405','13407','13409','13435','13437','13439','13465','13467','13469','13503','13505','13507','13509','13581','13583','13585','13587','13589','13591','13593','13595','13597','13599','13627','13629','14050','14052','14053','14055','14057','14059','14089','14109','14129','14163','14165','14167','14169','14193','14195','14197','14199','15230','15232','15234','15236','18055','18057','18059','18069','18106','18107','18109','18119','18146','18147','24937','24939','24941','24943','24944','39104','39106','39108','39110','39112','39114','39116','39118','39120','39122','39124','39126','39128','39130','39221','42103','42105','42107','42109','42111','42113','42115','42117','42119','42275','42277','42279','42281','42283','42285','42287','42289','42327','42329','42349','42369','42389','42399','44135','44137','44139','44141','44143','44145','44147','44149','44225','44227','44229','44263','44265','44267','44269','44287','44289','44309','44319','44328','44329','44339','44357','44359','44369','44379','44388','48143','48145','48147','48149','48151','48153','48155','48157','48159','48161','48163','48165','48167','50667','50668','50670','50672','50674','50676','50677','50678','50679','50733','50735','50737','50739','50765','50767','50769','50823','50825','50827','50829','50858','50859','50931','50933','50935','50937','50939','50968','50969','50996','50997','50999','51061','51063','51065','51067','51069','51103','51105','51107','51109','51143','51145','51147','51149','53111','53113','53115','53117','53119','53121','53123','53125','53127','53129','53173','53175','53177','53179','53225','53227','53229','60385','60386','60388','60435','60437','60438','66111','66113','66115','66117','66119','66121','66123','66125','66126','66127','66128','66129','66130','66131','66132','66133','70173','70174','70176','70178','70180','70182','70184','70186','70188','70190','70191','70192','70193','70195','70197','70199','70327','70329','70372','70374','70376','70378','70435','70437','70439','70469','70499','70563','70565','70567','70569','70597','70599','70619','70629','80331','80333','80335','80336','80337','80339','80469','80538','80539','80634','80636','80637','80638','80639','80686','80687','80689','80796','80797','80798','80799','80801','80802','80803','80804','80805','80807','80809','80933','80935','80937','80939','80992','80993','80995','80997','80999','81241','81243','81245','81247','81249','81369','81371','81373','81375','81377','81379','81475','81476','81477','81479','81539','81541','81543','81545','81547','81549','81667','81669','81671','81673','81675','81677','81679','81735','81737','81739','81825','81827','81829','81925','81927','81929',]

fixture_start = """
[
    {
        "model": "contenttypes.contenttype",
        "pk": 1,
        "fields": {
            "app_label": "admin",
            "model": "logentry"
        }
    },
    {
        "model": "contenttypes.contenttype",
        "pk": 2,
        "fields": {
            "app_label": "auth",
            "model": "permission"
        }
    },
    {
        "model": "contenttypes.contenttype",
        "pk": 3,
        "fields": {
            "app_label": "auth",
            "model": "group"
        }
    },
    {
        "model": "contenttypes.contenttype",
        "pk": 4,
        "fields": {
            "app_label": "auth",
            "model": "user"
        }
    },
    {
        "model": "contenttypes.contenttype",
        "pk": 5,
        "fields": {
            "app_label": "contenttypes",
            "model": "contenttype"
        }
    },
    {
        "model": "contenttypes.contenttype",
        "pk": 6,
        "fields": {
            "app_label": "sessions",
            "model": "session"
        }
    },
    {
        "model": "contenttypes.contenttype",
        "pk": 7,
        "fields": {
            "app_label": "iamstudent",
            "model": "student"
        }
    },
    {
        "model": "contenttypes.contenttype",
        "pk": 8,
        "fields": {
            "app_label": "iamstudent",
            "model": "berufsausbildung"
        }
    },
    {
        "model": "contenttypes.contenttype",
        "pk": 9,
        "fields": {
            "app_label": "ineedstudent",
            "model": "hospital"
        }
    },
"""

fixture_end = """

    {
        "model": "auth.permission",
        "pk": 1,
        "fields": {
            "name": "Can add log entry",
            "content_type": 1,
            "codename": "add_logentry"
        }
    },
    {
        "model": "auth.permission",
        "pk": 2,
        "fields": {
            "name": "Can change log entry",
            "content_type": 1,
            "codename": "change_logentry"
        }
    },
    {
        "model": "auth.permission",
        "pk": 3,
        "fields": {
            "name": "Can delete log entry",
            "content_type": 1,
            "codename": "delete_logentry"
        }
    },
    {
        "model": "auth.permission",
        "pk": 4,
        "fields": {
            "name": "Can view log entry",
            "content_type": 1,
            "codename": "view_logentry"
        }
    },
    {
        "model": "auth.permission",
        "pk": 5,
        "fields": {
            "name": "Can add permission",
            "content_type": 2,
            "codename": "add_permission"
        }
    },
    {
        "model": "auth.permission",
        "pk": 6,
        "fields": {
            "name": "Can change permission",
            "content_type": 2,
            "codename": "change_permission"
        }
    },
    {
        "model": "auth.permission",
        "pk": 7,
        "fields": {
            "name": "Can delete permission",
            "content_type": 2,
            "codename": "delete_permission"
        }
    },
    {
        "model": "auth.permission",
        "pk": 8,
        "fields": {
            "name": "Can view permission",
            "content_type": 2,
            "codename": "view_permission"
        }
    },
    {
        "model": "auth.permission",
        "pk": 9,
        "fields": {
            "name": "Can add group",
            "content_type": 3,
            "codename": "add_group"
        }
    },
    {
        "model": "auth.permission",
        "pk": 10,
        "fields": {
            "name": "Can change group",
            "content_type": 3,
            "codename": "change_group"
        }
    },
    {
        "model": "auth.permission",
        "pk": 11,
        "fields": {
            "name": "Can delete group",
            "content_type": 3,
            "codename": "delete_group"
        }
    },
    {
        "model": "auth.permission",
        "pk": 12,
        "fields": {
            "name": "Can view group",
            "content_type": 3,
            "codename": "view_group"
        }
    },
    {
        "model": "auth.permission",
        "pk": 13,
        "fields": {
            "name": "Can add user",
            "content_type": 4,
            "codename": "add_user"
        }
    },
    {
        "model": "auth.permission",
        "pk": 14,
        "fields": {
            "name": "Can change user",
            "content_type": 4,
            "codename": "change_user"
        }
    },
    {
        "model": "auth.permission",
        "pk": 15,
        "fields": {
            "name": "Can delete user",
            "content_type": 4,
            "codename": "delete_user"
        }
    },
    {
        "model": "auth.permission",
        "pk": 16,
        "fields": {
            "name": "Can view user",
            "content_type": 4,
            "codename": "view_user"
        }
    },
    {
        "model": "auth.permission",
        "pk": 17,
        "fields": {
            "name": "Can add content type",
            "content_type": 5,
            "codename": "add_contenttype"
        }
    },
    {
        "model": "auth.permission",
        "pk": 18,
        "fields": {
            "name": "Can change content type",
            "content_type": 5,
            "codename": "change_contenttype"
        }
    },
    {
        "model": "auth.permission",
        "pk": 19,
        "fields": {
            "name": "Can delete content type",
            "content_type": 5,
            "codename": "delete_contenttype"
        }
    },
    {
        "model": "auth.permission",
        "pk": 20,
        "fields": {
            "name": "Can view content type",
            "content_type": 5,
            "codename": "view_contenttype"
        }
    },
    {
        "model": "auth.permission",
        "pk": 21,
        "fields": {
            "name": "Can add session",
            "content_type": 6,
            "codename": "add_session"
        }
    },
    {
        "model": "auth.permission",
        "pk": 22,
        "fields": {
            "name": "Can change session",
            "content_type": 6,
            "codename": "change_session"
        }
    },
    {
        "model": "auth.permission",
        "pk": 23,
        "fields": {
            "name": "Can delete session",
            "content_type": 6,
            "codename": "delete_session"
        }
    },
    {
        "model": "auth.permission",
        "pk": 24,
        "fields": {
            "name": "Can view session",
            "content_type": 6,
            "codename": "view_session"
        }
    },
    {
        "model": "auth.permission",
        "pk": 25,
        "fields": {
            "name": "Can add student",
            "content_type": 7,
            "codename": "add_student"
        }
    },
    {
        "model": "auth.permission",
        "pk": 26,
        "fields": {
            "name": "Can change student",
            "content_type": 7,
            "codename": "change_student"
        }
    },
    {
        "model": "auth.permission",
        "pk": 27,
        "fields": {
            "name": "Can delete student",
            "content_type": 7,
            "codename": "delete_student"
        }
    },
    {
        "model": "auth.permission",
        "pk": 28,
        "fields": {
            "name": "Can view student",
            "content_type": 7,
            "codename": "view_student"
        }
    },
    {
        "model": "auth.permission",
        "pk": 29,
        "fields": {
            "name": "Can add berufsausbildung",
            "content_type": 8,
            "codename": "add_berufsausbildung"
        }
    },
    {
        "model": "auth.permission",
        "pk": 30,
        "fields": {
            "name": "Can change berufsausbildung",
            "content_type": 8,
            "codename": "change_berufsausbildung"
        }
    },
    {
        "model": "auth.permission",
        "pk": 31,
        "fields": {
            "name": "Can delete berufsausbildung",
            "content_type": 8,
            "codename": "delete_berufsausbildung"
        }
    },
    {
        "model": "auth.permission",
        "pk": 32,
        "fields": {
            "name": "Can view berufsausbildung",
            "content_type": 8,
            "codename": "view_berufsausbildung"
        }
    },
    {
        "model": "auth.permission",
        "pk": 33,
        "fields": {
            "name": "Can add hospital",
            "content_type": 9,
            "codename": "add_hospital"
        }
    },
    {
        "model": "auth.permission",
        "pk": 34,
        "fields": {
            "name": "Can change hospital",
            "content_type": 9,
            "codename": "change_hospital"
        }
    },
    {
        "model": "auth.permission",
        "pk": 35,
        "fields": {
            "name": "Can delete hospital",
            "content_type": 9,
            "codename": "delete_hospital"
        }
    },
    {
        "model": "auth.permission",
        "pk": 36,
        "fields": {
            "name": "Can view hospital",
            "content_type": 9,
            "codename": "view_hospital"
        }
    }
]
"""

def random_plz():
    return random.choice(list(plzs.keys()))

def big_city_plz():
    return random.choice(big_city_plzs)

def generate_student(number, plz_function):
    random_time = (datetime.now() - timedelta(days=randint(0,40), hours=randint(0,23), minutes=randint(0,59))).strftime("%Y-%m-%dT%H:%M:%S.%f")[0:-3] + 'Z'
    random_start_date = (datetime.now() + timedelta(days=randint(0,160), hours=randint(0,23), minutes=randint(0,59))).strftime("%Y-%m-%d")
    student_dict = {
        'uuid': str(uuid.uuid4()),
        'registration_date': random_time,
        'plz': plz_function(),
        'email': str(randint(0,10000)) + german_fake.email(),
        'semester': randint(0,16),
        'immatrikuliert': true_false[randint(0,1)],
        'availability_start': random_start_date,
        'braucht_bezahlung': randint(1,3),
        'ba_arzt': randint(1,3),
        'ba_krankenpflege': randint(1,3),
        'ba_pflegehilfe': randint(1,3),
        'ba_anaesthesiepflege': randint(1,3),
        'ba_intensivpflege': randint(1,3),
        'ba_ota': randint(1,3),
        'ba_mfa': randint(1,3),
        'ba_mta_lta': randint(1,3),
        'ba_rta': randint(1,3),
        'ba_rettungssanitaeter': randint(1,3),
        'ba_kinderbetreuung': randint(1,3),
        'ba_hebamme': randint(1,3),
        'ba_sprechstundenhilfe': randint(1,3),
        'ba_labortechnische_assistenz': randint(1,3),
        'ba_famulatur': randint(0,3),
        'ba_pflegepraktika': randint(0,3),
        'ba_fsj_krankenhaus': randint(0,9),
        'skill_coronascreening': randint(1,3),
        'skill_pflegeunterstuetzung': randint(1,3),
        'skill_transportdienst': randint(1,3),
        'skill_kinderbetreuung': randint(1,3),
        'skill_labortaetigkeiten': randint(1,3),
        'skill_drkblutspende': randint(1,3),
        'skill_hotline': randint(1,3),
        'skill_abstriche': randint(1,3),
        'skill_patientenpflege': randint(1,3),
        'skill_patientenlagerung': randint(1,3),
        'skill_opassistenz': randint(1,3),
        'skill_blutentnahmedienst': randint(1,3),
        'skill_anrufe': randint(1,3),
        'skill_infektionsnachverfolgung': randint(1,3),
        'skill_patientenaufnahme': randint(1,3),
        'skill_edvkenntnisse': randint(1,3),
        'skill_zugaengelegen': randint(1,3),
        'skill_arztbriefeschreiben': randint(1,3),
        'skill_blutkulturenabnehmen': randint(1,3),
        'skill_infusionenmischen': randint(1,3),
        'skill_ekgschreiben': randint(1,3),
        'skill_ultraschall': randint(1,3),
        'skill_bgas': randint(1,3),
        'skill_beatmungsgeraetebedienen': randint(1,3)
    }
    student_json = json.dumps(student_dict)

    string = ''
    string += '{"model": "iamstudent.student", "pk": '
    string += str(number)
    string += ', "fields": '
    string += student_json
    string += '},'

    return string

def generate_hospital(number, plz_function):
    random_time = (datetime.now() - timedelta(days=randint(0,40), hours=randint(0,23), minutes=randint(0,59))).strftime("%Y-%m-%dT%H:%M:%S.%f")[0:-3] + 'Z'
    #random_start_date = (datetime.now() + timedelta(days=randint(0,160), hours=randint(0,23), minutes=randint(0,59))).strftime("%Y-%m-%d")
    hospital_dict = {
        'email': german_fake.email(),
        'sonstige_infos': german_fake.text(),
        'ansprechpartner': multikulti_fake.name(),
        'telefon': german_fake.phone_number(),
        'firmenname': german_fake.company(),
        'plz': plz_function(),
        'uuid': str(uuid.uuid4()),
        'registration_date': random_time,
    }
    hospital_json = json.dumps(hospital_dict)

    string = ''
    string += '{"model": "ineedstudent.hospital", "pk": '
    string += str(number)
    string += ', "fields": '
    string += hospital_json
    string += '},'
    return string

fixture = ''
fixture += fixture_start

for i in range(10000):
    fixture += generate_student(i+1, big_city_plz)

for i in range(2000):
    fixture += generate_student(i+10001, random_plz)

for i in range(20):
    fixture += generate_hospital(i+1, big_city_plz)

for i in range(10):
    fixture += generate_hospital(i+21, random_plz)

fixture += fixture_end

with open("fixture.json", "w") as f:
    f.write(fixture)