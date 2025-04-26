class JobContext:
    def __init__(self):
        self.slots = {}
    def update(self, new_slots: dict):
        for k, v in new_slots.items():
            self.slots[k] = v
    def to_params(self, api_name: str) -> dict:
        mapping = {
            'keywords': {'cj':'keywords','jj':'keywords','w3':'tag'},
            'location': {'cj':'location','jj':'location','w3':'country'},
            'remote': {'w3':'remote'},
            'days': {'jj':'datePosted','w3':'posted_since'},
        }
        params = {}
        for slot, val in self.slots.items():
            if slot in mapping and api_name in mapping[slot]:
                key = mapping[slot][api_name]
                if slot == 'days':
                    params[key] = f"last {val} days"
                elif slot == 'remote':
                    params[key] = str(val).lower()
                elif slot == 'keywords':
                    params[key] = " ".join(val) if isinstance(val, list) else val
                else:
                    params[key] = val
        return params
