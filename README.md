# Lab work
Coding directed at processing raw lab data (inc. pH, DIC &amp; TA)

## pH optode
### Raw pH data processing
* _pH_optode.py_ : processes raw pH data acquired with a pH optode.
Output gives:
1. Graph per sample, inc. two subplots: 
   1) evolution of the slope while cutting one datapoint at a time.
   2) all pH datapoints (blue dots), datapoints used in computing the slope closest to 0 (red dots) and the mean from the latter (red line).
2. Text file inc., per sample:
   * "pH_raw_mean": mean of all raw pH datapoints, pre-processing.
   * "pH_raw_median": median of all raw pH datapoints, pre-processing.
   * "pH_last2min_mean": mean of pH datapoints during the last 2 min of measurement, pre-processing.
   * "pH_last2min_median": median of pH datapoints during the last 2 min of measurement, pre-processing.
   * "slope": slope closest to 0.
   * "lowest_ix": index at which slope closest to 0 occurs (gives an idea of how many datapoints are used).
   * "pH_s0_mean": mean pH only using datapoints giving the slope closest to 0, post-processing.
   * "pH_s0_median": median pH only using datapoints giving the slope closest to 0, post-processing.
   * "pH_s0_stderr": standard deviation of pH datapoints using only datapoints giving the slope closest to 0, post-processing.
   * "pH_s0_intercept": intercept of pH datapoints using only datapoints giving the slope closest to 0, post-processing.

## AIRICA
### Raw AIRICA data processing
* _fx_airica.py_ : processes raw pH data acquired with a pH optode.
Output gives a text file, inc. the following:
   * "temperature": temperature recorded at the time of measurement.
   * "salinity": salinity given to the AIRICA software.
   * "density": computed by the AIRICA software.
   * "mass_sample": mass of each sample computed by the AIRICA software.
   * "time": time of measurement.
   * "area_x" (x = 1, 2, 3 or 4): area under the curve of AIRICA integration.
   * "area_av_x" (x = 3 or 4): average area using the last 3 or all 4 areas computed by the AIRICA software.
   * "CF_x" (x = 3 or 4): conversion factor computed from the CRMs, using either the last 3 or all 4 areas computed by the AIRICA software.
   * "TCO2_x" (x = 3 or 4): final DIC value, calculated either from CF_3 or CF_4.

## VINDTA

### Data
* _VINDTA_temp_sensor_calib.xlsx_ : data acquired while calibrating VINDTA #17's temperature sensor on Port #4, using an OMEGA PT-104 Temperature Data Logger.

### Protocols
* _VINDTA_brackish_waters_exp_ : protocol to test VINDTA response to brackish and freshwater.
