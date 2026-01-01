class PrometheusExporter:
    def __init__(self):
        self.jobs_total = 0

    def render(self):
        return (
            "# HELP cpos_jobs_total Total jobs compiled\n"
            "# TYPE cpos_jobs_total counter\n"
            f"cpos_jobs_total {self.jobs_total}\n"
        )

exporter = PrometheusExporter()
