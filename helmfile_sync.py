import os
from github import Github
import re
import subprocess

# Devstack Label
devstack_label = 'shubham-kr-noob'

# ADD GITHUB ACCESS TOKEN 
github_access_token = os.getenv('GITHUB_TOKEN')

# ADD HELMFILE DIRECTORY PATH
helmfile_directory_path = '/Users/shubham.k/Desktop/Razorpay/kube-manifests/helmfile'
helmfile_yaml_path = '/Users/shubham.k/Desktop/Razorpay/kube-manifests/helmfile/helmfile.yaml'

repository_owner = 'razorpay'
repo_names_to_deploy_with_master_commit_id = ['dashboard', 'api', 'scrooge', 'terminals', 'pg-router', 'payment-links', 'gimli', 'reminders']

helmfile_lint_command = 'helmfile lint'
helmfile_delete_and_sync_command = 'helmfile delete && helmfile sync'

def fetchCommitIdForRepo():
   
   g = Github(github_access_token)
   try:
      repository_names_commit_id = {}
      for repo_name in  repo_names_to_deploy_with_master_commit_id:
         repo = g.get_repo(f'{repository_owner}/{repo_name}')
         latest_commit = repo.get_commits(sha='master')[0]
         repository_names_commit_id[repo_name] = latest_commit.sha
         
      return repository_names_commit_id
   except Exception as e:
      print(f'An error occurred: {e}')


def updateYAMLfile(repository_names_commit_id):
   
   with open(helmfile_yaml_path, 'r') as file:
      lines = file.readlines()
   
   find_image_after_namespace = False
   update_devstack_label = True
   
   for i, line in enumerate(lines):
      
      # This part will update the devstack label .
      pattern_for_devstack_label = r'devstack_label:\s+'
      match_devstack_label = re.search(pattern_for_devstack_label, line)
      if update_devstack_label and match_devstack_label:
         lines[i] = f"      - devstack_label: {devstack_label}\n"
         update_devstack_label = False
         
      
      # This part will update the image commit. 
      pattern = r'namespace:\s+'
      match = re.search(pattern, line)
      if match:
         namespace_value = line.replace("namespace: ", "")
         trimmed_namespace_value = namespace_value.strip()
         
         if trimmed_namespace_value in repository_names_commit_id:
            commit_id = repository_names_commit_id[trimmed_namespace_value]
            find_image_after_namespace = True
         
      elif find_image_after_namespace == True and "image:" in line:
         lines[i] = f"    - image: {commit_id}\n"
         find_image_after_namespace = False

   
   with open(helmfile_yaml_path, 'w') as file:
      file.writelines(lines)


def runHelmfileCommand():
   try:
      os.chdir(helmfile_directory_path)
   except FileNotFoundError:
      print(f"Directory '{helmfile_directory_path}' not found.")
      exit(1)

   try:
      subprocess.run(helmfile_lint_command, shell=True, check=True)
      subprocess.run(helmfile_delete_and_sync_command, shell=True, check=True)
   except subprocess.CalledProcessError as e:
      print(f"Error running command: {e}")


# Get commit id 
repo_name_with_commit_id = fetchCommitIdForRepo() 

# Update helmfile.yaml File
updateYAMLfile(repo_name_with_commit_id)

# Run Helmfile command 
runHelmfileCommand()