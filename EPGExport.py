import requests
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Configuration
enigma2_ip = "10.0.0.227"  # Replace with your Enigma2 box's IP
m3u_file = "M3U.m3u"  # Replace with your M3U file path
output_file = "epg.xml"  # Output XMLTV file

# Function to parse M3U file and extract channel information
def parse_m3u(m3u_path):
    channels = []
    with open(m3u_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#EXTINF:"):
                tvg_id_match = re.search(r'tvg-id="([^"]+)"', line)
                tvg_name_match = re.search(r'tvg-name="([^"]+)"', line)
                tvg_id = tvg_id_match.group(1) if tvg_id_match else "Unknown"
                tvg_name = tvg_name_match.group(1) if tvg_name_match else "Unknown"
            elif line.startswith("http://"):
                channels.append({"id": tvg_id, "name": tvg_name, "url": line.strip()})
    return channels

# Function to fetch EPG for a single channel
def fetch_epg(channel_url):
    service_ref = channel_url.split("/")[-1]  # Extract service reference
    epg_url = f"http://{enigma2_ip}/web/epgservice?sRef={service_ref}"
    response = requests.get(epg_url)
    if response.status_code == 200:
        return parse_epg(response.text)
    else:
        print(f"Failed to fetch EPG for {channel_url}. HTTP {response.status_code}")
        return []

# Function to parse the EPG XML response
def parse_epg(epg_xml):
    epg_data = []
    try:
        root = ET.fromstring(epg_xml)
        for event in root.findall("e2event"):
            title = event.find("e2eventtitle").text
            description = event.find("e2eventdescription").text
            start_time = event.find("e2eventstart").text
            duration = event.find("e2eventduration").text

            start_time = datetime.fromtimestamp(int(start_time))
            end_time = start_time + timedelta(seconds=int(duration))

            epg_data.append({
                "title": title,
                "description": description,
                "start_time": start_time,
                "end_time": end_time,
            })
    except ET.ParseError as e:
        print(f"Error parsing EPG XML: {e}")
    return epg_data

# Function to generate XMLTV file
def generate_xmltv(channels, output_path):
    root = ET.Element("tv", attrib={"generator-info-name": "Enigma2-EPG-Fetcher"})

    for channel in channels:
        channel_element = ET.SubElement(
            root, "channel", attrib={"id": channel["id"]}
        )
        ET.SubElement(channel_element, "display-name").text = channel["name"]

        print(f"Fetching EPG for channel: {channel['name']}")
        epg = fetch_epg(channel["url"])
        for event in epg:
            program = ET.SubElement(
                root, "programme", attrib={
                    "start": event["start_time"].strftime("%Y%m%d%H%M%S") + " +0000",
                    "stop": event["end_time"].strftime("%Y%m%d%H%M%S") + " +0000",
                    "channel": channel["id"]
                }
            )
            ET.SubElement(program, "title").text = event["title"]
            ET.SubElement(program, "desc").text = event["description"]

    tree = ET.ElementTree(root)
    with open(output_path, "wb") as file:
        tree.write(file, encoding="utf-8", xml_declaration=True)
    print(f"EPG data saved to {output_path}")

# Main function
def main():
    channels = parse_m3u(m3u_file)
    generate_xmltv(channels, output_file)

if __name__ == "__main__":
    main()
