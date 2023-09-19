# HelmSyncBot
Automatically update the helmfile.yaml file by adding commit id  and run the command to make the pod up.

# Note (Imp)
Do uncomment the helmfile.yaml file in kube-manifest for which you want to make the pod up. 

# Changes which can be done in `helmfile_sync.py` according to use-case.
1. Add devstack_label on which you want to make pod up in file https://github.com/shubham25kr07/HelmSyncBot/blob/6914ef39409322a3c645febf0a56fe84c44f2dff/helmfile_sync.py#L7
2. If you want to deploy the pod with your commit id(i.e not master commit id), then in this function `deployWithGivenCommitId()`
   add like this `repo_name_with_given_commit_id['dashboard'] = 'your_commit_id' `, `repo_name_with_given_commit_id['api'] = 'your_commit_id' ` etc.. 

# One Time Setup
1. Add GITHUB_TOKEN in ~/.bash_profile
2. Add  helmfile_directory_path in https://github.com/shubham25kr07/HelmSyncBot/blob/6914ef39409322a3c645febf0a56fe84c44f2dff/helmfile_sync.py#L13
3. Add helmfile_yaml_path in https://github.com/shubham25kr07/HelmSyncBot/blob/6914ef39409322a3c645febf0a56fe84c44f2dff/helmfile_sync.py#L14

# Install PyGithub library
`pip3 install PyGithub`

# Run the file 
`python3 helmfile_sync.py`
