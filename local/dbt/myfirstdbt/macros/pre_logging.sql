{% macro insert_trans_history() %}
INSERT INTO src.trans_history (modelname, status, rowcount, startdate, enddate)
VALUES ('{{ this }}', 'active', 0, now(), now());
{% endmacro %}