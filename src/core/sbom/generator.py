import platform, subprocess

def generate_sbom(job_id, dag_signature):
    try: pkgs=subprocess.check_output(['pip','freeze'],text=True).splitlines()
    except Exception: pkgs=[]
    return {'job_id':job_id,'dag_signature':dag_signature,'platform':{'os':platform.platform(),'python':platform.python_version()},'python_packages':pkgs}
