-- Built only after stg_criteo tests pass (dbt build order). Source for pipeline/export.py.
select * from {{ ref('stg_criteo') }}
