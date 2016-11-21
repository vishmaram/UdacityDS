from csvReader import *
from fixDataType import *
from setOperations import *
from customMethods import *
from listAndDictOperations import *
import numpy as np

# Option 1: Csv can be list of lists
# Option2: Csv can be dictionariy

plt.interactive(False)

enrollments_filename = 'data/enrollments.csv'
engagement_filename = 'data/daily_engagement.csv' 
submissions_filename = 'data/project_submissions.csv' 

# reading csv files
enrollments = read_csv(enrollments_filename)
daily_engagement = read_csv(engagement_filename)
project_submissions = read_csv(submissions_filename)


for enrollment in enrollments:
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['account_key'] = parse_maybe_int(enrollment['account_key'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])

    
for engagement in daily_engagement:
   engagement['lessons_completed'] = int(float(engagement['lessons_completed']))
   engagement['num_courses_visited'] = int(float(engagement['num_courses_visited']))
   engagement['total_minutes_visited'] = float(engagement['total_minutes_visited'])
   engagement['projects_completed'] = int(float(engagement['projects_completed']))
   engagement['acct'] = int(engagement['acct'])
   engagement['utc_date'] = parse_date(engagement['utc_date'])   
   
for submission in project_submissions:
   submission['account_key'] = int(submission['account_key'])
   submission['lesson_key'] = int(submission['lesson_key'])
   submission['completion_date'] = parse_date(submission['completion_date']) 
   submission['creation_date'] = parse_date(submission['creation_date'])

# adding a new key account key and value same as 'acct' and pop the 'acct'
# from the dictionary
for engagement in daily_engagement:
   engagement['account_key'] = int(engagement['acct'])
   engagement.pop('acct',None)

print enrollments[0]
print daily_engagement[0]
print project_submissions[0] 

print "\nNumber of enrollment records : " , len(enrollments)
print "\nNumber of daily engagement records : " , len(daily_engagement)
print "\nNumber of project submissions records : " , len(project_submissions)


eSet = get_unique_set(enrollments,'account_key')
deSet =  get_unique_set(daily_engagement,'account_key')
psSet =  get_unique_set(project_submissions,'account_key')

print "\n Unique student keys in enrollments : ", len(eSet)
print "\n Unique student keys in daily engement : ", len(deSet)
print "\n Unique student keys in project submissions : ", len(psSet)

#Enrollment keys for missing daily engagement records
acct_keys_set_missing_de = get_key_set_not_in(eSet,deSet)

print "\nNumber of students with missed daily engagement records :", len(acct_keys_set_missing_de)

missed_enrollment_records = filter_data_with_keys(enrollments,'account_key',acct_keys_set_missing_de)

# some employee in the missed_enrollment records have same enrollment and cancel date or datys to cancel is not zero

missed_enrollment_records_days_to_cancel_is_not_zero = list()
for enrollment in missed_enrollment_records : 
    if enrollment['days_to_cancel'] != 0:
        missed_enrollment_records_days_to_cancel_is_not_zero.append(enrollment)

print "\n Number of students with missed daily engagement records and days to cancel is not zero : ", len(missed_enrollment_records_days_to_cancel_is_not_zero)


# all the records in missed_enrollement_days_to_cancel_is_not_zero are the test records added by the udacity
#this is identified by the field is_udacity = false

udacity_test_accounts = get_udacity_test_account_set(enrollments)

non_udacity_enrollments = remove_udacity_test_accounts(enrollments,udacity_test_accounts)
non_udacity_daily_engagements = remove_udacity_test_accounts(daily_engagement,udacity_test_accounts)
non_udacity_project_submissions = remove_udacity_test_accounts(project_submissions,udacity_test_accounts)

print "\nNumber of original enrollment records : " , len(enrollments)
print "\nNumber of  new enrollment records : " , len(non_udacity_enrollments)

paid_students = get_paid_students_dict(non_udacity_enrollments)

print "\n number of unique students who atleast stayed at least a week",len(paid_students)

paid_enrollments = remove_free_trial_cancels(non_udacity_enrollments,paid_students)
paid_daily_engagements = remove_free_trial_cancels(non_udacity_daily_engagements,paid_students)
paid_project_submissions = remove_free_trial_cancels(non_udacity_project_submissions,paid_students)

paid_engagements_in_first_week = list()
for de in daily_engagement:
    account_key = de['account_key']
    if account_key in paid_students and within_one_week(paid_students[account_key],de['utc_date']):
        paid_engagements_in_first_week.append(de)

print "\n number of daily enrollment records within one week",len(paid_engagements_in_first_week)

engagement_by_account = get_data_grouped_by_field(paid_engagements_in_first_week,'account_key')
total_minutes_by_account = group_values_by_account(engagement_by_account,'total_minutes_visited')
describe_data(total_minutes_by_account.values())
total_lessons_completed_by_account = group_values_by_account(engagement_by_account,'lessons_completed')
describe_data(total_lessons_completed_by_account.values())

days_visited_by_account = group_no_of_valid_rows_by_account(engagement_by_account,'num_courses_visited')
describe_data(days_visited_by_account.values())


## Create two lists of engagement data for paid students in the first week.
## The first list should contain data for students who eventually pass the
## subway project, and the second list should contain data for students
## who do not.

subway_project_lesson_keys = [746169184, 3176718735]

passed_dict = get_proj_completion_dict(paid_project_submissions,subway_project_lesson_keys)

print "length of passed_dict : ", len(passed_dict)

passing_engagement = get_passing_engagementList(engagement_by_account,passed_dict,True)
non_passing_engagement = get_passing_engagementList(engagement_by_account,passed_dict,False)

print "number of passing engagement records : ",len(passing_engagement)
print "number of non passing engagement records : ",len(non_passing_engagement)


passing_engagement_by_account = get_data_grouped_by_field(passing_engagement,'account_key')
non_passing_engagement_by_account = get_data_grouped_by_field(non_passing_engagement,'account_key')


dataField = 'total_minutes_visited'
print "\n",dataField," - passed engagement metrics"
x1 = group_values_by_account(passing_engagement_by_account,dataField)
describe_data(x1.values())
print "\n",dataField," - non-passed engagement metrics"
x2 = group_values_by_account(non_passing_engagement_by_account,dataField)
describe_data(x2.values())

dataField = 'num_courses_visited'
print "\n", dataField, " - passed engagement metrics"
y1 = group_no_of_valid_rows_by_account(passing_engagement_by_account, dataField)
describe_data(y1.values())
print "\n", dataField, " - non-passed engagement metrics"
y2 = group_no_of_valid_rows_by_account(non_passing_engagement_by_account, dataField)
describe_data(y2.values())

dataField = 'lessons_completed'
print "\n", dataField, " - passed engagement metrics"
z1 = group_values_by_account(passing_engagement_by_account, dataField)
describe_data(z1.values())
print "\n", dataField, " - non-passed engagement metrics"
z2 = group_values_by_account(non_passing_engagement_by_account, dataField)
describe_data(z2.values())





