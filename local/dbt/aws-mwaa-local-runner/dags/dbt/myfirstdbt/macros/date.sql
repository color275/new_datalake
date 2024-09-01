-- macros/date.sql

{% macro timestamp_to_string(timestamp_col, format="YYYY-MM-DD HH24:MI:SS") %}
    {# 
    이 매크로는 타임스탬프 형식의 날짜 데이터를 지정된 문자열 포맷으로 변환한다.
    format 파라미터를 통해 원하는 출력 형식을 지정할 수 있으며, 기본값은 'YYYY-MM-DD HH24:MI:SS'이다.
    #}
    TO_CHAR({{timestamp_col}}, '{{format}}')
{% endmacro %}

{% macro now_string(timezone='Asia/Seoul', format='YYYY-MM-DD HH24:MI:SS') %}
    {#
    이 매크로는 현재 시간을 지정된 타임존과 포맷에 맞춰 문자열로 반환한다.
    기본 타임존은 'Asia/Seoul'이며, 기본 포맷은 'YYYY-MM-DD HH24:MI:SS'이다.
    #}
    TO_CHAR(TIMEZONE('{{timezone}}', CURRENT_TIMESTAMP), '{{format}}')
{% endmacro %}


{% macro to_kst_str(timestamp_str) %}
    {# 
    이 매크로는 주어진 타임스탬프 문자열을 KST(한국 표준시)로 변환하는 기능을 수행한다.
    - 'today_00:00': 오늘 자정(00:00:00)을 반환.
    - 'tomorrow_00:00': 내일 자정(00:00:00)을 반환.
    - '+00:00'이 포함된 UTC 타임스탬프는 9시간을 더해 KST로 변환.
    - 기타 타임스탬프 문자열은 그대로 KST 포맷으로 변환된다.
    #}
    
    {% if timestamp_str == 'today_00:00' %}
        TO_CHAR(CURRENT_DATE, 'YYYY-MM-DD') || ' 00:00:00'
    {% elif timestamp_str == 'tomorrow_00:00' %}
        TO_CHAR(CURRENT_DATE + INTERVAL '1 day', 'YYYY-MM-DD') || ' 00:00:00'
    {% elif '+00:00' in timestamp_str %}
        TO_CHAR(
            (TO_TIMESTAMP('{{ timestamp_str }}', 'YYYY-MM-DD HH24:MI:SS+00:00') + INTERVAL '9 hours'),
            'YYYY-MM-DD HH24:MI:SS'
        )
    {% else %}
        TO_CHAR(
            TO_TIMESTAMP('{{ timestamp_str }}', 'YYYY-MM-DD HH24:MI:SS'),
            'YYYY-MM-DD HH24:MI:SS'
        )
    {% endif %}
{% endmacro %}