import os
import re
from shell import BashService


class EnvService:
    """
    This class checks environment variables required for processing workflow
    """
    def __init__(self):
        pass

    @staticmethod
    def check_all_required_nextprot_envs():
        np_var_names = ["PY_INTEGRATION_HOME", "NP_LOADERS_HOME", "NP_CV_HOME", "NP_PERL_PARSERS_HOME", "PERL5LIB"]
        EnvService.check_envs(np_var_names)

    @staticmethod
    def check_envs(var_names):
        """Check that the given environment variables needed to process integration were correctly set
        quit with an error if at least one variable is missing"""

        for var_name in var_names:
            if os.getenv(var_name) is None:
                raise OSError("OS environment variable '"+var_name + "' has to be set.")

    @staticmethod
    def get_py_integration_home():
        return os.getenv("PY_INTEGRATION_HOME")

    @staticmethod
    def get_np_loaders_home():
        return os.getenv("NP_LOADERS_HOME")

    @staticmethod
    def get_np_dataload_prop_filename():
        return EnvService.get_np_loaders_home() + "/dataload.properties"

    @staticmethod
    def get_np_perl_parsers_home():
        return os.getenv("NP_PERL_PARSERS_HOME")

    @staticmethod
    def get_np_cv_home():
        return os.getenv("NP_CV_HOME")


class SoftwareCheckr:
    """
    This class checks host environment for mandatory software dependencies and minimum version
    """
    def __init__(self):
        pass

    @staticmethod
    def check_all_required_softwares():
        SoftwareCheckr.check_jdk_software()
        SoftwareCheckr.check_ant_software()
        SoftwareCheckr.check_maven_software()
        SoftwareCheckr.check_psql_software()

    @staticmethod
    def check_software_exists(soft_name):
        """Check that the software exists
        """
        shell_result = BashService.exec_bash(soft_name)

        if shell_result.return_code != 0:
            raise ValueError(soft_name+": "+shell_result.stderr)

    @staticmethod
    def check_jdk_software(min_version="1.7"):
        """Check that the minimum version of jdk is installed
        """
        SoftwareCheckr.check_software_exists("java -h")

        EnvService.check_envs(["JAVA_HOME"])
        # note: java -version flush output to stderr
        shell_result = BashService.exec_bash("java -version", swap_output_error=True)

        m = re.search(r'java version "(\d+\.\d+.\d+).*"', shell_result.stdout.split("\n")[0])

        SoftwareCheckr.__check_minimum_version("jdk", m.group(1), min_version)

    @staticmethod
    def check_ant_software(min_version="1.8"):
        """Check that the exact version of ant is installed
        """
        SoftwareCheckr.check_software_exists("ant -h")

        EnvService.check_envs(["ANT_HOME"])
        current_version = SoftwareCheckr.__bash_extract_software_version("ant -version", re.compile(r'.+version (\d+\.\d+.\d+).*'))

        SoftwareCheckr.__check_minimum_version("ant", current_version, min_version)

    @staticmethod
    def check_maven_software(min_version="3.0.5"):
        """Check that the minimum version of ant is installed
        """
        SoftwareCheckr.check_software_exists("mvn -h")

        EnvService.check_envs(["M2_HOME"])
        current_version = SoftwareCheckr.__bash_extract_software_version("mvn -version", re.compile(r'Apache Maven (\d+\.\d+.\d+).*'))

        SoftwareCheckr.__check_minimum_version("maven", current_version, min_version)

    @staticmethod
    def check_psql_software(version="9.2"):
        """Check that the given version of psql is installed
        """
        SoftwareCheckr.check_software_exists("psql --help")

        current_version = SoftwareCheckr.__bash_extract_software_version("psql --version", re.compile(r'psql \(PostgreSQL\) (\d+\.\d+)\.\d+'))

        SoftwareCheckr.__check_minimum_version("psql", current_version, version, exact=True)

    @staticmethod
    def __bash_extract_software_version(bash_command_version, pattern):
        """Extract the version number from bash command version
        """

        shell_result = BashService.exec_bash(bash_command_version)

        m = pattern.search(shell_result.stdout)
        return m.group(1)

    @staticmethod
    def __check_minimum_version(software_name, current_version, required_version, exact=False):
        """Verify that the current version number respect the required version
        """
        if exact:
            if current_version != required_version:
                raise OSError(software_name+" version '"+current_version + "' does not fit the exact requirement ("+required_version+")")
        else:
            current_version_array = [int(numeric_string) for numeric_string in current_version.split('.')]
            required_version_array = [int(numeric_string) for numeric_string in required_version.split('.')]

            if current_version_array < required_version_array:
                raise OSError(software_name+" version '"+current_version + "' does not fit the minimum requirement ("+required_version+")")
