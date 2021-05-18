from conans import ConanFile, CMake, tools
import os
from glob import glob

class ApriltagConan(ConanFile):
    name = "apriltag"
    version = "3.1.4"
    license = "https://github.com/AprilRobotics/apriltag/raw/master/LICENSE.md"
    url = "https://github.com/AprilRobotics/apriltag"
    description = "AprilTag is a visual fiducial system popular in robotics research."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    options = {
        "shared": [True, False], 
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False, 
        "fPIC": True,
    }

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def source(self):
        tools.get("https://github.com/AprilRobotics/apriltag/archive/refs/tags/v{}.tar.gz".format(self.version))
        os.rename(glob("apriltag-{0}*".format(self.version))[0], self.source_subfolder)

    def build(self):
        apriltag_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        cmake = CMake(self)
        cmake.definitions["BUILD_PYTHON_WRAPPER"] = False
        cmake.configure(source_folder="source_subfolder", build_folder="build_subfolder")
        cmake.build()
        
        

    def package(self):
        include_path = os.path.join("include","apriltag");
        self.copy(pattern="*.h*", dst="include", src="source_subfolder", keep_path=True)
        self.copy(pattern="*.a", dst="lib", src="build_subfolder", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="build_subfolder", keep_path=False)


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
