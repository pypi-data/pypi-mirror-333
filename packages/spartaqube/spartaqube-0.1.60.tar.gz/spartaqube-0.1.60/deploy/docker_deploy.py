import os, sys, subprocess, shutil
# Docker deploy
# We are going to use the dist version (obfuscated for production)

# 1. We must integrate again the removed files and folders (docker folder)
# 2. Build Docker container

ROOT_VENV_TEST_LIB = f"{os.getenv('BMY_PATH_PROJECT')}\\spartaqube_test_lib"

def get_activate_cmd(version) -> str:
    venv_script_path = f'{ROOT_VENV_TEST_LIB}\\venv_{version}\\Scripts'.replace('\\','/')
    return os.path.join(venv_script_path, 'activate.bat')

def copy_docker_resources(version):
    '''
    Copy docker resources to the docker dist version
    '''
    current_path = os.path.dirname(__file__)
    root_path = os.path.dirname(current_path)
    source_root_path = os.path.join(root_path, 'spartaqube')
    dest_root_path = f"{ROOT_VENV_TEST_LIB}\\venv_{version}\\Lib\\site-packages\\spartaqube"
    # Copy docker-compose
    shutil.copy(os.path.join(source_root_path, 'docker-compose.yml'), os.path.join(dest_root_path, 'docker-compose.yml'))
    # Copy docker folder
    shutil.copytree(os.path.join(source_root_path, 'docker'), os.path.join(dest_root_path, 'docker'))

def generate_requirements_from_venv(version):
    '''
    Generate the requirements.txt from the current venv
    '''
    # 1. Generate requirements.txt
    current_path = os.path.dirname(__file__)
    process = subprocess.Popen(f"{get_activate_cmd(version)} & pip freeze > temp_requirements.txt", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=current_path)
    stdout, stderr = process.communicate()
    print("stdout generate requirements.txt")
    print(stdout)

    exclude_packages = ["pywin32", "win32", "file://"]
    with open(os.path.join(current_path, "temp_requirements.txt"), "r") as req_file:
        filtered_reqs = [line for line in req_file if not any(excl in line for excl in exclude_packages)]

    with open("requirements.txt", "w") as temp_file:
        temp_file.writelines(filtered_reqs)

    # 2. Copy requirements.txt
    requirements_filepath_dest = f"{ROOT_VENV_TEST_LIB}\\venv_{version}\\Lib\\site-packages\\spartaqube\\docker\\requirements.txt"
    with open(requirements_filepath_dest, "w") as temp_file:
        temp_file.writelines(filtered_reqs)

def build_docker_container(version):
    '''
    Build docker container
    '''
    # docker-compose up --build &
    dest_root_path = f"{ROOT_VENV_TEST_LIB}\\venv_{version}\\Lib\\site-packages\\spartaqube"
    process = subprocess.Popen(
        f"docker-compose up --build &", 
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
        shell=True, 
        cwd=dest_root_path,
        bufsize=1,  # Line-buffered output
        universal_newlines=True  # Ensures text output, not bytes
    )

    try:
        for line in iter(process.stdout.readline, ""):
            print(line, end="")  # Avoids extra newlines
    except:
        pass

def docker_login():
    '''
    Docker login
    '''
    from .docker_secrets import get_docker_secrets
    username = "spartaqube"
    password = get_docker_secrets()['password']
    process = subprocess.run(
        ["docker", "login", "-u", username, "--password-stdin"],
        input=password + "\n",  # Ensure newline at the end
        text=True,
        capture_output=True
    )
    print(process.stdout)
    print(process.stderr)

def docker_tag_and_push(version):
    '''
    Docker tag and push
    '''
    # 1. Docker tag
    process = subprocess.Popen(
        f"docker tag spartaqube-spartaqube spartaqube/spartaqube:{version} spartaqube/spartaqube:latest", 
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
        shell=True, 
        bufsize=1,  # Line-buffered output
        universal_newlines=True  # Ensures text output, not bytes
    )
    try:
        for line in iter(process.stdout.readline, ""):
            print(line, end="")  # Avoids extra newlines
    except:
        pass
    
    # 2. Docker tag
    process = subprocess.Popen(
        f"docker push spartaqube/spartaqube:{version}", 
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
        shell=True, 
        bufsize=1,  # Line-buffered output
        universal_newlines=True  # Ensures text output, not bytes
    )
    try:
        for line in iter(process.stdout.readline, ""):
            print(line, end="")  # Avoids extra newlines
    except:
        pass

    # Push the latest tag
    process_latest = subprocess.Popen(
        "docker push spartaqube/spartaqube:latest", 
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
        shell=True, bufsize=1, universal_newlines=True
    )

    try:
        for line in iter(process_latest.stdout.readline, ""):
            print(line, end="")  # Avoids extra newlines
    except:
        pass

def entrypoint_docker_deploy(version):
    '''
    Docker deployment entrypoint
    '''
    # 1. Copy docker resources
    copy_docker_resources(version)

    # 2. Generate requirements.txt
    generate_requirements_from_venv(version)

    # 3. Build with docker-compose
    build_docker_container(version)

    # 4. Tests docker version?

    # 5. Push to dockerhub
    docker_login()
    docker_tag_and_push(version)
