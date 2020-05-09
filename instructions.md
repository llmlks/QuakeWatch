This application is meant for visualising and analysing earthquake catalogs. The supported catalog types are   

<ul>
  <li><a href="https://scedc.caltech.edu/research-tools/QTMcatalog.html" target="_blank">The QTM seismicity catalogs (SCEDC)</a></li>
  <li><a href="https://scedc.caltech.edu/research-tools/alt-2011-yang-hauksson-shearer.html" target="_blank">The focal mechanism catalogs (SCEDC)</a></li>
  <li><a href="https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2019JB017468" target="_blank">Basel seismicity catalog</a></li>
  <li><a href="https://advances.sciencemag.org/content/5/5/eaav7224" target="_blank">Otaniemi seismicity catalog</a></li>
</ul>

To get started, please upload the catalog of your choice by clicking the upload area above, or by dragging the file onto it. Optionally, you can use the sample dataset by clicking on the button below the upload area. The sample catalog is the 2018 Focal Mechanism Catalog from SCEDC.

Once the data has been uploaded, the available features include a map view, a scatter plot view, and a clustering view. Each of the features includes a set of configurations to control them. With the exception of the clustering view, changes in the settings only take effect after submitting them by clicking on the "Apply" button on each page.

##### Map

The map can be configured with the following settings:
*  **Select dates** allows the user to select the start and the end time for the earthquakes shown on the map. The selected dates represent the start and the end of the time slider underneath the map, respectively.
* **Time step** includes a selection of the value and the unit of one time step. A time step is the length of the time shown in one still frame on the map.
* **Size column** is used to define which column from the uploaded data is used to set the size for the marker of each earthquake. Only numerical columns are listed as valid choices.
* **Color column** defines the column used for setting the color of each marker. Only numerical columns are listed as valid choices.
* **Template ID** restricts the visible earthquakes to those that have the defined template. The other configurations are still valid, thus the earthquakes are only shown from the selected time range. If the earthquakes should be visible at the same time, the option **Show earthquakes cumulatively** can be used, together with setting the time slider below the map at the right. This will display all the events with the same template ID in the selected time range. This configuration is available only for the catalogs that contain information about the events' template IDs.
* **Update frequency** sets the update frequency of the "Play" feature in seconds. Default value is 2 seconds. **NB**: a very small value may cause the "Play" feature to lag.
* **Visualize location uncertainties** toggles visualizing the uncertainties in location for each earthquake marker on and off. If the catalog contains no information about location uncertainties, a default range of 500 m is used. The uncertainties are related to the location of the hypocenter, the size of the marker is not taken into account.
* **Show fault lines** toggles the Southern California fault lines on and off. Only available for the two SCEDC catalogs. **NB**: slows down the application, not recommended with the play-feature.
* **Show earthquakes cumulatively** controls whether the visible earthquakes consist only of those that occurred within the selected time slot, or whether all earthquakes from the start of the time range until the end of the selected time slot are visible.
* **Opacity decrease rate** is available for configuration when the **Show earthquakes cumulatively** is selected. When displaying the earthquakes cumulatively, the opacity of the earthquake markers is computed as a logarithm of time. Thus, the larger the time difference between the the end of the current time slot and the time of occurrence, the more transparent the marker. The rate of the decrease can be controlled by selecting the value and unit of time in which the opacity decreases.

The time slider below the map can be either moved manually, or played automatically from start to end. Using the play-feature will automatically move the time slider one step at a time, once every x seconds set by the configuration "Update frequency", until the end. The currently shown time step with start and end times is visible underneath the slider. Clicking on an earthquake on the map will display all the information related to it.

##### Scatter plot

The configurations available on the scatter plot are
*  **Select dates** allows the user to select the start and the end dates for the earthquakes shown on the plot. All the earthquakes that occurred between the start and the end dates are shown.
* **X/Y-axis** settings define which column is used for which of the axes. Any column, even non-numerical ones can be selected here.
* **Size column** is used to define which column from the uploaded data is used to set the size for the marker of each earthquake. Only numerical columns are listed as valid choices.
* **Color column** defines the column used for setting the color of each marker. Only numerical columns are listed as valid choices.

The plot can be zoomed into by selecting an area to zoom into or by clicking on the zoom icons in the top right corner of the plot. Zooming out can also be done by a double-click. After moving the plot around, it can be restored to its original position and zoom level by clicking on the "Reset axes" icon. Other options include printing a png of the plot, and selecting what is shown when hovering over a marker.

##### Histogram

The configurations available on the histogram are
*  **Time range** allows the user to select the start and the end dates for the earthquakes shown on the plot. All the earthquakes that occurred between the start and the end dates are shown.
* **Column** is used to define which column from the uploaded data is used as the data for the histogram. Any column, even non-numerical ones can be selected here.
* **Maximum number of bins** is used to define the maximum number of desired bins. The biggest number, that is lower than the selected maximum and provides a nice round number for the bin size is selected for the plot. For non-numerical columns, the number of bins is always the number of different labels.

The plot can be zoomed into by selecting an area to zoom into or by clicking on the zoom icons in the top right corner of the plot. Zooming out can also be done by a double-click. After moving the plot around, it can be restored to its original position and zoom level by clicking on the "Reset axes" icon. Other options include printing a png of the plot, and selecting what is shown when hovering over a marker.

##### Clustering

The clustering method used is based on a distance measure introduced by [Zaliapin and Be-Zion (2013)](https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1002/jgrb.50179), which defines the distance between two earthquakes in terms of the difference in their location, time of occurrence, and magnitude. The distances are then used to find clusters with fore-, main-, and aftershocks, similarly to an accompanying article [Zaliapin and Be-Zion (2013)](https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1002/jgrb.50178). 

The clustering method works by finding the nearest neighbor (using the Zaliapin distance as measure of closeness; the nearest neighbor is also known as the parent event) for each event, this process creates a spanning network; a single cluster where each event is connected to its parent. The cluster can be modeled as a graph, where each edge is assigned a weight equal to the Zaliapin distance between the two events and the strength of an edge is defined as the inverse of the Zaliapin distance. This graph is pruned by removing weak edges, that is, edges whose strength is lower than certain threshold value, as a result the large graph is split into smaller disjoint ones. 

For each graph, the event with the highest magnitude is labeled as the **mainshock**. Events occurring before the mainshock, are categorized as **foreshocks**, and finally, events taking place after the mainshock, are named **aftershocks**. 

*  **Select dates** allows the user to select the start and the end dates for the earthquakes included in the clustering. All the earthquakes that occurred between the start and the end dates are taken into account.
* **Threshold value** allows the user to control the threshold value for removing edges. High values would lead to fewer and higly connected clusters, lower values to more sparse and less populated ones. 


Different clusters can be compared easily by selecting a time range in each of the two tabs. **NB**: The clustering takes quite a while, especially with large amounts of data.

##### Data

The uploaded data can be inspected in this view. Available features consists of filtering and sorting the data. Using the control underneath the table, you can browse through the whole data set. Filtering is possible by using the inputs under each column header. Syntax for filtering is as follows:
* `=` or `eq` are used to search for exact matches, and `!=` or `ne` filter out the rows containing the given value.
* `>` or `gt`, and `<` or `lt` return rows that have values greater than or less than the input. Similarly, `>=` or `ge`, and `<=` or `le` find rows with values greater/less than or equal to the given value.
* Entering a value without an operator returns partial matches, this can only be used with columns that have alphabetic values. Optionally, the operator `contains` can be inserted before the input.
