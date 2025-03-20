# sparkparse

identify spark bottlenecks without breaking your neck

![example](docs/sparkparse.png)

## design goals

- simplified ui that highlights bottlenecks and their causes
- node drill-down for detailed information and metric distribution
- generation of base models and dataframes for extensible analysis

## TODOs

- [ ] structured node details like project columns and scan sources
- [ ] task histograms on node click
- [ ] hotspot highlighting by metrics other than duration (spill, records, etc.)
- [ ] metric capture via context manager / decorator
- [ ] reading from cloud storage
