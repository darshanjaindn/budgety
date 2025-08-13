import os

# Define the folder structure
structure = {
    "budgetly": {
        "backend": {
            "package.json": "",
            ".env": "",
            "src": {
                "server.js": "",
                "config": {
                    "passport.js": ""
                },
                "models": {
                    "User.js": "",
                    "Transaction.js": "",
                    "Category.js": ""
                },
                "routes": {
                    "auth.js": "",
                    "api.js": ""
                },
                "middleware": {
                    "auth.js": ""
                }
            },
            "README.md": ""
        },
        "frontend": {
            "package.json": "",
            "vite.config.js": "",
            "src": {
                "main.jsx": "",
                "App.jsx": "",
                "services": {
                    "api.js": "",
                    "auth.js": ""
                },
                "pages": {
                    "Login.jsx": "",
                    "Dashboard.jsx": "",
                    "Transactions.jsx": "",
                    "Categories.jsx": "",
                    "Settings.jsx": ""
                },
                "components": {
                    "Nav.jsx": "",
                    "TransactionForm.jsx": ""
                }
            },
            "README.md": ""
        },
        "README.md": ""
    }
}

def create_structure(base_path, struct):
    for name, content in struct.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):  # It's a folder
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:  # It's a file
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

# Create the folder structure in the current directory
create_structure(".", structure)

print("✅ Folder and file structure created successfully.")