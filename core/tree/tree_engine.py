import os, json, datetime

ROOT = r"C:\InfinityMesh"
IGNORE = {"node_modules",".git","__pycache__","venv"}

def build_tree(path):
    tree = {}
    for name in os.listdir(path):
        if name in IGNORE:
            continue
        full = os.path.join(path,name)
        if os.path.isdir(full):
            tree[name] = build_tree(full)
        else:
            tree[name] = "file"
    return tree

tree = build_tree(ROOT)

with open(r"C:\InfinityMesh\docs\FOLDER_TREE.json","w",encoding="utf-8") as f:
    json.dump(tree,f,indent=2)

with open(r"C:\InfinityMesh\memory\state\tree_state.json","w",encoding="utf-8") as f:
    json.dump({
        "last_scan": datetime.datetime.utcnow().isoformat(),
        "root": ROOT
    },f,indent=2)

print("TREE_UPDATED")
