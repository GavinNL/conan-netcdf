from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

#
# This is the conan recipe for libnetcdf. This recipe is for the older
# version of netcdf which does not use Cmake or Git. The source is
# downloaded from ftp.
#
#
# This will need to be modified for the newer versions which use git
#
class LibnetcdfConan(ConanFile):
    name = "netcdf"
    version = "4.1.2"
    sha256 = "0c8df55f5967be2cd6ede1a1e8a4a96a69d6b716ec649b3eba9640dbbcda16b9"

    ftp_address = "ftp.unidata.ucar.edu"
    file_name = "netcdf-{0}.tar.gz".format(version)
    ftp_file_path = "pub/netcdf/old/{0}".format(file_name)

    license = "BSD"
    url = "https://github.com/conan-community/conan-libalsa"
    description = "Library of ALSA: The Advanced Linux Sound Architecture, that provides audio " \
                  "and MIDI functionality to the Linux operating system"
    options = {"shared": [True, False] }
    default_options = "shared=False"
    settings = "os", "compiler", "build_type", "arch"
    build_policy = "missing"

    _source_subfolder = "source_subfolder"

    def configure(self):
        print("Running configure()")
        if self.settings.os != "Linux":
            raise Exception("Only Linux supported")
#
#    def source(self):
#        self.run("git clone git://git.alsa-project.org/alsa-lib.git")
#        self.run("cd alsa-lib && git checkout v%s" % self.version)
#
#        tools.replace_in_file(os.path.join('alsa-lib', 'modules', 'mixer', 'simple', 'python.c'),
#                              'self->ob_type', 'Py_TYPE(self)')
#
    def source(self):
        tools.ftp_download(self.ftp_address, self.ftp_file_path)
        tools.check_sha256(self.file_name, self.sha256)
        tools.untargz(self.file_name)
        os.rename("netcdf-{0}".format(self.version), self._source_subfolder)
        #tools.get("{}/{}-{}.tar.gz".format(self.homepage, self.name, self.version))
        #os.rename("netcdf-4.1.2", self._source_subfolder)
#        if not tools.os_info.is_windows:
#            configure_file = os.path.join(self._source_subfolder, "configure")
#            st = os.stat(configure_file)
#            os.chmod(configure_file, st.st_mode | stat.S_IEXEC)


    def build(self):
        ab = AutoToolsBuildEnvironment(self)
        print( "Current directory: " + os.getcwd() )

        configure_args = [ '--enable-static=no', "--enable-shared=yes"]

        with tools.chdir( self._source_subfolder ):
            ab.configure(args=configure_args)
            ab.make(target="install")

        #with tools.environment_append(ab.vars):
        #    with tools.chdir(os.path.join(self.source_folder, "alsa-lib")):
        #        args = ["--enable-static=no", "--enable-shared=yes"] \
        #            if not self.options.shared else ["--enable-static=no", "--enable-shared=yes"]
        #        python = "--disable-python" if self.options.disable_python else ""
        #        self.run("touch ltconfig")
        #        #self.run("libtoolize --force --copy --automake")
        #        #self.run("aclocal $ACLOCAL_FLAGS")
        #        #self.run("autoheader")
        #        #self.run("automake --foreign --copy --add-missing")
        #        #self.run("touch depcomp")
        #        #self.run("autoconf")
        #        if python:
        #            args.append(python)
        #        args.append('--prefix=%s' % self.package_folder)
        #        ab.configure(args=args)
        #        self.run("make install")

    def package(self):
        self.copy("*COPYRIGHT*", dst="licenses")

    def package_info(self):
        self.cpp_info.libs = ["netcdf"]
        #self.env_info.ALSA_CONFIG_DIR = os.path.join(self.package_folder, "share", "alsa")
