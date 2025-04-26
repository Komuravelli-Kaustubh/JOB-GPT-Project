from core.api_clients import CareerjetClient, JoobleClient, Web3Client
from core.parser import parse_query
from core.job_context import JobContext

def aggregate(*lists):
    seen = {}
    for lst in lists:
        for job in lst:
            key = job.get('apply_url') or job.get('url')
            if key and key not in seen:
                seen[key] = job
    return list(seen.values())

class JobOrchestrator:
    def __init__(self):
        self.context = JobContext()
        self.cj = CareerjetClient('en_IN')
        self.jj = JoobleClient()
        self.w3 = Web3Client()
        self.history = []

    def handle(self, user_message: str):
        last_five = self.history[-5:]
        try:
            slots = parse_query(user_message, last_five)
        except Exception:
            slots = {}
        if not slots:
            return "I’m missing some details—can you specify role or location?"

        merged = self.context.slots.copy()
        merged.update(slots)
        self.context.slots = merged

        self.history.append((user_message, merged.copy()))
        if len(self.history) > 5:
            self.history.pop(0)

        cj_p = self.context.to_params('cj')
        jj_p = self.context.to_params('jj')
        w3_p = self.context.to_params('w3')

        jobs = aggregate(
            self.cj.search(**cj_p),
            self.jj.search(**jj_p),
            self.w3.search(**w3_p)
        )

        if not jobs:
            return "No matching jobs found. Try broadening your search."

        lines = []
        for i, job in enumerate(jobs[:5], 1):
            title = job.get('title', 'N/A')
            company = job.get('company', 'N/A')
            loc = job.get('location') or job.get('locations', 'N/A')
            url = job.get('apply_url') or job.get('url', '')
            lines.append(f"{i}. **{title}** at {company} ({loc})\nApply: {url}")
        lines.append("\nAnything else I can refine?")
        return "\n\n".join(lines)
