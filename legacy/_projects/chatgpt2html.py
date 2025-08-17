# def add_html_paragraph_tags(file_path, output_file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     with open(output_file_path, 'w') as file:
#         for line in lines:
#             if line.strip():  # If the line is not empty
#                 file.write('<p>\n' + line.strip() + '\n</p>\n')
#             else:
#                 file.write('\n')


# # Example usage
# input_file = r"C:\projects\website-content\aichat1.txt"
# output_file = 'output.html'
# add_html_paragraph_tags(input_file, output_file)

# Rewriting the script from scratch to add HTML paragraph tags around paragraphs, 
# while ignoring lines that start with "User" or "ChatGPT".

# def add_html_paragraph_tags_excluding_specific_lines(file_path, output_file_path, exclude_prefixes):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     with open(output_file_path, 'w') as file:
#         for line in lines:
#             if not line.startswith(exclude_prefixes) and line.strip():
#                 file.write('<p>\n' + line.strip() + '\n</p>\n')
#             elif not line.startswith(exclude_prefixes):
#                 file.write('\n')

# # Example usage
# input_file = r"C:\projects\website-content\aichat1.txt"
# output_file = '_python/output2.html'
# exclude_prefixes = ("User", "ChatGPT")
# add_html_paragraph_tags_excluding_specific_lines(input_file, output_file, exclude_prefixes)

# output_file

# Rewriting the script from scratch to add HTML paragraph tags around each line.
# For lines following those that start with "User", the content will be wrapped in <em> tags within the paragraph tags.

# Rewriting the script to add HTML paragraph tags around each line.
# Lines following "User" will be wrapped in <em> tags within paragraph tags.
# Lines following "ChatGPT" will be wrapped in normal paragraph tags, ignoring the "ChatGPT" line itself.

# Rewriting the script to correctly add HTML paragraph tags around each line.
# Lines following "User" will be wrapped in <em> tags within paragraph tags.
# Lines following "ChatGPT" will be wrapped in normal paragraph tags, ignoring the "ChatGPT" line itself and without emphasis tags.

def add_html_paragraph_tags_corrected(file_path, output_file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(output_file_path, 'w') as file:
        add_emphasis = False
        for line in lines:
            line_content = line.strip()
            if line_content.startswith("User"):
                add_emphasis = True
            elif line_content.startswith("ChatGPT"):
                add_emphasis = False
                continue  # Skipping writing the "ChatGPT" line itself
            elif line_content and add_emphasis:
                file.write(f'<p><em>{line_content}</em></p>\n')
                add_emphasis = False  # Resetting the flag
            elif line_content:
                # Normal paragraph tags for other lines
                file.write(f'<p>{line_content}</p>\n')

# Example usage
input_file = r"C:\projects\website-content\aichat1.txt"
output_file = '_python/output2.html'
add_html_paragraph_tags_corrected(input_file, output_file)

output_file







