from listAndDictOperations import *
import numpy as np

def within_one_week(fromDate, toDate):
    if toDate<fromDate:
        return False
    time_delta = toDate - fromDate
    return time_delta.days < 7

def remove_free_trial_cancels(data,paid_students):
    new_data = []
    for row in data:
        if row['account_key'] in paid_students:
            new_data.append(row)
    return new_data

def get_udacity_test_account_set(data):
    s = set()
    for row in data:
        if row['is_udacity']:
            s.add(row['account_key'])
    return s

def remove_udacity_test_accounts(data,udacity_account_set):
    new_data = []
    for row in data:
        if row['account_key'] not in udacity_account_set:
            new_data.append(row)
    return new_data

# assumption : student who have been present for more than 7 days are considered paid students
def get_paid_students_dict(non_udacity_enrollments):
    paid_students = {}
    for e in non_udacity_enrollments:
        if not e['is_canceled'] or e['days_to_cancel'] > 7:
            account_key = e['account_key']
            enrollment_date = e['join_date']

            if (account_key not in paid_students or \
                            enrollment_date > paid_students[account_key]):
                paid_students[account_key] = enrollment_date
    return paid_students

def group_values_by_account(engagement_by_account,dataField):
    group_dict = {}
    for key,value in engagement_by_account.items():
        group_dict[key] = get_sum_byField(value,dataField)
    return group_dict

def group_no_of_valid_rows_by_account(engagement_by_account,dataField):
    group_dict = {}
    for key,value in engagement_by_account.items():
        group_dict[key] = get_rowcount_with_field_greater_than_zero(value,'num_courses_visited')
    return group_dict

def get_incorrect_accounts(total_engagement_by_account):
    incorrect_accounts = {}
    for key, value in total_engagement_by_account.items():
        if value > 7*24*60:
            incorrect_accounts[key] = value
    return incorrect_accounts

def get_proj_completion_dict(data,lessonsKeys):
    passed_dict = {}
    for row in data:
        lessonKey = row['lesson_key']
        rating = row['assigned_rating']
        if lessonKey in lessonsKeys and (rating == 'PASSED' or rating == 'DISTINCTION'):
                passed_dict[row['account_key']]= row['completion_date']
    return passed_dict

def get_passing_engagementList(data,passed_dict, isPassed):
    l = list()
    for key, value in data.items():
        if isPassed and key in passed_dict:
            l.extend(value)
        elif not isPassed and key not in passed_dict:
            l.extend(value)
    return l








