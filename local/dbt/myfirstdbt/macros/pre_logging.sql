{% macro insert_trans_history() %}

{% set start = to_kst_str(var('data_interval_start', 'today_00:00')) %}
{% set end = to_kst_str(var('data_interval_end', 'tomorrow_00:00')) %}

INSERT INTO src.trans_history (modelname, status, rowcount, startdate, enddate, data_interval_start, data_interval_end)
VALUES (
    '{{ this }}',
    'active',
    -1,
    now(),
    now(),
    {{ start }}, 
    {{ end }}
);

{% endmacro %}