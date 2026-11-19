-- Typed copy of raw Hillstrom. No feature engineering here: the authors' preprocessing runs in pipeline/prepare.py.
select
    cast(row_id as bigint)            as row_id,
    cast(recency as integer)          as recency,
    cast(history_segment as varchar)  as history_segment,
    cast(history as double)           as history,
    cast(mens as integer)             as mens,
    cast(womens as integer)           as womens,
    cast(zip_code as varchar)         as zip_code,
    cast(newbie as integer)           as newbie,
    cast(channel as varchar)          as channel,
    cast(segment as varchar)          as segment,
    cast(visit as integer)            as visit,
    cast(conversion as integer)       as conversion,
    cast(spend as double)             as spend
from {{ source('raw', 'hillstrom') }}
