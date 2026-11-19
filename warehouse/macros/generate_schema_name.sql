{#
  ci target: write to the shared schemas exactly (STAGING, VALIDATED, ANALYTICS).
  other targets: prefix with the personal schema (e.g. DEV_YASHASHREE_STAGING) so teammates don't overwrite each other.
#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- elif target.name == 'ci' -%}
        {{ custom_schema_name | trim | upper }}
    {%- else -%}
        {{ target.schema }}_{{ custom_schema_name | trim | upper }}
    {%- endif -%}
{%- endmacro %}
