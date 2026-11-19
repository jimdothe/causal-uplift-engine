-- Typed copy of raw Criteo (10% sample). `exposure` is kept for Model 3 but is NOT randomized.
select
    cast(row_id as bigint)     as row_id,
    {% for i in range(12) -%}
    cast(f{{ i }} as double)   as f{{ i }},
    {% endfor -%}
    cast(treatment as integer) as treatment,
    cast(exposure as integer)  as exposure,
    cast(visit as integer)     as visit,
    cast(conversion as integer) as conversion
from {{ source('raw', 'criteo') }}
