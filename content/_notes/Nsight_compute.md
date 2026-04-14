---


---

# List of Metrics
`nv-nsight-cu-cli --devices 0 --query-metrics`


# List all Sections
`ncu --list-sections`


# Run Profiler
`ncu -o profile ./a.out`


# Example script
```bash=
ncu -f -o profile  \
--cache-control all \
--clock-control base \
--section ComputeWorkloadAnalysis \
--section MemoryWorkloadAnalysis_Tables  \
--section SpeedOfLight_RooflineChart  \
--section WarpStateStats  \
--section MemoryWorkloadAnalysis \
--section MemoryWorkloadAnalysis_Chart \
--section SourceCounters      \
--metrics lts__t_sectors_srcunit_tex.avg.pct_of_peak_sustained_elapsed,\
lts__t_sectors_srcunit_tex_lookup_miss.sum,\
lts__t_sectors_srcunit_tex_aperture_peer_lookup_miss.sum,\
lts__t_sectors_srcunit_tex_aperture_sysmem_lookup_miss.sum,\
dram__bytes.sum.per_second,\
smsp__sass_inst_executed_op_memory_8b.sum,\
smsp__sass_inst_executed_op_memory_16b.sum,\
smsp__sass_inst_executed_op_memory_32b.sum,\
smsp__sass_inst_executed_op_memory_64b.sum,\
smsp__sass_inst_executed_op_memory_128b.sum,\
l1tex__t_sectors.sum.pct_of_peak_sustained_elapsed,\
lts__t_sectors_op_read.sum.pct_of_peak_sustained_elapsed,\
lts__t_sectors_op_write.sum.pct_of_peak_sustained_elapsed,\
smsp__sass_inst_executed_op_shared_ld.sum,\
pcie__read_bytes.sum.per_second,\
pcie__write_bytes.sum.per_second,\
smsp__sass_inst_executed_op_shared_st.sum,\
smsp__pcsamp_sample_count,\
gpc__cycles_elapsed.max \
bin/a.out
```

# Reference
https://developer.nvidia.com/blog/using-nsight-compute-to-inspect-your-kernels/
https://www2.cisl.ucar.edu/sites/default/files/2022-06/10_HandsOnNsight_ncu.pdf