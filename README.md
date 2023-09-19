# HelmSyncBot
Automatically update the helmfile.yaml file by adding commit id  and run the command to make the pod up.

# Note
Do uncomment the helmfile.yaml file in kube-manifest for which you want to make the pod up. 
# Changes which can be done according to use-case
1. Add devstack_label on which you want to make pod up. 
2. If you want to deploy the pod with your commit id(i.e not master commit id), then in this function deployWithGivenCommitId()
   add like this `repo_name_with_given_commit_id['dashboard'] = 'your_commit_id' `
# One Time Setup 
Add GITHUB_TOKEN in ~/.bash_profile
Add  helmfile_directory_path
Add helmfile_yaml_path