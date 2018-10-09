# Project Title: Web Portal for Concentration and Flux of CO<sub>2</sub> in Global Inland Waters
## Phase 2 Project Development of the CO<sub>2</sub> Web Portal


## **Two Directions:**
* [**1. Refining and developing backend database models**](##**Refining-and-developing-backend-database-models:**)
* [**2. Developing frontend views of the CO<sub>2</sub> web portal**](##-**2.-Frontend-Views-to-be-developed**)

See details below:

Note: 
* (1) In the following descriptions, measurement refers to column-wise or field-wise variable (e.g., CO<sub>2</sub>, CO<sub>2</sub> flux, and DOC, etc.) in the database and sample refers to row-wise or case-wise serial measurements. One sample can have many measurements.
* (2) Refer to docs/Date_Template.xlsx when reading the following descriptions about the database model.
* (3) Refer to docs/Web portal.pptx when reading about development of frontend views.

## **Refining and developing backend database models:**

**Overall description**

The backend database contains the following **six database tables**: Site Location, Physical Properties, Greenhouse Gas Concentrations, Greenhouse Gas Fluxes, Gas Transfer Velocity, and Other Measurements. 

The Site Location table contains fields such as *Site Type*, *Latitude*, *Longitude*, *Altitude* and the geometry field *Point*.

Physical properties refer to physical properties of the surveyed water body and/or the surrounding environment while taking field measurements of greenhouse gases. The Physical Properties table contains the following 8 fields: *Width*, *Depth*, *Surface Area*, *Discharge*, *Flow Velocity*, *Wind Speed*, *Water Temperature* and *Air Temperature*.

The Greenhous Gas Concentrations table contains concentration measurements of three types of greenhouse gases, namely, *CO<sub>2</sub>*, *CH<sub>4</sub>* and *N<sub>2</sub>O*, corresponding to the 3 fields in this database table.

The Greenhouse Gas Fluxes table contains measurements of greenhouse gas emission fluxes from the water body’s surface. It also contains 3 fields, *CO<sub>2</sub> Flux*, *CH<sub>4</sub> Flux* and *N<sub>2</sub>O Flux*, corresponding to the three greenhouse gases.

Gas transfer velocity (or, k) refers to the rate at which a gas is evaded from the water-air interface. It is usually calculated according to the Fick’s Law of diffusion (see https://www.comsol.com/multiphysics/diffusion-equation), or in our case, dividing a field measurement of gas flux by the gas concentration difference between the water body and the overlying atmosphere. It is a convention to normalize the measured gas transfer velocity to a Schmidt number of 600, called k<sub>600</sub>, in order to be comparable among different gases.

Theoretically, k<sub>600</sub> measured from different gases at the same location and time should be the same. In reality, however, k<sub>600</sub> from different gases can vary significantly due to large uncertainty associated with this measurement. In addition, evasion of CH<sub>4</sub> from water surfaces includes bubble fluxes (i.e., non-diffusive), making k<sub>600</sub> calculated from CH<sub>4</sub> fluxes deviates significantly from diffusive k<sub>600</sub> in that case (read docs/ Raymond_et_al-2012.pdf if you want to know about gas transfer velocity).

Considering the above factors, the Gas Transfer Velocity table therefore contains 6 six fields, two for each gas, namely, *k-CO<sub>2</sub>*, *k<sub>600</sub>-CO<sub>2</sub>*, *k-CH<sub>4</sub>*, *k<sub>600</sub>-CH<sub>4</sub>*, *k-N<sub>2</sub>O* and *k<sub>600</sub>-N<sub>2</sub>O*.

Other measurements refer to measurements that are not directly related to the greenhouse gas concentration or flux but are closely related to its production or consumption in freshwaters. The Other Measurements table contains 7 fields: *DOC*, *POC*, *TOC*, *pH*, *Alkalinity*, *DO* and *Chl a*.

Besides fields contained in each database table, two fields, *Date Time* and *User Note* are sample-specific and **shared by all database tables expect the Site Location table**.

In addition, the geometry field *Point* in the Site Location table serves as the foreign key and shared by the other database tables.

__All fields listed above are optional for users to provide except the Latitude and Longitude fields.__

**Fields description**

1.1 Shared Fields (among sample-specific database tables)

1.1.1 *Date Time*

The default format for *Date Time* is yyyy-mm-dd hh:mm:ss. We provide data template for users to fill in. However, users might still have various formats for *Date Time* and in some cases even not be a date or time (e.g., date or time range). Try read *Date Time* to see whether it can be read correctly and transformed to the correct format (i.e., yyyy-mm-dd hh:mm:ss). If not, prompt with a notice to remind us to manually modify the *Date Time* input. Time zone is not considered at this stage.

1.1.2 *User Note*

Text field for storing user’s notes for sampling and measurement, etc.

1.2 the Site Location table

1.2.1 *Site Type*

Change the Site Description field to *Site Type*in the original database model. We’ll just need to differentiate among different types of inland water bodies from the site description: Stream, River, Lake, Reservoir, Estuary, Pond, Wetland, Floodplain and Others. We therefore need to deploy a procedure for filtering through user site description, grabbing key words and assigning a correct type to the *Site Type* field in our database. See below:
* If there is/are key word(s) reservoir, assign Reservoir to *Site Type* in the database;
* Else if there is/are key word(s) estuary, assign Estuary to *Site Type* in the database;
* Else if there is/are key word(s) lake, assign Lake to *Site Type* in the database;
* Else if there is/are key word(s) pond, assign Pond to *Site Type* in the database;
* Else if there is/are key word(s) stream, assign Stream to *Site Type* in the database;
* Else If there is/are key word(s) river, assign River to *Site Type* in the database; 
* Else if there is/are key word(s) floodplain, assign Floodplain to *Site Type* in the database;
* Else if there is/are key word(s) wetland, Marsh, swamp, bog, fen, meadow, assign Wetland to *Site Type* in the database;
* Else if, assign Others.

1.2.2 *Latitude* and *Longitude*

The default unit for *Latitude* and *Longitude* in the database is decimal degree. We advise users to convert their coordinates to decimal degrees before submitting. In cases where the *Latitude* and *Longitude* inputs are not decimal degrees, prompt with a notification for manually converting the inputs.

1.2.3 *Altitude*

The default unit for altitude is meters above sea level (m). Users also have options of foot or kilometer (km). Detect and convert user units to m before storage in the database. 

1 foot = 0.3048 meters, 1 kilometer = 1000 meters.

1.2.4 *Point*

The geometry field *Point* is a geometry representation of the site location in the database. The field also serves as the foreign key in other tables.

1.3 the Physical Properties table

1.3.1 *Width*

*Width* refers to the width of a water body like river, stream, estuary, or reservoir, etc. Default unit for *Width* is meter (m). Users also have options of km, foot, mile. Detect and convert user unit to m before storage into database. 

1km = 1000 m, 1 foot = 0.3048 m, and 1 mile = 1609.34 m.

1.3.2 *Depth*

*Depth* refers to water depth of the surveyed water body. Default unit for *Depth* is meter (m). Users also have options of centimeter (cm), foot, inch. Detect and convert user unit to m before storage into database. 

1 cm = 0.01 m, 1 foot = 0.3048 m, and 1 inch = 0.0254 m.

1.3.3 *Surface Area*

*Surface Area* refers to surface area covered by water of the surveyed water body. It applies to water bodies that are hard to describe with a width such as lake, wetland, and pond, etc. Default unit for *Surface Area* is square kilometer (m<sup></sup>). Users also have options of km<sup></sup>, ft<sup></sup>, and mile<sup>2</sup>. Detect and convert user unit to m<sup></sup> before storage into database. 

1 km<sup></sup> = 1,000,000 m<sup>2</sup>, 1 ft<sup></sup> = 0.0929 m<sup></sup>, and 1 mile<sup>2</sup> = 2,589,990 m<sup></sup>.

1.3.4 *Discharge*

*Discharge* applies to water bodies that have a unidirectional net flow of water such as stream, river, estuary, and reservoir, etc. The default unit for *Discharge* is m<sup>3</sup> s<sup>-1</sup> but users also have options of L s<sup>-1</sup>, ft<sup>3</sup> s<sup>-1</sup>, km<sup>3</sup> yr<sup>-1</sup>. Detect and convert user unit to m<sup>3</sup> s<sup>-1</sup> before storage into database.

1 L s<sup>-1</sup> = 0.001 m<sup>3</sup> s<sup>-1</sup>, 1 ft<sup>3</sup> s<sup>-1</sup> = 0.028317 m<sup>3</sup> s<sup>-1</sup>, and 1 km<sup>3</sup> yr<sup>-1</sup> = 31.71 m<sup>3</sup> s<sup>-1</sup>.

1.3.5 *Flow Velocity*

*Flow Velocity* refers to water flow velocity of a flowing water body such as stream, river, estuary, and reservoir, etc. The default unit for *Flow Velocity* is m s<sup>-1</sup> but users also have options of ft s<sup>-1</sup>, and cm s<sup>-1</sup>. Detect and convert user unit to m s<sup>-1</sup> before storage into database. 

1 ft s<sup>-1</sup> = 0.3048 m s<sup>-1</sup>, and 1 cm s<sup>-1</sup> = 0.01 m s<sup>-1</sup>.

1.3.6 *Wind Speed*

*Wind Speed* refers to wind speed measured at the location and time of the measurement. The default unit for *Wind Speed* is m s<sup>-1</sup> but users also have options of ft s<sup>-1</sup>. Detect and convert user unit to m s<sup>-1</sup> before storage into database. 

1 ft s<sup>-1</sup> = 0.3048 m s<sup>-1</sup>.

1.3.7 *Water Temperature*

*Water Temperature* refers to the temperature of water measured at the location and time of sampling. Default unit for *Water Temperature* is °C but users also have the option of °F. Detect and convert user unit to °C before storage into database. 

(°F – 32) × 5 / 9 = °C.

1.3.8 *Air Temperature*

*Air Temperature* refers to the temperature of overlying air measured at the location and time of sampling. Default unit for *Air Temperature* is °C but users also have the option of °F. Detect and convert user unit to °C before storage into database. 

(°F – 32) × 5 / 9 = °C.

1.4 the Greenhouse Gas Concentration table

1.4.1 *CO<sub>2</sub>*

*CO<sub>2</sub>* refers to dissolved CO<sub>2</sub> concentration in the surveyed water body. Dissolved CO<sub>2</sub> concentration in freshwater is often expressed as equivalent atmospheric partial pressure (µatm) or part per million (ppm). The default unit for *CO<sub>2</sub>* is µatm but users also have options of ppm, ppmv, µmol L<sup>-1</sup>, mmol L<sup>-1</sup> and nmol L<sup>-1</sup>. Detect and convert user unit to µatm before storage into database. 1 ppm (or ppmv) = 1 µatm. 

For conversion between µatm and mol L<sup>-1</sup>, we need to introduce a temperature sensitive Henry’s Law constant (H): - log10 (H) = - 700000  × T<sup>2</sup> + 0.015 × T + 1.11, where T is Water Temperature.
µatm = µmol L<sup>-1</sup> / H
µatm = mmol L<sup>-1</sup> × 1000 / H
µatm = nmol L<sup>-1</sup> / (H × 1000)

1.4.2 *CH<sub>4</sub>*

*CH<sub>4</sub>* refers to dissolved CH<sub>4</sub> concentration in the surveyed water body. The default unit for *CH<sub>4</sub>* is nmol L<sup>-1</sup> but users also have options of µmol L<sup>-1</sup>. Detect and convert user unit to µatm before storage into database. 

1 µmol L<sup>-1</sup>= 1000 nmol L<sup>-1</sup>.

1.4.3 *N<sub>2</sub>O*

*N<sub>2</sub>O* refers to dissolved N<sub>2</sub>O concentration in the surveyed water body. The default unit for *N<sub>2</sub>O* is nmol L<sup>-1</sup> but users also have options of µmol L<sup>-1</sup>. Detect and convert user unit to µatm before storage into database. 

1 µmol L<sup>-1</sup>= 1000 nmol L<sup>-1</sup>.

1.5 the Greenhouse Gas Flux table

1.5.1 *CO<sub>2</sub> Flux*

*CO<sub>2</sub> Flux* refers to the amount of CO<sub>2</sub> evaded from the water surface in a certain time. Default unit for *CO<sub>2</sub> Flux* in the database is g C m<sup>-2</sup> yr<sup>-1</sup>, but users also have options of mg C m<sup>-2</sup> d<sup>-1</sup>, mg C m<sup>-2</sup> hr<sup>-1</sup>, µg C m<sup>-2</sup> s<sup>-1</sup>, mmol m<sup>-2</sup> d<sup>-1</sup>, µmol m<sup>-2</sup> hr<sup>-1</sup>, and µmol m<sup>-2</sup> s<sup>-1</sup>. Detect and convert user unit to g C m<sup>-2</sup> yr<sup>-1</sup> before storage into database. 

1 mg C m<sup>-2</sup> d<sup>-1</sup> = 0.365 g C m<sup>-2</sup> yr<sup>-1</sup>, 1 mg C m<sup>-2</sup> hr<sup>-1</sup> = 8.76 g C m<sup>-2</sup> yr<sup>-1</sup>, 1 µg C m<sup>-2</sup> s<sup>-1</sup> = 31.536 g C m<sup>-2</sup> yr<sup>-1</sup>, 1 mmol m<sup>-2</sup> d<sup>-1</sup> = 4.38 g C m<sup>-2</sup> yr<sup>-1</sup>, 1 µmol m<sup>-2</sup> hr<sup>-1</sup> = 0.10512 g C m<sup>-2</sup> yr<sup>-1</sup>, 1 µmol m<sup>-2</sup> s<sup>-1</sup> = 378.432 g C m<sup>-2</sup> yr<sup>-1</sup>.	

1.5.2 *CH<sub>4</sub> Flux*

*CH<sub>4</sub> Flux* refers to the amount of CH<sub>4</sub> evaded from the water surface in a certain time. Default unit for *CH<sub>4</sub> Flux* in the database is g C m<sup>-2</sup> yr<sup>-1</sup>, but users also have options of mg C m<sup>-2</sup> d<sup>-1</sup>, mg C m<sup>-2</sup> hr<sup>-1</sup>, µg C m<sup>-2</sup> s<sup>-1</sup>, mmol m<sup>-2</sup> d<sup>-1</sup>, µmol m<sup>-2</sup> hr<sup>-1</sup>, and µmol m<sup>-2</sup> s<sup>-1</sup>. Detect and convert user unit to g C m<sup>-2</sup> yr<sup>-1</sup> before storage into database. 

1 mg C m<sup>-2</sup> d<sup>-1</sup> = 0.365 g C m<sup>-2</sup> yr<sup>-1</sup>, 1 mg C m<sup>-2</sup> hr<sup>-1</sup> = 8.76 g C m<sup>-2</sup> yr<sup>-1</sup>, 1 µg C m<sup>-2</sup> s<sup>-1</sup> = 31.536 g C m<sup>-2</sup> yr<sup>-1</sup>, 1 mmol m<sup>-2</sup> d<sup>-1</sup> = 4.38 g C m<sup>-2</sup> yr<sup>-1</sup>, 1 µmol m<sup>-2</sup> hr<sup>-1</sup> = 0.10512 g C m<sup>-2</sup> yr<sup>-1</sup>, 1 µmol m<sup>-2</sup> s<sup>-1</sup> = 378.432 g C m<sup>-2</sup> yr<sup>-1</sup>.

1.5.3 *N<sub>2</sub>O Flux*

*N<sub>2</sub>O Flux* refers to the amount of N<sub>2</sub>O evaded from the water surface in a certain time. Default unit for *N<sub>2</sub>O Flux* in the database is g N m<sup>-2</sup> yr<sup>-1</sup>, but users also have options of mg N m<sup>-2</sup> d<sup>-1</sup>, mg N m<sup>-2</sup> hr<sup>-1</sup>, µg N m<sup>-2</sup> s<sup>-1</sup>, mmol m<sup>-2</sup> d<sup>-1</sup>, µmol m<sup>-2</sup> hr<sup>-1</sup>, and µmol m<sup>-2</sup> s<sup>-1</sup>. Detect and convert user unit to g N m<sup>-2</sup> yr<sup>-1</sup> before storage into database. 

1 mg N m<sup>-2</sup> d<sup>-1</sup> = 0.365 g N m<sup>-2</sup> yr<sup>-1</sup>, 1 mg N m<sup>-2</sup> hr<sup>-1</sup> = 8.76 g N m<sup>-2</sup> yr<sup>-1</sup>, 1 µg N m<sup>-2</sup> s<sup>-1</sup> = 31.536 g N m<sup>-2</sup> yr<sup>-1</sup>, 1 mmol m<sup>-2</sup> d<sup>-1</sup> = 5.11 g N m<sup>-2</sup> yr<sup>-1</sup>, 1 µmol m<sup>-2</sup> hr<sup>-1</sup> = 0.12264 g N m<sup>-2</sup> yr<sup>-1</sup>, 1 µmol m<sup>-2</sup> s<sup>-1</sup> = 441.504 g N m<sup>-2</sup> yr<sup>-1</sup>.

1.6 the Gas Transfer Velocity table

1.6.1 *k-CO<sub>2</sub>*

*k-CO<sub>2</sub>* refers to gas transfer velocity calculated from measured CO<sub>2</sub> flux and concentration. *k-CO<sub>2</sub>* has the default unit of meter per day (m d<sup>-1</sup>) in the database but user has another option of cm hr<sup>-1</sup>. Convert the unit of *k-CO<sub>2</sub>* to m d<sup>-1</sup> before storage into the database. 

1 m d<sup>-1</sup> = 25 / 6 cm hr<sup>-1</sup>.

1.6.2 *k<sub>600</sub>-CO<sub>2</sub>*

*k<sub>600</sub>-CO<sub>2</sub>* refers to gas transfer velocity calculated from measured CO<sub>2</sub> flux and concentration which is further normalized to a Schmidt number of 600.  *k<sub>600</sub>-CO<sub>2</sub>* has the default unit of meter per day (m d<sup>-1</sup>) in the database but user has options of cm hr<sup>-1</sup>. Convert the unit of *k<sub>600</sub>-CO<sub>2</sub>* to m d<sup>-1</sup> before storage into the database. 

1 m d<sup>-1</sup> = 25 / 6 cm hr<sup>-1</sup>.

1.6.3 *k-CH<sub>4</sub>*

*k-CH<sub>4</sub>* refers to gas transfer velocity calculated from measured CO<sub>2</sub> flux and concentration. *k-CH<sub>4</sub>* has the default unit of meter per day (m d<sup>-1</sup>) in the database but user has another option of cm hr<sup>-1</sup>. Convert the unit of *k-CH<sub>4</sub>* to m d<sup>-1</sup> before storage into the database. 

1 m d<sup>-1</sup> = 25 / 6 cm hr<sup>-1</sup>.

1.6.4 *k<sub>600</sub>-CH<sub>4</sub>*

*k<sub>600</sub>-CH<sub>4</sub>* refers to gas transfer velocity calculated from measured CO<sub>2</sub> flux and concentration which is further normalized to a Schmidt number of 600.  *k<sub>600</sub>-CH<sub>4</sub>* has the default unit of meter per day (m d<sup>-1</sup>) in the database but user has options of cm hr<sup>-1</sup>. Convert the unit of *k<sub>600</sub>-CH<sub>4</sub>* to m d<sup>-1</sup> before storage into the database. 

1 m d<sup>-1</sup> = 25 / 6 cm hr<sup>-1</sup>.

1.6.3 *k-N<sub>2</sub>O*

*k-N<sub>2</sub>O* refers to gas transfer velocity calculated from measured CO<sub>2</sub> flux and concentration. *k-N<sub>2</sub>O* has the default unit of meter per day (m d<sup>-1</sup>) in the database but user has another option of cm hr<sup>-1</sup>. Convert the unit of *k-N<sub>2</sub>O* to m d<sup>-1</sup> before storage into the database. 
1 m d<sup>-1</sup> = 25 / 6 cm hr<sup>-1</sup>.

1.6.7 *k<sub>600</sub>-N<sub>2</sub>O*

*k<sub>600</sub>-N<sub>2</sub>O* refers to gas transfer velocity calculated from measured CO<sub>2</sub> flux and concentration which is further normalized to a Schmidt number of 600. *k<sub>600</sub>-N<sub>2</sub>O* has the default unit of meter per day (m d<sup>-1</sup>) in the database but user has options of cm hr<sup>-1</sup>. Convert the unit of *k<sub>600</sub>-N<sub>2</sub>O* to m d<sup>-1</sup> before storage into the database.

1 m d<sup>-1</sup> = 25 / 6 cm hr<sup>-1</sup>.

1.7 the Other Measurements table

1.7.1 *DOC*

*DOC* refers to dissolved organic carbon concentration in the surveyed water body. The default unit for *DOC* is mg L<sup>-1</sup> in the database but user has another option of µmol L<sup>-1</sup>. Convert the unit to mg L<sup>-1</sup> before storage in the database. 

12 mg L<sup>-1</sup> = 1000 µmol L<sup>-1</sup>. 

1.7.2 *POC*

*POC* refers to particulate organic carbon concentration in the surveyed water body. The default unit for *POC* is mg L<sup>-1</sup> in the database but user has another option of µmol L<sup>-1</sup>. Convert the unit to mg L<sup>-1</sup> before storage in the database. 

12 mg L<sup>-1</sup> = 1000 µmol L<sup>-1</sup>.

1.7.3 *TOC*

*TOC* refers to total organic carbon concentration in the surveyed water body. The default unit for *TOC* is mg L<sup>-1</sup> in the database but user has another option of µmol L<sup>-1</sup>. Convert the unit to mg L<sup>-1</sup> before storage in the database. 

12 mg L<sup>-1</sup> = 1000 µmol L<sup>-1</sup>.

*TOC* = POC + DOC. Therefore, for storing the three variables in the database or upon a query on the database:

** If two of the three exit, the third can be calculated from the exiting two.
** If all of the three exit, respond with the user’s original inputs.
** If one of the three exits, simply store them in the database.

1.7.4 *pH*

The *pH* value of water at the sampling location and time. *pH* has no unit.

1.7.5 *Alkalinity*

*Alkalinity* has the default unit of mg CaCO3 L<sup>-1</sup> in the database table. Prompt with notification if user unit is not mg CaCO3 L<sup>-1</sup>.

1.7.6 *DO*

*DO* refers to dissolved oxygen concentration in the water body. The default unit for *DO* is mg L<sup>-1</sup> in the database. Users have the options of mmol L<sup>-1</sup> and µmol L<sup>-1</sup>. We ask users to convert the unit to mg L<sup>-1</sup> or mmol L<sup>-1</sup> if their record is %saturation. Convert the unit of *DO* to mg L<sup>-1</sup> before storage in the database. 

1 mmol L<sup>-1</sup> = 32 mg L<sup>-1</sup>, 100 µmol L<sup>-1</sup> = 3.2 mg L<sup>-1</sup>.

1.7.7 *Chl a*

*Chl a* refers to chlorophyll a concentration in the water body. The default unit for *Chl a* is µg L<sup>-1</sup> in the database.


## **2. Frontend Views to be developed**

Note: 
(1) Refer to docs/Web portal.pptx when reading about development of frontend views.
(2) Not mature thoughts. Let’s try out a few of these.

2.1 View of home page

Contains a map interface showing background world map and site locations. It also contains links to views such as Upload Data, Download Data, etc.

2.2 View of Upload Data with Excel File

Contains links to downing the Data_Template.xlsx and Metadata_Template.xlsx files, and the link of Upload Data and Upload Metadata.

2.3 View of Uploading Data (Batch Upload)

Contains six parts of information from which to select parameters and units, corresponding fields in the database tables. Part 1: Site Information, Part 2: Water Physical Properties; Part 3: Greenhouse Gas Concentrations; Part 4, Greenhouse gas fluxes; Part 5, Gas transfer velocity; Part 6: Other measurements

Upon finishing selection of parameters and unit, ask users to specify a total number of observations and click on Generate Table.

View of Generated Spread Table: A spread table is generated upon user’s click on Generate Table with user-specified columns and unit. Small widget provided for user to adjust column sequence by giving sequence number of columns.

A submit button to send data to the backend.

2.4 View for displaying static site locations 

(1) Using interactive world map as background; 
(2) Having functionalities like changing symbol size or color, etc.

2.5 View for displaying site location marker clustering

2.6 View for displaying total measurements at each site location

2.7 View for displaying CO<sub>2</sub> measurements at one site as time series

2.8 View for displaying all CO<sub>2</sub> measurement

