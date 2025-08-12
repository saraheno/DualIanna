chmod 777 /data/users/eno/CalVision/dd4hep/stuff4stuff/DualTestBeam/compact/jobs/*
condor_submit /data/users/eno/CalVision/dd4hep/stuff4stuff/DualTestBeam/compact/jobs/condor-executable-FSCEPonly-20-e.jdl
condor_submit /data/users/eno/CalVision/dd4hep/stuff4stuff/DualTestBeam/compact/jobs/condor-executable-FSCEPonly-20-pi.jdl
condor_q