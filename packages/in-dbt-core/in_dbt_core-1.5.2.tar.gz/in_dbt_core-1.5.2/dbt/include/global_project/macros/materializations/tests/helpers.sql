{% macro get_test_sql(main_sql, fail_calc, warn_if, error_if, limit) -%}
  {{ adapter.dispatch('get_test_sql', 'dbt')(main_sql, fail_calc, warn_if, error_if, limit) }}
{%- endmacro %}

{% macro default__get_test_sql(main_sql, fail_calc, warn_if, error_if, limit) -%}
    {% set warn_if, warn_denominator = get_denominator(warn_if, fail_calc) %}
    {% set error_if, error_denominator = get_denominator(error_if, fail_calc) %}

select
    {{ fail_calc }} as failures,
    {{ fail_calc }} {{ warn_denominator }} {{ warn_if }} as should_warn,
    {{ fail_calc }} {{ error_denominator }} {{ error_if }} as should_error
from (
    {{ main_sql }}
    {{ "limit " ~ limit if limit != none }}
    ) dbt_internal_test
{%- endmacro %}

{% macro get_denominator(threshold, model_name, fail_calc) %}
    {% if threshold[-1] == '%' %}
        {% set model_name = model.file_key_name.split('.')[1] %}
        {% set threshold = threshold[:-1] %}
        {% set denominator = '/ (SELECT ' ~ fail_calc ~ ' FROM ' ~ ref(model_name) ~ ') * 100' %}
    {% else %}
        {% set denominator = '' %}
    {% endif %}

    {% do return((threshold, denominator)) %}
{% endmacro %}
