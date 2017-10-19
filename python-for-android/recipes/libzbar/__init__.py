from pythonforandroid.toolchain import shprint, current_directory
from pythonforandroid.recipe import Recipe
from multiprocessing import cpu_count
import sh


class LibZBarRecipe(Recipe):

    version = '0.10'

    url = 'https://github.com/ZBar/ZBar/archive/{version}.zip'

    depends = ['hostpython2', 'python2', 'libiconv']

    patches = ["werror.patch"]

    def build_arch(self, arch):
        # TODO:
        # - handle libiconv:
        #   https://sourceforge.net/p/zbar/discussion/664595/thread/fcf39edc/
        super(LibZBarRecipe, self).build_arch(arch)
        env = self.get_recipe_env(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(sh.Command('autoreconf'), '-vif', _env=env)
            shprint(
                sh.Command('./configure'),
                '--host=' + arch.toolchain_prefix,
                '--target=' + arch.toolchain_prefix,
                '--prefix=' + self.ctx.get_python_install_dir(),
                # Python bindings are compiled in a separated recipe
                '--with-python=no',
                '--with-gtk=no',
                '--with-qt=no',
                '--with-x=no',
                '--with-jpeg=no',
                '--with-imagemagick=no',
                '--enable-pthread=no',
                '--enable-video=no',
                '--enable-shared=no',
                _env=env)
            shprint(sh.make, '-j' + str(cpu_count()), _env=env)
            assert False
            libs = ['.libs/libzbar.so']
            self.install_libs(arch, *libs)


recipe = LibZBarRecipe()
