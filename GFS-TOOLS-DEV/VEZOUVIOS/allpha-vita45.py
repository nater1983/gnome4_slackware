# Open the file with URLs for reading
with open('LINKS-45NATER.TXT', 'r') as input_file:
    # Read the URLs into a list, removing leading/trailing whitespace
    urls = [line.strip() for line in input_file]

# Sort the list alphabetically
urls.sort()

# Create a new file for writing the sorted URLs
with open('45sorted_urls.txt', 'w') as output_file:
    # Write the sorted URLs to the new file
    for url in urls:
        output_file.write(url + '\n')

