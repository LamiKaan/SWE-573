## Git commands learned during Week 1

`git clone (SSH key)` --> Bring a repository that is hosted somewhere like Github into a directory on your local machine  
`git add ./filename` --> Track your files and changes in Git, staged changes  
`git commit -m "title" -m "description"` --> Save your files in Git with a commit message   
`git remote add origin (SSH key)` --> Add a reference to a remote repository like Github. "origin" is basically a word that stands for the location of remote Git repository, could be anything but origin is widely used by convention  
`git push origin master/(branch)` --> Upload Git commits to the desired branch of the remote repo  
`git pull` --> Download changes from remote repo to your local machine, the opposite of push  
`git init` --> Turn directory into Git repository  
`git branch (name of branch)` --> Create a new branch or show the already existing branches (* symbol denotes the branch that I'm currently on)  
`git checkout (name of branch)` --> Switch between branches  
`git remote -v` --> See connected repositories  
`git diff (name of branch)` --> See the difference between current branch and (name of branch)  
`git merge (name of branch)` --> Merge (name of branch) to the current branch  
`git log` --> See log of all your commits  
`git reset (name of file)` --> Undo a "git add" command, unstaged changes