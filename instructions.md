This application is meant for visualising and analysing earthquake catalogs. The supported catalog types are   
* [The QTM seismicity catalogs (SCEDC)](https://scedc.caltech.edu/research-tools/QTMcatalog.html)
* [The focal mechanism catalogs (SCEDC)](https://scedc.caltech.edu/research-tools/alt-2011-yang-hauksson-shearer.html)
* [Basel seismicity catalog](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2019JB017468)
* [Otaniemi seismicity catalog](https://advances.sciencemag.org/content/5/5/eaav7224)   

To get started, please upload the catalog of your choice by clicking the upload area above, or by dragging the file onto it.

Once the data has been uploaded, the available features include a map view, a scatter plot view, and a clustering view. Each of the features includes a set of configurations to control them. With the exception of the clustering view, changes in the settings only take effect after submitting them by clicking on the "Apply" button on each page.

##### Map

The map can be configured with the following settings:
*  **Time range** allows the user to select the start and the end time for the earthquakes shown on the map. The selected dates represent the start and the end of the time slider underneath the map, respectively.
* **Time step** includes a selection of the value and the unit of one time step. A time step is the length of the time shown in one still frame on the map.
* **Size column** is used to define which column from the uploaded data is used to set the size for the marker of each earthquake. Only numerical columns are listed as valid choices.
* **Color column** defines the column used for setting the color of each marker. Only numerical columns are listed as valid choices.
* **Template ID** restricts the visible earthquakes to those that have the defined template. Using this feature disables the time slider and the time step selections will be ignored. The time range setting is still valid: only the events that occurred within the selected time range are shown. This configuration is available only for the catalogs that contain information about the events' template IDs.
* **Visualize location uncertainties** toggles visualizing the uncertainties in location for each earthquake marker on and off. If the catalog contains no information about location uncertainties, a default range of 500 m is used. The uncertainties are related to the location of the hypocenter, the size of the marker is not taken into account.
* **Show fault lines** toggles the Southern California fault lines on and off. Only available for the two SCEDC catalogs. **NB**: slows down the application, not recommended with the play-feature.

The time slider below the map can be either moved manually, or played automatically from start to end. Using the play-feature will automatically move the time slider one step at a time, once every three seconds, until the end. The currently shown time step with start and end times is visible underneath the slider. Clicking on an earthquake on the map will display all the information related to it.

##### Scatter plot

The configurations available on the scatter plot are
*  **Time range** allows the user to select the start and the end dates for the earthquakes shown on the plot. All the earthquakes that occurred between the start and the end dates are shown.
* **X/Y-axis** settings define which column is used for which of the axes. Any column, even non-numerical ones can be selected here.
* **Size column** is used to define which column from the uploaded data is used to set the size for the marker of each earthquake. Only numerical columns are listed as valid choices.
* **Color column** defines the column used for setting the color of each marker. Only numerical columns are listed as valid choices.

The plot can be zoomed into by selecting an area to zoom into or by clicking on the zoom icons in the top right corner of the plot. Zooming out can also be done by a double-click. After moving the plot around, it can be restored to its original position and zoom level by clicking on the "Reset axes" icon. Other options include printing a png of the plot, and selecting what is shown when hovering over a marker.

##### Clustering

The clustering method used is based on a distance measure introduced by [Zaliapin and Be-Zion (2013)](https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1002/jgrb.50179), which defines the distance between two earthquakes in terms of the difference in their location, time of occurrence, and magnitude. The distances are then used to find clusters with fore-, main-, and aftershocks, similarly to an accompanying article [Zaliapin and Be-Zion (2013)](https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1002/jgrb.50178).

*  **Time range** allows the user to select the start and the end dates for the earthquakes included in the clustering. All the earthquakes that occurred between the start and the end dates are taken into account.

Different clusters can be compared easily by selecting a time range in each of the two tabs. **NB**: The clustering takes quite a while, especially with large amounts of data.

##### Data

The uploaded data can be inspected in this view. Available features consists of filtering and sorting the data. Using the control underneath the table, you can browse through the whole data set. Filtering is possible by using the inputs under each column header. Syntax for filtering is as follows:
* `=` or `eq` are used to search for exact matches, and `!=` or `ne` filter out the rows containing the given value.
* `>` or `gt`, and `<` or `lt` return rows that have values greater than or less than the input. Similarly, `>=` or `ge`, and `<=` or `le` find rows with values greater/less than or equal to the given value.
* Entering a value without an operator returns partial matches, this can only be used with columns that have alphabetic values. Optionally, the operator `contains` can be inserted before the input.
