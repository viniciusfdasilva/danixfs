import os

@staticmethod
def check_equal_sentence(left_expression, right_expression):
    return left_expression == right_expression

@staticmethod
def check_not_equal_sentence(left_expression, right_expression):
    return left_expression == right_expression

@staticmethod
def is_unique_database_tuple(model_queryset):

    return True if model_queryset.count() == 1 else False

@staticmethod
def get_message(message, is_finishprogram, finish_status_code):
    
    print(message)

    if is_finishprogram:
        exit(finish_status_code)
    
def is_root():
    return True if os.geteuid() == 0 else False