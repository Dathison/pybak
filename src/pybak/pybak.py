import pybak_utils as PbUtils
import subprocess

class PybakBackup:
    def __init__(self, binary:str = "restic"):
        self.RESTIC_BINARY = binary

    def _run(self, *args):
        cmd = [self.RESTIC_BINARY] + list(args)

        result = subprocess.run(
            cmd,
            capture_output = True,
            text = True,
            check = True
            )

        return result

    def check_repo(self, repo_dir:str) -> bool:
        """
        Checks if a Restic repository exists at the specified path.

        Args:
            repo_dir (str): The path to check for.

        Returns:
            bool: True if a repository exists, false if it does not.
        """

        try:
            self._run("snapshots", "-r", repo_dir, "--insecure-no-password")

        except subprocess.CalledProcessError as e:
            match e.returncode:
                case 0 | 12:
                    return True
                
                case _:
                    return False

    def init(self, repo_dir:str, password_file:str = None):
        """
        Initialises a Restic repository at the specified location.

        Args:
            repo_dir (str): The location where the repository should be initialised.
            password_file (Optional[str]): The location for a file to be used as the password for the repository.

        Raises:
            FileExistsError: If repo_dir is already a Restic repository.
            ValueError: If password_file does not exist.
        """

        if self.check_repo(repo_dir) == True:
            raise FileExistsError(f"{repo_dir}: A repository already exists at that location. No repository initialised this time.")

        if PbUtils.lookup_file(password_file) == False:
            raise ValueError(f"{password_file}: File could not be found or does not exist.")

        try:
            if password_file == None:
                output = self._run("init", "-r", repo_dir)

            else:
                output = self._run("init", "-r", repo_dir, "-p", password_file)

            print(f"Repository succesfully initialiased at '{repo_dir}'!")
            return output

        except subprocess.CalledProcessError as e:
            return RuntimeError(f"An error occurred during repository initialisation with return code: {e.returncode}. Find more info below:\n\n-------------\n{e.stderr.strip()}\n-------------\n\n")

        except Exception as e:
            return RuntimeError(f"An error occurred. Find more info below:\n\n-------------\n{e.stderr.strip()}\n-------------\n\n")

    def backup(self, backup_src:str, repo_dir:str, password_file:str = None):
        """
        Backs up the specified location into the specified Restic repository.

        Args:
            backup_src (str): The path to be backed up.
            repo_dir (str): The Restic repository to store the backup in.
            password_file (str): The location for a file to be used as the password for the repository.

        Raises:
            ValueError:
                - If `backup_src` doesn't exist.
                - If `repo_dir` doesn't exist.
            PermissionError: 
                - If some or all files in `backup_src` couldn't be read.
                - If the wrong password is passed to the Restic repository.
            RuntimeError: If an unhandled error occurs. Please report these as bugs in Git.
        """

        if PbUtils.lookup_file(backup_src) == False and PbUtils.lookup_path(backup_src) == False:
            raise ValueError(f"{backup_src}: File/directory could not be found or does not exist.")

        try:
            if password_file == None:
                output = self._run("backup", backup_src, "-r", repo_dir)

            else:
                output = self._run("backup", backup_src, "-r", repo_dir, "-p", password_file)

            print(f"Backup of '{backup_src}' to '{repo_dir}' succesful!")
            return output

        except subprocess.CalledProcessError as e:
            match e.returncode:
                case 3:
                    return PermissionError(f"WARNING: Could not read all source data. Backup may be incomplete!")
                case 10:
                    return ValueError(f"ERROR: Restic repository does not exist at the specified location, so backup could not be executed.")
                case 12:
                    raise PermissionError(f"ERROR: Incorrect password for Restic repository.")
                case _:
                    raise RuntimeError(f"An error occurred during backup execution with. Find more info below:\n\n-------------\n{e.stderr.strip()}\n-------------\n\n")

        except Exception as e:
            raise RuntimeError(f"An error occurred. Find more info below:\n\n-------------\n{e.stder.strip()}\n-------------\n\n")