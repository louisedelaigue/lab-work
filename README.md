# Lab work
Coding directed at processing raw lab data (inc. pH, DIC &amp; TA)

## pH optode
### Raw pH data processing
_fx_ph_optode.py_ : processes raw pH data acquired with a pH optode.
#### Output gives a text file inc. the folllowing:
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
_fx_airica.py_ : processes raw DIC data acquired with an AIRICA from Marianda.
#### Input is a .xlsx file inc. the following:
   * "bottled_date": date of sampling.
   * "analysis_date": date of analysis.
   * "opened_date": date at which a bottle was opened (applicable to CRMs if not using a new bottle).
   * "analysis_batch": batch number assigned to each sample based on day of analysis - batch number for a given sample should match that of the CRM calibration it belongs to.
   * "location": sample name (mostly applicable to RWS samples).
   * "sample": sample number.
   * "name": location + sample number.
   * "measurement_t": AIRICA total measurement time.
   * "preacid_t": AIRICA waiting time before acid addition.
   * "postacid_t": AIRICA waiting time after acid addition.
   * "extra_time": AIRICA extra time.
   * "sample_v": sample volume used by AIRICA for sample measurement.
   * "rinsing_v": sample volume used by AIRICA to rinse the cell.
   * "filling_speed": speed at which the Kloehn delivers the sample to the AIRICA cell for measurement.
   * "rinsing_speed": speed at which the Kloehn delivers the sample to the AIRICA cell for rinsing.
   * "pumping_speed": speed at which the Kloehn pumps the sample directly from the bottle.
   * "acid_strokes": number of acid strokes delivered to the AIRICA cell.
   * "nb_of_rinses": number of times the AIRICA cell gets rinsed.
   * "rinsing_method": chosen rinsing method for the AIRICA cell.
   * "database_name": name of the database selected in the AIRICA software.
   * "file_name": name of individual sample file name.
   * "flag": attributed to samples depending on measurement unwinding.
   * "comments": comments.
   
#### Output gives a text file, inc. the following:

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
