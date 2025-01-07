def export_url(url, output_file="exported_url.txt"):
    try:
        with open(output_file, 'w') as file:
            file.write(url + "\n")
        print(f"URL exported to {output_file}")
    except Exception as e:
        print(f"Error exporting URL: {e}")

def import_url(input_file="exported_url.txt"):
    try:
        with open(input_file, 'r') as file:
            url = file.readline().strip()
        print(f"URL imported from {input_file}")
        return url
    except Exception as e:
        print(f"Error importing URL: {e}")
        return None
