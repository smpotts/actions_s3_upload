/*
  Purpose: This is a query used in Metabase to produce the data table needed for 
      the 2021-10-18 principal alert email.
  Filtering Rules: This is for trial and partner schools with at least one teacher
      who has used eSpark 10 or more times in this school year and has mastered at 
      least one standard.
*/


/*
  An aggregate of usage metrics at the school level.
*/
with school_agg as (
    select
        teacher_data_cached.school_id,
        teacher_data_cached.school_nces_id,
        school_data.unique_identifier_for_salesforce,
        max(teacher_data_cached.total_usage_days) as max_total_usage_days_per_school,
        max(teacher_data_cached.total_standards_mastered) as total_standards_mastered
    from bi.teacher_data_cached
    join bi.school_data
        on school_data.school_id = teacher_data_cached.school_id
    where teacher_data_cached.school_purpose in ('trial', 'partner')
        and total_standards_mastered > 0
    group by teacher_data_cached.school_id,
        teacher_data_cached.school_nces_id,
        school_data.unique_identifier_for_salesforce
    having max(teacher_data_cached.total_usage_days) >= 10
),

/*
  Combines the school aggregate with the teacher data to get the 
  top teacher at that school. Also uses a UDF exfunc_namecase() to 
  handle intelligent namecasing.
*/
teacher_school_metrics as (
    select
        teacher_data_cached.school_id,
        teacher_data_cached.school_nces_id,
        school_agg.unique_identifier_for_salesforce,
        exfunc_namecase(teacher_data_cached.first_name) as top_teacher_first_name,
        exfunc_namecase(teacher_data_cached.last_name) as top_teacher_last_name,
        exfunc_namecase(teacher_data_cached.school_name) as school_name,
        teacher_data_cached.school_purpose,
        row_number() over (partition by teacher_data_cached.school_id 
            order by total_quests_mastered_school_year desc nulls last, 
                total_usage_days desc nulls last, 
                last_student_login_at desc nulls last, 
                last_name) as ranking,
        school_agg.max_total_usage_days_per_school,
        school_agg.total_standards_mastered
    from bi.teacher_data_cached
    join school_agg 
        on school_agg.school_id = teacher_data_cached.school_id
)

select
    school_id,
    school_nces_id,
    unique_identifier_for_salesforce,
    top_teacher_first_name,
    top_teacher_last_name,
    school_name,
    school_purpose,
    max_total_usage_days_per_school,
    total_standards_mastered
from teacher_school_metrics
where ranking = 1 -- grab the top teacher in case of a tie
