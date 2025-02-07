import pybak_utils as PbUtils
import subprocess

class PybakBackup:
    def __init__(self, binary:str = "restic"):
        self.RESTIC_BINARY = binary

    def _run(self, *args):
        cmd = [self.RESTIC_BINARY] + ["--json"] + list(args)

        result = subprocess.run(
            cmd,
            capture_output = True,
            text = True
            )

        return result

    def init(self, repo_dir:str, password_file:str = None):
        """
        Initialises a Restic repository at the specified location.

        Args:
            repo_dir (str): Specify the location where the repository should be initialised.
            password_file (Optional[str]): Specify the location for a file to be used as the password for the repository.

        Raises:
            ValueError: If password_file does not exist.
        """

        if PbUtils.lookup_file(password_file) == False:
            raise ValueError(f"{password_file}: File could not be found or does not exist.")

        try:
            output = self._run("init", "-r", repo_dir, "-p", password_file)
            return output

        except Exception as e:
            print(f"An error occurred during repository initialisation. Find more info below:\n\n-------------\n{e}\n-------------\n\n")
