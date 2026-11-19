-- Built only after stg_hillstrom tests pass (dbt build order). Source for pipeline/export.py.
select * from {{ ref('stg_hillstrom') }}
