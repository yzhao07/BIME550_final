import requests

def get_children(doid, level=0, visited=set()):
    """ Recursively fetch children for a given DOID """
    l = []
    indent = "  " * level  # Indentation for hierarchy visualization
    encoded_doid = doid.replace(":", "_")  # Convert DOID:303 → DOID_303
    children_url = f"https://www.ebi.ac.uk/ols4/api/ontologies/doid/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F{encoded_doid}/hierarchicalChildren"

    response = requests.get(children_url)
    if response.status_code == 200:
        data = response.json()
        if "_embedded" in data and "terms" in data["_embedded"]:
            for term in data["_embedded"]["terms"]:
                child_id = term.get('obo_id', 'N/A')
                child_name = term.get('label', 'N/A')
                print(f"{indent}- {child_id}: {child_name}")
                # Prevent infinite loops by tracking visited nodes
                if child_id not in visited:
                    visited.add(child_id)
                    l.append(child_name)
                    get_children(child_id, level + 1, visited)  # Recursive call
        else:
            print(f"{indent}No further children found.")
    else:
        print(f"{indent}Failed to fetch children for {doid} (HTTP {response.status_code})")
    return l

print("Hierarchy for DOID:303")
get_children("DOID:303")