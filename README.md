\
Enigma2 EPG Exporter
=====================

Enigma2 EPG Exported is a Python script designed to fetch Electronic Program Guide (EPG) data from an Enigma2 set-top box and save it in XMLTV format. The XMLTV file can be used with various media players and tools to display program schedules.

* * * * *

Features
--------

-   Fetches EPG data from an Enigma2 box using its API.

-   Parses an M3U playlist file to identify channel details.

-   Outputs EPG data in XMLTV format, compatible with most media applications.

-   Easy to configure and customize.

* * * * *

Requirements
------------

-   Python 3.7+

-   An Enigma2-compatible set-top box

-   M3U playlist file containing channel details

  
* * * * *

Configuration
------------

-  Configuration enigma2_ip = "10.0.0.227" # Replace with your Enigma2 box's IP 
-  m3u_file = "channels.m3u" # Replace with your M3U file path 
-  output_file = "epg.xml" # Output XMLTV file



### Example Output (XMLTV Format):


```<?xml version="1.0" encoding="utf-8"?>
<tv generator-info-name="Enigma2-EPG-Fetcher">
  <channel id="ChannelID123">
    <display-name>Channel Name</display-name>
  </channel>
  <programme start="20250113120000 +0000" stop="20250113130000 +0000" channel="ChannelID123">
    <title>Program Title</title>
    <desc>Program Description</desc>
  </programme>
</tv>






