import os
import re
import html

def get_html_title(file_path):
    """Extracts the title from an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if match:
                return html.unescape(match.group(1).strip())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

def generate_index():
    root_dir = "tools"
    tools = []

    if not os.path.exists(root_dir):
        print(f"Directory '{root_dir}' not found.")
        return

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".html"):
                full_path = os.path.join(dirpath, filename)
                # Calculate relative path from the script execution location (project root)
                rel_path = os.path.relpath(full_path, ".")

                title = get_html_title(full_path)
                if not title:
                    title = filename # Fallback to filename if no title

                # Get category from directory name (e.g., tools/image_generation -> image_generation)
                category = os.path.basename(os.path.dirname(full_path))
                if category == "tools":
                    category = "Uncategorized"

                tools.append({
                    "path": rel_path,
                    "title": title,
                    "category": category.replace("_", " ").title(),
                    "filename": filename
                })

    # Sort tools by category then title
    tools.sort(key=lambda x: (x["category"], x["title"]))

    # Group by category
    categories = {}
    for tool in tools:
        cat = tool["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(tool)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tools Index</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f8fafc; color: #1e293b; }
        .tool-card { transition: all 0.2s; }
        .tool-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    </style>
</head>
<body class="min-h-screen py-10 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
        <header class="mb-10 text-center">
            <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight mb-2">My Tools</h1>
            <p class="text-lg text-slate-600">Index of available utilities</p>
        </header>
"""

    for category, items in categories.items():
        html_content += f"""
        <div class="mb-8">
            <h2 class="text-xl font-bold text-slate-800 mb-4 border-b border-slate-200 pb-2 capitalize">{category}</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
"""
        for tool in items:
            html_content += f"""
                <a href="{tool['path']}" class="tool-card block p-2 px-4 bg-white rounded-xl border border-slate-200 hover:border-indigo-500 hover:ring-1 hover:ring-indigo-500 shadow-sm group">
                  {tool['title']}
                </a>
"""
        html_content += """
            </div>
        </div>
"""

    html_content += """
        <footer class="mt-16 text-center text-sm text-slate-400">
            <p>Generated automatically</p>
        </footer>
    </div>
</body>
</html>
"""

    with open("index.html", "w", encoding='utf-8') as f:
        f.write(html_content)

    print(f"Successfully generated index.html with {len(tools)} tools.")

if __name__ == "__main__":
    generate_index()
