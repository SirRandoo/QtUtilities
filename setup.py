# This file is part of QtUtilities.
#
# QtUtilities is free software:
# you can redistribute it and/or
# modify it under the terms of the
# GNU General Public License as
# published by the Free Software
# Foundation, either version 3 of
# the License, or (at your option)
# any later version.
#
# QtUtilities is
# distributed in the hope that it
# will be useful, but WITHOUT ANY
# WARRANTY; without even the implied
# warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License
# for more details.
#
# You should have received a copy of
# the GNU General Public License along
# with QtUtilities.
# If not, see <http://www.gnu.org/licenses/>.
from distutils.core import setup

setup(
        name='QtUtilities',
        version='0.1.0a',
        packages=['QtUtilities', 'QtUtilities.requests', 'QtUtilities.widgets'],
        url='https://www.github.com/SirRandoo/QtUtilities',
        license='LGPLv3+',
        author='SirRandoo',
        author_email='',
        description='A utility bundle for PyQt5.',
        requires=['PyQt5']
)