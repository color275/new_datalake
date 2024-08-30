{% macro update_trans_history() %}
UPDATE src.trans_history 
SET status = 'done',
    rowcount = (SELECT COUNT(*) FROM {{ this }}),
    enddate = now()
WHERE modelname = '{{ this }}'
  AND jobid = (SELECT MAX(jobid) FROM src.trans_history  WHERE modelname = '{{ this }}')
  AND startdate = (SELECT MAX(startdate) FROM src.trans_history  WHERE modelname = '{{ this }}');
{% endmacro %}