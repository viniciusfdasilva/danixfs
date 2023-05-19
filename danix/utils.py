import os
from settings import MAIN_REPO, MAIN_DIR, BASE_DIR

def separate(path):
    list_path = path.split(" ")

    environment_path = None
    environment_uuid = None
    host_path        = None
    environent_is_first = False

    if len(list_path) >= 2:

        if list_path[1]:
            if str(list_path[1]).__contains__(":"):

                environment_uuid = list_path[1].split(":")[0]
                environment_path = list_path[1].split(":")[1]

            else:
                host_path = list_path[1]

        if list_path[0]:

            if str(list_path[0]).__contains__(":"):

                environent_is_first = True
                environment_uuid = list_path[0].split(":")[0]
                environment_path = list_path[0].split(":")[1]

            else:
                host_path = list_path[0]
                
    return environent_is_first, environment_uuid, environment_path, host_path

def check_create_dir():
    mainrepo_resp = os.system(f"cd {MAIN_REPO} >/dev/null 2>&1")
    snapshot_resp = os.system(f" cd {MAIN_REPO}.snapshots >/dev/null 2>&1")

    return True if mainrepo_resp == 0 and snapshot_resp == 0 else False

def check_create_db():
    return True if os.system(f"cat {MAIN_DIR}/db/db.sqlite3 >/dev/null 2>&1") == 0 else False

def check_create_dotenv():
    return True if os.system(f"cat {BASE_DIR}/danix/.env >/dev/null 2>&1") == 0 else False

@staticmethod
def check_system_configuration():

    check_dir_resp = check_create_dir()
    check_db_resp  = check_create_db()
    check_env_resp = check_create_dotenv()

    return check_dir_resp and check_db_resp and check_env_resp

@staticmethod
def print_footer():
    print("================================================================================================================================================")

@staticmethod
def get_size_in_mb_or_gb(size_str):

    try:

        size = int(size_str.replace("M","").replace(",","."))
    
        if size >= 1000:

            return f"{round(size/1000, 1)}GB"
        elif size <= 100:

            return size_str + "B "

    except Exception:
        return size_str.replace(",",".") + "B"
       
    return size_str + "B"

@staticmethod
def print_snapshot_list_header():
    print("================================================================================================================================================")
    print("|            SNAPSHOT NAME             |          ENVIRONMENT NAME            |          CREATED       |     LAST SNAPSHOT     |    SIZE       |")
    print("|==============================================================================================================================================|")

@staticmethod
def print_environment_list_header():
    print("================================================================================================================================================")
    print("|  ENVIRONMENT NAME  |  TEMPLATE  |       CREATED         |            SUBSYSTEM NAME            |      IMAGE     |      STATUS   |    SIZE    |")
    print("|==============================================================================================================================================|")

@staticmethod
def check_equal_sentence(left_expression, right_expression):
    return left_expression == right_expression

@staticmethod
def check_not_equal_sentence(left_expression, right_expression):
    return left_expression == right_expression

@staticmethod
def is_unique_database_tuple(model_queryset):

    if model_queryset.count() == 0:
        return Exception
    
    return True if model_queryset.count() == 1 else False

@staticmethod
def get_message(message, is_finishprogram, finish_status_code):
    
    print(message)

    if is_finishprogram:
        exit(finish_status_code)
    
def is_root():
    return True if os.geteuid() == 0 else False