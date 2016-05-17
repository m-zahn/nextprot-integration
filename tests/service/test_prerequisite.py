from unittest import TestCase

from nextprot_integration.service.prerequisite import SoftwareCheckr, EnvService


class TestSoftwareCheckr(TestCase):

    def test_jdk(self):
        SoftwareCheckr.check_jdk_software()

    def test_jdk_bad_version(self):
        with self.assertRaises(OSError):
            SoftwareCheckr.check_jdk_software("1.8.75")

    def test_maven(self):
        SoftwareCheckr.check_maven_software()

    def test_maven_bad_version(self):
        with self.assertRaises(OSError):
            SoftwareCheckr.check_maven_software("3.5")

    def test_psql(self):
        SoftwareCheckr.check_psql_software()

    def test_psql_bad_version(self):
        with self.assertRaises(OSError):
            SoftwareCheckr.check_psql_software("9.3.0")

    def test_ant(self):
        SoftwareCheckr.check_ant_software()

    def test_ant_bad_version(self):
        with self.assertRaises(OSError):
            SoftwareCheckr.check_ant_software("1.10.2")

    def test_constr_check_all_software(self):
        SoftwareCheckr.check_all_required_softwares()

    def test_environment_vars(self):
        var_names = ["NP_SCRIPTS_HOME", "NP_LOADERS_HOME", "NP_CV_HOME", "NP_PERL_PARSERS_HOME", "PERL5LIB"]
        EnvService.check_envs(var_names)

    def test_environment_vars_not_found(self):
        var_names = ["NP_SCRIPTS_HOME", "NP_LOADERS_HOME", "NP_CV_HOME", "NP_PERL_PARSERS_HOM"]

        with self.assertRaises(OSError):
            EnvService.check_envs(var_names)

    def test_all(self):
        EnvService.check_all_required_nextprot_envs()
        self.assertIsNotNone(EnvService.get_py_integration_home())
        self.assertIsNotNone(EnvService.get_np_loaders_home())
        self.assertIsNotNone(EnvService.get_np_dataload_prop_filename())
        self.assertIsNotNone(EnvService.get_np_perl_parsers_home())
        self.assertIsNotNone(EnvService.get_np_cv_home())
