-- Standardized mean difference (SMD) of each feature, each e-mail arm vs. "No E-Mail".
-- In a valid randomized experiment every |smd| should be small (< 0.05).
{% set features = ['recency', 'history', 'mens', 'womens', 'newbie'] %}

with long as (
    {% for f in features %}
    select segment, '{{ f }}' as feature, cast({{ f }} as double) as value
    from {{ ref('hillstrom') }}
    {% if not loop.last %}union all{% endif %}
    {% endfor %}
),

stats as (
    select segment, feature, avg(value) as mean_value, stddev_samp(value) as sd_value, count(*) as n
    from long
    group by segment, feature
)

select
    t.segment                                   as treatment_arm,
    t.feature,
    t.mean_value                                as treated_mean,
    c.mean_value                                as control_mean,
    (t.mean_value - c.mean_value)
        / nullif(sqrt((t.sd_value * t.sd_value + c.sd_value * c.sd_value) / 2), 0) as smd
from stats t
join stats c
  on c.feature = t.feature and c.segment = 'No E-Mail'
where t.segment <> 'No E-Mail'
