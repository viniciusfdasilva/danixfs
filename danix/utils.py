import os

@staticmethod
def print_footer():
    print("================================================================================================================================================")


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