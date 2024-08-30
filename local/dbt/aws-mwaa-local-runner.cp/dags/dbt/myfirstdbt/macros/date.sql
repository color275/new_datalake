-- macros/date.sql

-- timestamp 포맷의 날짜 데이터를 특정 포맷의 string 타입으로 변환하는 매크로
-- format 파라메터를 지정하지 않으면 YYYY-MM-DD 가 default
{% macro timestamp_to_string(timestamp_col, format="YYYY-MM-DD HH24:MI:SS") %}
    TO_CHAR({{timestamp_col}}, '{{format}}')
{% endmacro %}

-- 현재 년월일 시간을 KST 시간의 string 타입으로 리턴하는 매크로
{% macro now_string(timezone='Asia/Seoul', format='YYYY-MM-DD HH24:MI:SS') %}
    TO_CHAR(TIMEZONE('{{timezone}}', CURRENT_TIMESTAMP), '{{format}}')
{% endmacro %}